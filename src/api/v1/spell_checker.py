from fastapi import APIRouter, Request, Depends

from src.services.spell_checker import SpellCheckerService
from src.enums.speller import VerbosityEnum
from src.dependencies.spell_checker import get_spell_checker_service

router = APIRouter(prefix='/spell-checker', tags=['spell-checker'])


@router.post("/")
async def spellcheck(request:Request,words:list[str],format:VerbosityEnum):
    service = request.app.state.spellchecker_service

    words = [service.lookup_word(word,format,2) for word in words]

    return words
