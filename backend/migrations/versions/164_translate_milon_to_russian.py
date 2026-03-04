"""Translate English translations from milon import to Russian.

Translations are performed via scripts/translate_to_russian.py
which runs on the host and uses Google Translate (deep_translator).

This migration is a version marker only — the actual translation
is done by the script connecting directly to the database.

Revision ID: 164
Revises: 163
"""
from alembic import op

revision = "164"
down_revision = "163"


def upgrade() -> None:
    # Translation done via scripts/translate_to_russian.py
    # This migration exists to maintain the version chain.
    pass


def downgrade() -> None:
    pass
