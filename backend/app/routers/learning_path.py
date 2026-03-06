from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.learning_path import (
    get_all_paths,
    get_path_for_level,
    get_user_progress,
    complete_step,
    get_next_step,
)

router = APIRouter(prefix="/path", tags=["learning-path"])


class PathStepOut(BaseModel):
    id: int
    level_id: int
    unit: int
    step: int
    step_type: str
    content_id: int | None
    title_ru: str
    title_he: str | None
    description_ru: str | None
    icon: str | None
    completed: bool = False

    class Config:
        from_attributes = True


class PathResponse(BaseModel):
    steps: list[PathStepOut]
    next_step_id: int | None


class CompleteStepRequest(BaseModel):
    step_id: int


@router.get("", response_model=PathResponse)
async def get_path(
    level_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if level_id:
        steps = await get_path_for_level(db, level_id)
    else:
        steps = await get_all_paths(db)

    completed = await get_user_progress(db, user.id)
    user_level = user.current_level or 1
    next_step = await get_next_step(db, user.id, level_id or user_level)

    out = []
    for s in steps:
        step_out = PathStepOut(
            id=s.id,
            level_id=s.level_id,
            unit=s.unit,
            step=s.step,
            step_type=s.step_type,
            content_id=s.content_id,
            title_ru=s.title_ru,
            title_he=s.title_he,
            description_ru=s.description_ru,
            icon=s.icon,
            completed=s.id in completed,
        )
        out.append(step_out)

    return PathResponse(
        steps=out,
        next_step_id=next_step.id if next_step else None,
    )


@router.get("/recommended")
async def get_recommended_step(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Return the next uncompleted step with a descriptive label."""
    user_level = user.current_level or 1
    step = await get_next_step(db, user.id, user_level)
    if not step:
        return {"step": None}

    step_labels = {
        "vocabulary": "Изучить слова",
        "grammar": "Грамматика",
        "exercise": "Упражнения",
        "reading": "Читать текст",
        "dialogue": "Пройти диалог",
        "srs_review": "Повторить карточки",
    }
    label = step_labels.get(step.step_type, step.step_type)

    return {
        "step": {
            "id": step.id,
            "level_id": step.level_id,
            "unit": step.unit,
            "step": step.step,
            "step_type": step.step_type,
            "content_id": step.content_id,
            "title_ru": step.title_ru,
            "label": f"{label}: {step.title_ru}",
        }
    }


@router.post("/complete")
async def mark_complete(
    req: CompleteStepRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    ok = await complete_step(db, user.id, req.step_id)
    if not ok:
        return {"message": "Already completed or step not found"}
    await db.commit()
    return {"message": "Step completed", "step_id": req.step_id}
