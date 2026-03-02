from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.alphabet import AlphabetLetterOut, NikkudOut, AlphabetResponse
from app.services.alphabet import get_all_letters, get_all_nikkud, get_letter

router = APIRouter(tags=["alphabet"])


@router.get("/alphabet", response_model=AlphabetResponse)
async def get_alphabet(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    letters = await get_all_letters(db)
    nikkud = await get_all_nikkud(db)
    return AlphabetResponse(
        letters=[AlphabetLetterOut.model_validate(l) for l in letters],
        nikkud=[NikkudOut.model_validate(n) for n in nikkud],
    )


@router.get("/alphabet/letters/{letter_id}", response_model=AlphabetLetterOut)
async def get_letter_detail(
    letter_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    letter = await get_letter(db, letter_id)
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")
    return AlphabetLetterOut.model_validate(letter)
