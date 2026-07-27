 # This script ties the retriver part and embeddings part, builds embeddings + index once from processed data.

import os 
import pandas as pd

from triage.rag.embeddings import get_embeddings_batch, save_embeddings, load_embeddings
from triage.rag.retriever import build_index, save_index, load_index
from triage.utils.logger import get_logger

logger = get_logger(__name__)




from triage.config import config

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
PROCESSED_DATA_PATH = os.path.join(root_dir, config['data']['processed_path'])
EMBEDDINGS_PATH = os.path.join(root_dir, config['data']['embeddings_path'])
INDEX_PATH = os.path.join(root_dir, config['data']['index_path'])

def build_knowledge_base(force_rebuild:bool= False) :
    logger.info("Loading cached embeddings" if os.path.exists(EMBEDDINGS_PATH) and not force_rebuild else "Rebuilding embeddings via OpenAI API")
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
    