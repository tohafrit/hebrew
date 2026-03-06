from sqlalchemy import select, func, or_, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.word import Word, RootFamily, RootFamilyMember


async def list_words(
    db: AsyncSession,
    *,
    page: int = 1,
    per_page: int = 20,
    search: str | None = None,
    pos: str | None = None,
    level_id: int | None = None,
    frequency: int | None = None,
    root: str | None = None,
    sort_by: str = "hebrew",
) -> tuple[list[Word], int]:
    """Return paginated word list with optional filters."""
    query = select(Word)

    if search:
        pattern = f"%{search}%"
        query = query.where(
            or_(
                Word.hebrew.ilike(pattern),
                Word.transliteration.ilike(pattern),
                Word.translation_ru.ilike(pattern),
            )
        )

    if pos:
        query = query.where(Word.pos == pos)

    if level_id:
        query = query.where(Word.level_id == level_id)

    if frequency is not None:
        query = query.where(Word.frequency_rank == frequency)

    if root:
        query = query.where(Word.root == root)

    # Count
    count_q = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_q) or 0

    # Sort
    sort_col = getattr(Word, sort_by, Word.hebrew)
    query = query.order_by(sort_col)

    # Paginate
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    return list(result.scalars().all()), total


async def get_word_detail(db: AsyncSession, word_id: int) -> Word | None:
    """Return a word with its forms, examples, and root family members."""
    query = (
        select(Word)
        .options(selectinload(Word.forms), selectinload(Word.examples))
        .where(Word.id == word_id)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_root_family(db: AsyncSession, root: str) -> list[Word]:
    """Return all words sharing a root."""
    query = select(Word).where(Word.root == root).order_by(Word.hebrew)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_root_families(
    db: AsyncSession, *, page: int = 1, per_page: int = 20
) -> tuple[list[RootFamily], int]:
    """Return paginated root families with their member words."""
    count_q = select(func.count()).select_from(RootFamily)
    total = await db.scalar(count_q) or 0

    query = (
        select(RootFamily)
        .options(selectinload(RootFamily.members))
        .order_by(RootFamily.root)
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    result = await db.execute(query)
    return list(result.scalars().unique().all()), total


async def get_root_family_detail(db: AsyncSession, root: str) -> dict | None:
    """Get detailed root family with words grouped by POS."""
    # Get root family info
    fam_result = await db.execute(
        select(RootFamily).where(RootFamily.root == root)
    )
    fam = fam_result.scalar_one_or_none()

    # Get all words with this root
    words_result = await db.execute(
        select(Word).where(Word.root == root).order_by(Word.pos, Word.hebrew)
    )
    words = list(words_result.scalars().all())

    if not words and not fam:
        return None

    # Group by POS
    by_pos: dict[str, list] = {}
    for w in words:
        pos = w.pos or "other"
        if pos not in by_pos:
            by_pos[pos] = []
        by_pos[pos].append(w)

    return {
        "root": root,
        "meaning_ru": fam.meaning_ru if fam else None,
        "words_by_pos": by_pos,
        "total_words": len(words),
    }


async def search_root_families(
    db: AsyncSession, search: str, limit: int = 20
) -> list[dict]:
    """Search root families by root or meaning."""
    pattern = f"%{search}%"
    q = (
        select(RootFamily)
        .where(
            or_(
                RootFamily.root.ilike(pattern),
                RootFamily.meaning_ru.ilike(pattern),
            )
        )
        .order_by(RootFamily.root)
        .limit(limit)
    )
    result = await db.execute(q)
    families = result.scalars().all()

    return [
        {"id": f.id, "root": f.root, "meaning_ru": f.meaning_ru}
        for f in families
    ]


async def get_dictionary_stats(db: AsyncSession) -> dict:
    """Return aggregated dictionary statistics."""
    total = await db.scalar(select(func.count()).select_from(Word)) or 0

    # By POS
    pos_q = select(Word.pos, func.count()).group_by(Word.pos)
    pos_result = await db.execute(pos_q)
    by_pos = {(row[0] or "unknown"): row[1] for row in pos_result.all()}

    # By frequency
    freq_labels = {1: "high", 2: "mid", 3: "low", 4: "rare"}
    freq_q = select(Word.frequency_rank, func.count()).group_by(Word.frequency_rank)
    freq_result = await db.execute(freq_q)
    by_frequency = {
        freq_labels.get(row[0], "unknown"): row[1]
        for row in freq_result.all()
        if row[0] is not None
    }

    root_count = await db.scalar(select(func.count()).select_from(RootFamily)) or 0

    return {
        "total_words": total,
        "by_pos": by_pos,
        "by_frequency": by_frequency,
        "root_families": root_count,
    }
