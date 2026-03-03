import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import async_session
from app.routers import auth, health, seed, words, srs, alphabet, grammar, lessons, dialogues, gamification, topics, tts
from app.routers import settings as settings_router
from app.scripts.seed_dictionary import seed_dictionary

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-seed dictionary on startup if DB is empty
    try:
        async with async_session() as db:
            result = await seed_dictionary(db)
            logger.info("Seed result: %s", result)
    except Exception as e:
        logger.error("Seed failed: %s", e)
    yield


app = FastAPI(title="Ulpan AI", version="0.2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(seed.router, prefix="/api")
app.include_router(words.router, prefix="/api")
app.include_router(srs.router, prefix="/api")
app.include_router(alphabet.router, prefix="/api")
app.include_router(grammar.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(dialogues.router, prefix="/api")
app.include_router(gamification.router, prefix="/api")
app.include_router(settings_router.router, prefix="/api")
app.include_router(topics.router, prefix="/api")
app.include_router(tts.router, prefix="/api")
