from fastapi import APIRouter
from sqlalchemy import text

from app.database import async_session
from app.schemas.common import HealthResponse
from app.services.auth import get_redis

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    db_ok = False
    redis_ok = False

    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
            db_ok = True
    except Exception:
        pass

    try:
        r = await get_redis()
        await r.ping()
        redis_ok = True
    except Exception:
        pass

    return HealthResponse(status="ok", db=db_ok, redis=redis_ok)
