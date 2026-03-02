from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alphabet import AlphabetLetter, Nikkud


async def get_all_letters(db: AsyncSession) -> list[AlphabetLetter]:
    result = await db.execute(
        select(AlphabetLetter).order_by(AlphabetLetter.order)
    )
    return list(result.scalars().all())


async def get_all_nikkud(db: AsyncSession) -> list[Nikkud]:
    result = await db.execute(select(Nikkud).order_by(Nikkud.id))
    return list(result.scalars().all())


async def get_letter(db: AsyncSession, letter_id: int) -> AlphabetLetter | None:
    result = await db.execute(
        select(AlphabetLetter).where(AlphabetLetter.id == letter_id)
    )
    return result.scalar_one_or_none()
