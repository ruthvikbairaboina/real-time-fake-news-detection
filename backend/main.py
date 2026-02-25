from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, Article
from schemas import NewsRequest, NewsResponse
from model import predict_news, get_metrics

app = FastAPI()

# ✅ Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root route
@app.get("/")
def root():
    return {"message": "Fake News Detection API is running"}

# Prediction endpoint
@app.post("/predict", response_model=NewsResponse)
def predict(news: NewsRequest, db: Session = Depends(get_db)):
    prediction, confidence = predict_news(news.text)

    article = Article(
        content=news.text,
        prediction=prediction,
        confidence=confidence
    )

    db.add(article)
    db.commit()

    return {
        "prediction": prediction,
        "confidence": confidence
    }

# Metrics endpoint
@app.get("/metrics")
def metrics():
    return get_metrics()