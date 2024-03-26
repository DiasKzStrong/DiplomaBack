from fastapi import APIRouter, Request
from src.services.sentiment_analysys import SentimentAnalysysService
from src.schemas.sentiment_analysys import SentimentPropsModel

router = APIRouter(prefix='/sentiment', tags=['sentiment analysys'])


@router.post("/")
async def sentiment_analysys(request:Request,body:SentimentPropsModel):
    service: SentimentAnalysysService = request.app.state.ml_serivce

    predict = service.predict_sentiment(body.text)

    sentiment = predict[0]
    procentage = predict[1]

    return {
        'sentiment': sentiment,
        'procentage': procentage
    }
