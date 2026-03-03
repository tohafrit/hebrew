import hashlib
import os
from pathlib import Path

import edge_tts

AUDIO_DIR = Path("/app/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_VOICE = "he-IL-AvriNeural"
MAX_TEXT_LENGTH = 500


def _cache_key(text: str, voice: str, rate: str) -> str:
    """Generate a cache key based on text, voice, and rate."""
    raw = f"{voice}:{rate}:{text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


async def get_or_generate_audio(
    text: str,
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
) -> Path:
    """Generate MP3 audio via edge-tts, caching by content hash.

    Returns the full path to the cached MP3 file.
    """
    key = _cache_key(text, voice, rate)
    filename = f"{key}.mp3"
    filepath = AUDIO_DIR / filename

    if filepath.exists():
        return filepath

    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(filepath))

    return filepath
