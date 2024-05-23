from pydantic import BaseModel


class SentimentPropsModel(BaseModel):
    text: str
