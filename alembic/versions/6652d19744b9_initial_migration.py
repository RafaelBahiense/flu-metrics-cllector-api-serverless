"""Initial migration

Revision ID: 6652d19744b9
Revises:
Create Date: 2024-10-11 00:59:09.552991

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6652d19744b9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "collected_health_metrics",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("timestamp", sa.DateTime, nullable=False),
        sa.Column("temperature", sa.Float, nullable=False),
        sa.Column("spo2", sa.Float, nullable=False),
        sa.Column("heart_rate", sa.Integer, nullable=False),
        sa.Column("device_id", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("collected_health_metrics")
