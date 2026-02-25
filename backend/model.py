import os
import joblib
import pandas as pd
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "saved_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "saved_vectorizer.pkl")

def preprocess(text):
    text = text.lower()
    text = "".join([char for char in text if char not in string.punctuation])
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# If model already saved → load it
if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    metrics = joblib.load(os.path.join(BASE_DIR, "metrics.pkl"))

else:
    # Load datasets
    true_df = pd.read_csv(os.path.join(BASE_DIR, "data", "True.csv"))
    fake_df = pd.read_csv(os.path.join(BASE_DIR, "data", "Fake.csv"))

    true_df["label"] = "REAL"
    fake_df["label"] = "FAKE"

    df = pd.concat([true_df, fake_df], axis=0)

    df["text"] = df["text"].fillna("")
    df["text"] = df["text"].apply(preprocess)

    X = df["text"]
    y = df["label"]

    vectorizer = TfidfVectorizer(max_features=5000)
    X_vectorized = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, pos_label="FAKE")
    recall = recall_score(y_test, y_pred, pos_label="FAKE")
    f1 = f1_score(y_test, y_pred, pos_label="FAKE")

    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }

    # Save model + vectorizer + metrics
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(metrics, os.path.join(BASE_DIR, "metrics.pkl"))

def predict_news(text):
    text = preprocess(text)
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)[0]
    probability = model.predict_proba(text_vectorized).max()
    return prediction, float(probability)

def get_metrics():
    return metrics
