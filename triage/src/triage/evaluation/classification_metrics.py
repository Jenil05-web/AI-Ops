from sklearn.metrics import classification_report


def evaluate_classifier(y_true, y_pred) -> str:
    return classification_report(y_true, y_pred)