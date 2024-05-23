from fastapi import APIRouter

from .spell_checker import router as spellchecker_router
from .sentiment_analysys import router as sentiment_analysy_router


router = APIRouter(prefix="/v1")

router.include_router(spellchecker_router)
router.include_router(sentiment_analysy_router)
