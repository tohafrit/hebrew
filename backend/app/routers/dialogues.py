from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.dialogue import (
    DialogueBrief, DialogueDetail,
    DialogueCheckRequest, DialogueCheckResponse,
)
from app.services.dialogue import list_dialogues, get_dialogue, check_dialogue_answer
from app.services.gamification import award_xp, check_and_award_achievements

router = APIRouter(tags=["dialogues"])


@router.get("/dialogues", response_model=list[DialogueBrief])
async def get_dialogues(
    level_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    dialogues = await list_dialogues(db, level_id=level_id)
    return [DialogueBrief.model_validate(d) for d in dialogues]


@router.get("/dialogues/{dialogue_id}", response_model=DialogueDetail)
async def get_dialogue_detail(
    dialogue_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    dialogue = await get_dialogue(db, dialogue_id)
    if not dialogue:
        raise HTTPException(status_code=404, detail="Dialogue not found")
    return DialogueDetail.model_validate(dialogue)


@router.post("/dialogues/check", response_model=DialogueCheckResponse)
async def check_answer(
    req: DialogueCheckRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    dialogue = await get_dialogue(db, req.dialogue_id)
    if not dialogue:
        raise HTTPException(status_code=404, detail="Dialogue not found")

    is_correct, correct_idx, correct_text = check_dialogue_answer(
        dialogue, req.line_index, req.selected_option
    )

    xp_amount = 20 if is_correct else 2
    await award_xp(db, user, xp_amount, "dialogue_done")
    await check_and_award_achievements(db, user)
    await db.commit()

    return DialogueCheckResponse(
        correct=is_correct,
        correct_option=correct_idx,
        correct_text_he=correct_text,
    )
