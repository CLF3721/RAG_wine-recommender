#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
@File         : wine-rag.py
@Created      : 2025-04-13 12:14:05
@Project      : Wine RAG
'''


###~~~~~~~~~~~~~~~~~~~~~>
###~> Data Manipulation
###~~~~~~~~~~~~~~~~~~~~~>
import pandas as pd
df = pd.read_csv('top_rated_wines.csv')
df = df[df['variety'].notna()] # remove any NaN values bc it blows up serialization
data = df.sample(500).to_dict('records') # minimuze datapoint nums for play
len(data)


###~~~~~~~~~~~~~>
###~> Embeddings
###~~~~~~~~~~~~~>
from sentence_transformers import SentenceTransformer
encoder = SentenceTransformer('all-MiniLM-L6-v2') # this encoder converts text into vectors embeddings


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

# Vectorize!
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

hits = qdrant.query_points(
    collection_name="top_wines",
    query=encoder.encode(user_prompt).tolist(),
    limit=3
)
print(hits)
search_results = []
for hit in hits.points:  # Note the .points accessor
    print(f"Wine: {hit.payload['name']}, Region: {hit.payload['region']}, Variety: {hit.payload['variety']}, Notes: {hit.payload['notes']}, Score: {hit.score}")
    search_results.append(hit.payload)


###~~~~~~~~~~~~~~~~~~~~~~~>
###~> Groq.com LLM Client
###~~~~~~~~~~~~~~~~~~~~~~~>
import os
from groq import Groq
client = Groq(
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