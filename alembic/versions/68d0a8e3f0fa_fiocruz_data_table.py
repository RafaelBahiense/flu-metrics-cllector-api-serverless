"""Create fio_cruz_data table

Revision ID: 68d0a8e3f0fa
Revises: 6652d19744b9
Create Date: 2024-10-12 13:04:55.131823

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "68d0a8e3f0fa"
down_revision: Union[str, None] = "6652d19744b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "fio_cruz_data",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("SG_UF_NOT", sa.Integer, nullable=False),
        sa.Column("fx_etaria", sa.String(10), nullable=False),
        sa.Column("SRAG", sa.Integer, nullable=False),
        sa.Column("SARS2", sa.Integer, nullable=False),
        sa.Column("VSR", sa.Integer, nullable=False),
        sa.Column("FLU", sa.Integer, nullable=False),
        sa.Column("FLU_A", sa.Integer, nullable=False),
        sa.Column("FLU_AH1N1", sa.Integer, nullable=False),
        sa.Column("FLU_AH3N2", sa.Integer, nullable=False),
        sa.Column("FLU_ANSUBTPD", sa.Integer, nullable=False),
        sa.Column("FLU_ANSUBTPV", sa.Integer, nullable=False),
        sa.Column("FLU_AINC", sa.Integer, nullable=False),
        sa.Column("FLU_AOUT", sa.Integer, nullable=False),
        sa.Column("FLU_B", sa.Integer, nullable=False),
        sa.Column("FLU_BVIC", sa.Integer, nullable=False),
        sa.Column("FLU_BYAM", sa.Integer, nullable=False),
        sa.Column("FLU_BNLIN", sa.Integer, nullable=False),
        sa.Column("FLU_BINC", sa.Integer, nullable=False),
        sa.Column("FLU_BOUT", sa.Integer, nullable=False),
        sa.Column("RINO", sa.Integer, nullable=False),
        sa.Column("ADNO", sa.Integer, nullable=False),
        sa.Column("BOCA", sa.Integer, nullable=False),
        sa.Column("METAP", sa.Integer, nullable=False),
        sa.Column("PARA1", sa.Integer, nullable=False),
        sa.Column("PARA2", sa.Integer, nullable=False),
        sa.Column("PARA3", sa.Integer, nullable=False),
        sa.Column("PARA4", sa.Integer, nullable=False),
        sa.Column("OUTROS", sa.Integer, nullable=False),
        sa.Column("positivos", sa.Integer, nullable=False),
        sa.Column("negativos", sa.Integer, nullable=False),
        sa.Column("aguardando", sa.Integer, nullable=False),
        sa.Column("DS_UF_SIGLA", sa.String(2), nullable=False),
        sa.Column("epiyear", sa.Integer, nullable=False),
        sa.Column("epiweek", sa.Integer, nullable=False),
        sa.Column("semana_epidemiologica", sa.Integer, nullable=False),
        sa.Column("ano_epidemiologico", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("fio_cruz_data")
