"""Version marker for number + proper noun detection in reader.

Code changes in backend/app/routers/reader.py:
- Numbers (2026, 50, ב-2) detected before dictionary lookup
- Proper nouns (names with geresh like אנג׳לס) detected after all lookups fail

Frontend changes in frontend/src/pages/reader.tsx:
- Numbers: neutral styling, no "not found" message
- Proper nouns: italic + "שם פרטי" label

Revision ID: 167
Revises: 166
"""

revision = "167"
down_revision = "166"


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
