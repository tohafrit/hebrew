import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.routers import auth, health, words, srs, alphabet, grammar, lessons, dialogues, gamification, topics, tts, reader, learning_path, placement, minimal_pairs
from app.routers import settings as settings_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Cleanup on shutdown
    from app.services.auth import _redis
    if _redis is not None:
        await _redis.close()


app = FastAPI(title="Ulpan AI", version="0.2.0", lifespan=lifespan)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
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
app.include_router(reader.router, prefix="/api")
app.include_router(learning_path.router, prefix="/api")
app.include_router(placement.router, prefix="/api")
app.include_router(minimal_pairs.router, prefix="/api")
