"""create_tasks_table

Revision ID: 6aff2de8a784
Revises: 77a0a51fad5f
Create Date: 2025-08-08 20:47:48.322413

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6aff2de8a784"
down_revision: Union[str, Sequence[str], None] = "77a0a51fad5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_users", sa.Integer(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=30), nullable=False),
        sa.Column("describe", sa.TEXT(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "completed",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("completed_at", sa.DateTime()),
        sa.ForeignKeyConstraint(
            ["id_users"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tasks")
