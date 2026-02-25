# real-time-fake-news-detection

Real-Time Fake News Detection System

A production-ready machine learning-powered fake news detection platform built using FastAPI and Scikit-learn.

This system performs NLP preprocessing, trains a Logistic Regression classifier using TF-IDF features, evaluates model performance with precision/recall/F1 metrics, and exposes a REST API for real-time predictions.

Features

TF-IDF feature engineering for text vectorization

Logistic Regression classifier

Train/Test split with evaluation metrics

Accuracy, Precision, Recall, and F1 Score endpoint

Model persistence using joblib (no retraining on restart)

REST API built with FastAPI

SQLite database for storing predictions

Swagger documentation support

Model Performance

The model is evaluated using an 80/20 train-test split.

Metrics include:

Accuracy

Precision

Recall

F1 Score

Use the /metrics endpoint to view performance results.

API Endpoints
POST /predict

Predict whether a news article is REAL or FAKE.

Request Body example:

{
"text": "Sample news article text here."
}

Response example:

{
"prediction": "REAL",
"confidence": 0.94
}

GET /metrics

Returns model evaluation metrics:

{
"accuracy": 0.99,
"precision": 0.99,
"recall": 0.98,
"f1_score": 0.99
}

Tech Stack

Python

FastAPI

Scikit-learn

Pandas

NLTK

SQLAlchemy

SQLite

Joblib

Project Structure

fake-news-detector/

│
├── backend/
│ ├── main.py
│ ├── model.py
│ ├── database.py
│ ├── schemas.py
│ └── data/
│
├── frontend/
│
└── README.md

Dataset

Fake and Real News Dataset from Kaggle:

https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset

Place Fake.csv and True.csv inside:

backend/data/

Running the Project Locally

Backend:

cd backend
venv\Scripts\python -m uvicorn main:app --reload

Then visit:

http://127.0.0.1:8000/docs

Future Improvements

Upgrade to BERT-based transformer model

Add confusion matrix visualization

Deploy to cloud (Render / AWS / Railway)


Author

Ruthvik Bairaboina
Master's in Computer Science
University of North Texas
