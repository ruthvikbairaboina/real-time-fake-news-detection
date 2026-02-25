from pydantic import BaseModel

class NewsRequest(BaseModel):
    text: str

class NewsResponse(BaseModel):
    prediction: str
    confidence: float