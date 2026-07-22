import os
import re
import pandas as pd

# Calculate the project's data directory relative to this file's location
current_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA_DIR = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "data", "raw"))

DEFAULT_FILES = [
    'dataset-tickets-multi-lang-4-20k.csv', 
    'dataset-tickets-multi-lang3-4k.csv', 
    'aa_dataset-tickets-multi-lang-5-2-50-version.csv'
]

def load_raw_data(data_dir: str = DEFAULT_DATA_DIR, files: list[str] = None) -> pd.DataFrame:
    """Load and merge the CSV files"""
    if files is None:
        files = DEFAULT_FILES
    
    df_temp = [pd.read_csv(os.path.join(data_dir, f)) for f in files]
    df = pd.concat(df_temp, ignore_index=True)
    return df

def filter_english_tickets(df: pd.DataFrame) -> pd.DataFrame:
    """Keeping only english language tickets"""
    return df[df['language'] == 'en']

def drop_unused_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop sparse tag columns and metadata not needed for MVP."""
    cols_to_drop = [c for c in df.columns if c.startswith('tag_')] + \
                   ['business_type', 'version', 'language']
    return df.drop(columns=[c for c in cols_to_drop if c in df.columns])

def drop_missing_and_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with missing core text fields and duplicate ticket bodies."""
    df = df.dropna(subset=['subject', 'body', 'answer'])
    df = df.drop_duplicates(subset='body')
    return df

def clean_text(text: str) -> str:
    """Strip HTML tags/placeholders and collapse whitespace."""
    if pd.isna(text):
        return text
    text = re.sub(r'<[^>]+>', ' ', str(text))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def build_text_input(df: pd.DataFrame) -> pd.DataFrame:
    """Combine subject + body into a single text_input column, clean it and the answer column."""
    df['text_input'] = (df['subject'] + " " + df['body']).apply(clean_text)
    df['answer'] = df['answer'].apply(clean_text)
    return df

def clean_pipeline(files: list[str] = None) -> pd.DataFrame:
    """Run the full cleaning pipeline end-to-end."""
    df = load_raw_data(files=files)
    df = filter_english_tickets(df)
    df = drop_unused_columns(df)
    df = drop_missing_and_duplicates(df)
    df = build_text_input(df)
    return df 

DEFAULT_OUTPUT_PATH = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "data", "processed", "tickets_clean.csv"))

def save_processed_data(df: pd.DataFrame, output_path: str = DEFAULT_OUTPUT_PATH) -> None:
    """Save the cleaned dataframe to disk."""
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    df_cleaned = clean_pipeline()
    print("Final shape:", df_cleaned.shape)
    save_processed_data(df_cleaned)
    print(f"Saved to {DEFAULT_OUTPUT_PATH}")


# Note the pattern: every function takes a dataframe in, returns a dataframe out.