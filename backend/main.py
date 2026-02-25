from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Article
from schemas import NewsRequest, NewsResponse
from model import predict_news
from model import predict_news, get_metrics

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

    return {"prediction": prediction, "confidence": confidence}

@app.get("/metrics")
def metrics():
    return get_metrics()