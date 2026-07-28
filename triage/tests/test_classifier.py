import numpy as np
from triage.models.classifier import build_vectorizer, build_model, predict
from sklearn.preprocessing import LabelEncoder


def test_build_vectorizer_returns_fitted_shape():
    vectorizer = build_vectorizer(max_features=100)
    X = vectorizer.fit_transform(["hello world", "billing issue here"])
    assert X.shape[0] == 2
    assert X.shape[1] <= 100


def test_build_model_returns_xgb_classifier():
    model = build_model()
    assert hasattr(model, 'fit')
    assert hasattr(model, 'predict')


def test_predict_returns_known_label():
    vectorizer = build_vectorizer(max_features=50)
    texts = ["billing question about invoice", "server is down outage", "how to return an item"]
    labels = ["Billing and Payments", "Service Outages and Maintenance", "Returns and Exchanges"]

    X = vectorizer.fit_transform(texts)
    le = LabelEncoder()
    y = le.fit_transform(labels)

    model = build_model()
    model.fit(X, y)

    result, confidence = predict("invoice billing question", model, vectorizer, le)
    assert result in labels
    assert isinstance(confidence, float)
