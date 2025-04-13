#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
@File         : rag-wine.py
@Created      : 2025-04-13 12:14:05
@LastModified : ------
@Project      : Wine RAG - Coursera Guided Project - Duke University
'''



#######~~~~~~~~~~~~~~~~~~~~~~~~~~>
###>!~> Dev Imports & Env Settings
#######~~~~~~~~~~~~~~~~~~~~~~~~~~>
import sys
sys.path.append('/home/clf/_WSL-Foreshizzle/call-classifier')
sys.path.append('/home/clf/_WSL-Foreshizzle/call-classifier/utils')
import pandas as pd
pd.options.mode.copy_on_write = True
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.colheader_justify', 'left')
pd.set_option('display.max_info_columns', 300000)
pd.set_option('display.max_info_rows', 300000)
# import warnings
# warnings.filterwarnings("ignore", message="cudf.pandas detected an already configured memory resource")
# import cudf.pandas
# cudf.pandas.install()



###~~~~~~~~~~~~~~~~~~~~~>
###~> Data Manipulation
###~~~~~~~~~~~~~~~~~~~~~>
import pandas as pd
df = pd.read_csv('/home/clf/_WSL-Foreshizzle/learn-retrieval-augmented-generation/applied-rag/top_rated_wines.csv')
df = df[df['variety'].notna()] # remove any NaN values as it blows up serialization
data = df.sample(500).to_dict('records')
len(data)


###~~~~~~~~~~~~~>
###~> Embeddings
###~~~~~~~~~~~~~>
from sentence_transformers import SentenceTransformer
encoder = SentenceTransformer('all-MiniLM-L6-v2') # Create the sentence transformer encoder to convert text into vector embeddings


###~~~~~~~~~~~~~~~~~~~~~~~~~>
###~> Vector Database Client
###~~~~~~~~~~~~~~~~~~~~~~~~~>
from qdrant_client import models, QdrantClient
qdrant = QdrantClient(":memory:") # Create in-memory Qdrant instance

# Create collection to store wines
qdrant.create_collection(
    collection_name="top_wines",
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(), # Vector size is defined by used model
        distance=models.Distance.COSINE
    )
)

# vectorize!
qdrant.upload_points(
    collection_name="top_wines",
    points=[
        models.PointStruct(
            id=idx,
            vector=encoder.encode(doc["notes"]).tolist(),
            payload=doc,
        ) for idx, doc in enumerate(data) # data is the variable holding all the wines
    ]
)

# Search time for awesome wines!
user_prompt = "Provide me with a list of amazing wines from Mendoza Argentina"

hits = qdrant.search(
    collection_name="top_wines",
    query_vector=encoder.encode(user_prompt).tolist(),
    limit=3
)
for hit in hits:
  print(hit.payload, "score:", hit.score)

# Define a variable to hold the search results
search_results = [hit.payload for hit in hits]


###~~~~~~~~~~~~~~~~~~~~~~~~~>
###~> Local LLM Client
###~~~~~~~~~~~~~~~~~~~~~~~~~>
import os
from groq import Groq
client = Groq(
    # base_url="http://127.0.0.1:8080/v1", # "http://<Your api-server IP>:port"
    api_key = os.environ.get("GROQ_API_KEY")
)

chat_completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You are chatbot, a wine specialist. Your top priority is to help guide users into selecting amazing wine and guide them with their requests."},
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": str(search_results)}
    ]
)
print(chat_completion.choices[0].message.content)