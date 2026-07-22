# combining the logic of notebook 1 and notebook 2 

import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

from triage.models.classifier import build_vectorizer, build_model, save_artifacts

current_dir = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DATA_PATH = os.path.abspath(
    os.path.join(current_dir, "..", "..", "..", "data", "processed", "tickets_clean.csv")
)
MODEL_DIR = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "models"))


def load_processed_data(path: str = PROCESSED_DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def train_and_evaluate():
    df = load_processed_data()

    X = df['text_input']
    y = df['queue']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = build_vectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    label_encoder = LabelEncoder()
    y_train_enc = label_encoder.fit_transform(y_train)
    y_test_enc = label_encoder.transform(y_test)

    model = build_model()
    model.fit(X_train_vec, y_train_enc)

    y_pred_enc = model.predict(X_test_vec)
    y_pred = label_encoder.inverse_transform(y_pred_enc)
    y_test_labels = label_encoder.inverse_transform(y_test_enc)

    print(classification_report(y_test_labels, y_pred))

    os.makedirs(MODEL_DIR, exist_ok=True)
    save_artifacts(model, vectorizer, label_encoder, MODEL_DIR)
    print(f"Artifacts saved to {MODEL_DIR}")


if __name__ == "__main__":
    train_and_evaluate()