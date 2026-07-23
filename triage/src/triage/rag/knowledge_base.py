 # This script ties the retriver part and embeddings part, builds embeddings + index once from processed data.

import os 
import pandas as pd

from triage.rag.embeddings import get_embeddings_batch, save_embeddings, load_embeddings
from triage.rag.retriever import build_index, save_index, load_index


current_dir = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DATA_PATH = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "data", "processed", "tickets_clean.csv"))
EMBEDDINGS_PATH = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "data", "processed", "ticket_embeddings.npy"))
INDEX_PATH = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "data", "processed", "ticket_index.faiss"))

def build_knowledge_base(force_rebuild:bool= False) :
    df = pd.read_csv(PROCESSED_DATA_PATH)

    if os.path.exists(EMBEDDINGS_PATH) and not force_rebuild:
        embeddings = load_embeddings(EMBEDDINGS_PATH)
    else :
        embeddings = get_embeddings_batch(df['text_input'].tolist())
        save_embeddings(embeddings, EMBEDDINGS_PATH)

    if os.path.exists(INDEX_PATH) and not force_rebuild:
        index = load_index(INDEX_PATH)
    else:
        index = build_index(embeddings)
        save_index(index, INDEX_PATH)
        
    return index, df

if __name__ == "__main__":
    index, df = build_knowledge_base()
    print(f"Knowledge base built. Index size: {index.ntotal}")
    