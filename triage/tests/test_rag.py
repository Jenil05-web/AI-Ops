import numpy as np
import pandas as pd
from triage.rag.retriever import build_index, search

def test_build_index_returns_correct_size():
    fake_embeddings = np.random.rand(10, 1536).astype('float32')
    index = build_index(fake_embeddings)
    assert index.ntotal ==10


def test_search_returns_k_results(monkeypatch):
    fake_embeddings = np.random.rand(5, 1536).astype('float32')
    index = build_index(fake_embeddings)


    df = pd.DataFrame({
        'subject': [f"subject_{i}" for i in range(5)],
        'body': [f"body_{i}" for i in range(5)],
        'answer': [f"answer_{i}" for i in range(5)],
    })


    def fake_embed_query(text, model=None):
        return np.random.rand(1, 1536).astype('float32')


    monkeypatch.setattr('triage.rag.retriever.embed_query', fake_embed_query)
    results = search("any query", index, df, k=3)
    assert len(results) ==3
    assert 'answer' in results.columns

## monkeypatch : this is a new testing concept : it temporarily replaces embed_query with a fake version during the test, 
# so the test doesn't make a real (paid) OpenAI API call every time we run test suite.
# This is standard practice for testing anything that touches external paid APIs.




