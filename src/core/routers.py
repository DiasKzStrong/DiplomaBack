from fastapi import APIRouter
from ..authentication.api import v1_auth_router
from ..ml.api.v1 import spellchecker_router, sentiment_analysy_router
