from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.tts import get_or_generate_audio, MAX_TEXT_LENGTH

router = APIRouter(prefix="/tts", tags=["tts"])

SPEED_MAP = {
    0.5: "-50%",
    0.75: "-25%",
    1.0: "+0%",
    1.25: "+25%",
    1.5: "+50%",
}


@router.get("/speak")
async def speak(
    text: str = Query(..., max_length=MAX_TEXT_LENGTH),
    rate: float = Query(1.0, ge=0.5, le=1.5),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate or serve cached TTS audio for Hebrew text."""
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text is required")

    rate_str = SPEED_MAP.get(rate, f"+{int((rate - 1) * 100)}%" if rate >= 1 else f"{int((rate - 1) * 100)}%")

    try:
        filepath = await get_or_generate_audio(text.strip(), rate=rate_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {e}")

    return FileResponse(
        path=str(filepath),
        media_type="audio/mpeg",
        filename="speech.mp3",
    )
