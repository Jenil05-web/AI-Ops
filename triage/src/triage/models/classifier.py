# This file defines what the model is (build/load/predict logic)...

# And we are converting the logic from notebook 2 to this file

import joblib
import xgboost as xgb
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer

def build_vectorizer(max_features: int=5000)-> TfidfVectorizer:
  return TfidfVectorizer(max_features=max_features, stop_words='english')

def build_model() -> xgb.XGBClassifier: # We have used XGBoost to address the multi-class text classification problem 
    return xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
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

def predict(text: str, model, vectorizer, label_encoder) -> str:
    """Predict the queue for a single raw ticket text string."""    
    vec = vectorizer.transform([text])
    pred_encoded = model.predict(vec)
    return label_encoder.inverse_transform(pred_encoded)[0]