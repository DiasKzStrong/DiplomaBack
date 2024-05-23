from fastapi import APIRouter, Request

from src.ml.schemas.spell_checker import SpellPropsModel
from src.ml.enums.speller import VerbosityEnum
from src.ml.utils import split_text

router = APIRouter(prefix="/spell-checker", tags=["spell-checker"])


@router.post("/")
async def spellcheck(request: Request, text: SpellPropsModel, format: VerbosityEnum):
    service = request.app.state.spellchecker_service

    words = split_text(text.text)

    words = [service.lookup_word(word, format, 2) for word in words]

    return words
