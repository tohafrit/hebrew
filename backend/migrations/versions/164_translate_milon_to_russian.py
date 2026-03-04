"""Translate English translations from milon import to Russian.

Uses Google Translate (via deep_translator) to convert the 22K+ English
translations to Russian, processing in batches.

Revision ID: 164
Revises: 163
"""
import time

from alembic import op
import sqlalchemy as sa

revision = "164"
down_revision = "163"

BATCH_SIZE = 50  # Google Translate batch limit


def upgrade() -> None:
    from deep_translator import GoogleTranslator

    conn = op.get_bind()
    translator = GoogleTranslator(source='en', target='ru')

    # Find words with English-only translations (no Cyrillic characters)
    rows = conn.execute(sa.text("""
        SELECT id, translation_ru FROM words
        WHERE translation_ru ~ '[a-zA-Z]'
          AND translation_ru !~ '[а-яА-ЯёЁ]'
        ORDER BY id
    """)).fetchall()

    total = len(rows)
    print(f"  Words to translate: {total}")

    if total == 0:
        return

    updated = 0
    errors = 0

    for i in range(0, total, BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        texts = [row[1] for row in batch]
        ids = [row[0] for row in batch]

        try:
            translated = translator.translate_batch(texts)

            for word_id, russian in zip(ids, translated):
                if russian and russian.strip():
                    conn.execute(
                        sa.text("UPDATE words SET translation_ru = :ru WHERE id = :id"),
                        {"ru": russian.strip(), "id": word_id},
                    )
                    updated += 1

        except Exception as e:
            # If batch fails, try one by one
            for word_id, text in zip(ids, texts):
                try:
                    russian = translator.translate(text)
                    if russian and russian.strip():
                        conn.execute(
                            sa.text("UPDATE words SET translation_ru = :ru WHERE id = :id"),
                            {"ru": russian.strip(), "id": word_id},
                        )
                        updated += 1
                except Exception:
                    errors += 1

            time.sleep(1)  # Rate limit after error

        if (i + BATCH_SIZE) % 500 == 0 or i + BATCH_SIZE >= total:
            print(f"    Translated {min(i + BATCH_SIZE, total)}/{total} (errors: {errors})")
            conn.execute(sa.text("SELECT 1"))  # Keep connection alive

        # Small delay to avoid rate limiting
        time.sleep(0.3)

    print(f"  Done! Updated {updated} translations, {errors} errors")


def downgrade() -> None:
    print("  Note: downgrade does not revert translations.")
    print("  Original English translations are lost. Restore from backup if needed.")
