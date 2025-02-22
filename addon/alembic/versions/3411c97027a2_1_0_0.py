"""1.0.0

Revision ID: 3411c97027a2
Revises:
Create Date: 2025-02-22 21:19:57.842348

"""

import sqlalchemy as sa
from alembic import op

revision = "3411c97027a2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "key_values",
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("value", sa.UnicodeText(), nullable=True),
        sa.PrimaryKeyConstraint("key", name=op.f("pk_key_values")),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )


def downgrade():
    op.drop_table("users")
    op.drop_table("key_values")
