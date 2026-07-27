 # Extracting the RAG logic of embeddings part from notebook 3

import numpy as np
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

from triage.config import config

EMBEDDING_MODEL = config['rag']['embedding_model']

def get_embeddings_batch(texts: list[str], model: str = EMBEDDING_MODEL, batch_size: int = 100) -> list[list[float]]:
    """Embed a list of texts in batches using OpenAI's embedding API."""
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(input=batch, model=model)
        all_embeddings.extend([e.embedding for e in response.data])
    return all_embeddings

def embed_query(text:str , model:str = EMBEDDING_MODEL)->np.ndarray:
    """Embed a single query string, returns shape (1, dim) for FAISS search.."""
    response = client.embeddings.create(input=[text], model=model)
    return np.array(response.data[0].embedding, dtype='float32').reshape(1, -1)

def save_embeddings(embeddings: list[list[float]], path: str) -> None:
    np.save(path, np.array(embeddings, dtype='float32'))

def load_embeddings(path: str) -> np.ndarray:
    return np.load(path)    


# Basically in this filew we are converting the data into embeddings 