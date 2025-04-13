# Retrieval Augmented Generation

This repo is a modified version from the Coursera Guided Project
[Introduction to RAG](https://www.coursera.org/projects/introduction-to-rag) by [Alfredo Deza](https://www.linkedin.com/in/alfredodeza/) from Duke University.


## Dataset overview:

The well-known wine dataset.

## Tech Stack overview:

1. [Qdrant](https://github.com/qdrant/qdrant) for the vector database. We will use an in-memory database for the examples
2. [Sentence Transformers](https://huggingface.co/sentence-transformers) - create the embeddings with minimal effort

**Use Llamafile for a full RAG and LLM setup**

3. [Groq's Python API](https://console.groq.com/docs/overview) - connect to the LLM after retrieving the vectors response from Qdrant
4. [Llamafile](https://github.com/Mozilla-Ocho/llamafile) for the LLM (alternatively you can use an Groq API compatible key and endpoint)
    
    > [Phi-2 model](https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file#other-example-llamafiles) is recommended due to its small size (approx 2GB). Download the model from the Llamafile repository and run it in your system.

## Setup your environment:

Create the virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:
```
.venv/bin/pip install -r requirements.txt
```

If this project is out of date or the req file install is acting up, here are the installs:
```
pip install --upgrade pip setuptools build wheel ipykernel ipywidgets jupyter pandas qdrant-client groq sentence-transformers
```

## Other Courses recommended by Alfredo Deza:

**Machine Learning:**

- [MLOps Machine Learning Operations Specialization](https://www.coursera.org/specializations/mlops-machine-learning-duke)
- [Open Source Platforms for MLOps](https://www.coursera.org/learn/open-source-platforms-duke)
- [Python Essentials for MLOps](https://www.coursera.org/learn/python-essentials-mlops-duke)

**Data Engineering:**

- [Linux and Bash for Data Engineering](https://www.coursera.org/learn/linux-and-bash-for-data-engineering-duke)
- [Web Applications and Command-Line tools for Data Engineering](https://www.coursera.org/learn/web-app-command-line-tools-for-data-engineering-duke)
- [Python and Pandas for Data Engineering](https://www.coursera.org/learn/python-and-pandas-for-data-engineering-duke)
- [Scripting with Python and SQL for Data Engineering](https://www.coursera.org/learn/scripting-with-python-sql-for-data-engineering-duke)
