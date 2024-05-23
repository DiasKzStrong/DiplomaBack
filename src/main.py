from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ml.api.v1 import router
from authentication.api import v1_auth_router
from ml.dependencies import get_spell_checker_instance, get_spell_checker_service
from ml.dependencies import get_sentiment_analysis_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load symspell model

    symspell = get_spell_checker_instance()
    app.state.spellchecker_service = get_spell_checker_service(symspell)

    ml_serivce = get_sentiment_analysis_service()
    app.state.ml_serivce = ml_serivce

    # Load the ML model
    yield
    # Clean up the ML models and release the resources


app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(v1_auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
