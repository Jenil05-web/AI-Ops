# Here we are retriveing the query , basically the retrieval part (logic from notebook 3)

import faiss
import pandas as pd
import numpy as np

from triage.rag.embeddings import embed_query

def build_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """Build a FAISS L2 index from an embeddings array."""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def save_index(index: faiss.IndexFlatL2, path:str)-> None:
    faiss.write_index(index,path)

def load_index(path:str)-> faiss.IndexFlatL2:
    return faiss.read_index(path)    


def search(query: str, index: faiss.IndexFlatL2, df: pd.DataFrame, k: int = 3) -> pd.DataFrame:
    """Search the index for the top-k most relevant tickets, return their subject/body/answer."""
    query_vec = embed_query(query)
    distances, indices = index.search(query_vec, k)
    results = df.iloc[indices[0]][['subject', 'body', 'answer']].copy()
    results['distance'] = distances[0]
    return results


