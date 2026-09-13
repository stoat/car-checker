"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "vehicle_cache",
        sa.Column("registration", sa.String(10), primary_key=True),
        sa.Column("dvla_data", postgresql.JSONB(), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "mot_cache",
        sa.Column("registration", sa.String(10), primary_key=True),
        sa.Column("mot_data", postgresql.JSONB(), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "valuation_cache",
        sa.Column("registration", sa.String(10), primary_key=True),
        sa.Column("webuyanycar", sa.Numeric(10, 2), nullable=True),
        sa.Column("parkers_retail", sa.Numeric(10, 2), nullable=True),
        sa.Column("parkers_private", sa.Numeric(10, 2), nullable=True),
        sa.Column("raw_html", sa.Text(), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "recall_cache",
        sa.Column("registration", sa.String(10), primary_key=True),
        sa.Column("recalls", postgresql.JSONB(), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "vehicle_reports",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("registration", sa.String(10), nullable=False, index=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("risk_summary", postgresql.JSONB(), nullable=True),
        sa.Column("full_report", postgresql.JSONB(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("vehicle_reports")
    op.drop_table("recall_cache")
    op.drop_table("valuation_cache")
    op.drop_table("mot_cache")
    op.drop_table("vehicle_cache")
