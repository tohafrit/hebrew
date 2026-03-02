from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.scripts.seed_dictionary import seed_dictionary

router = APIRouter(tags=["seed"])


@router.post("/seed/dictionary")
async def run_seed(db: AsyncSession = Depends(get_db)):
    result = await seed_dictionary(db)
    return result
