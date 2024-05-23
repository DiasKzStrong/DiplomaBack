from pydantic import BaseModel


class SpellPropsModel(BaseModel):
    text: str
