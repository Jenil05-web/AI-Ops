# This file defines what the model is (build/load/predict logic)...

# And we are converting the logic from notebook 2 to this file

import joblib
import xgboost as xgb
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer

from triage.config import config

def build_vectorizer(max_features: int=None)-> TfidfVectorizer:
  features = max_features if max_features is not None else config['model']['max_features']
  return TfidfVectorizer(max_features=features, stop_words='english')

def build_model() -> xgb.XGBClassifier: # We have used XGBoost to address the multi-class text classification problem 
    return xgb.XGBClassifier(
        n_estimators=config['model']['n_estimators'],
        max_depth=config['model']['max_depth'],
        learning_rate=config['model']['learning_rate'],
        objective='multi:softmax',
        eval_metric='mlogloss',
        random_state=42 
    )



def save_artifacts(model, vectorizer, label_encoder, model_dir: str) -> None:
    joblib.dump(model, f"{model_dir}/xgb_classifier.pkl")
    joblib.dump(vectorizer, f"{model_dir}/tfidf_vectorizer.pkl")
    joblib.dump(label_encoder, f"{model_dir}/label_encoder.pkl")

def load_artifacts(model_dir: str):
    model = joblib.load(f"{model_dir}/xgb_classifier.pkl")
    vectorizer = joblib.load(f"{model_dir}/tfidf_vectorizer.pkl")
    label_encoder = joblib.load(f"{model_dir}/label_encoder.pkl")
    return model, vectorizer, label_encoder

def predict(text: str, model, vectorizer, label_encoder) -> tuple[str, float]:
    vec = vectorizer.transform([text])
    proba = model.predict_proba(vec)[0]
    pred_idx = proba.argmax()
    confidence = float(proba[pred_idx])
    label = label_encoder.inverse_transform([pred_idx])[0]
    return label, confidence