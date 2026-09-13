from datetime import datetime, timezone

from sqlalchemy import DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class VehicleCache(Base):
    __tablename__ = "vehicle_cache"

    registration: Mapped[str] = mapped_column(String(10), primary_key=True)
    dvla_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class MotCache(Base):
    __tablename__ = "mot_cache"

    registration: Mapped[str] = mapped_column(String(10), primary_key=True)
    mot_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ValuationCache(Base):
    __tablename__ = "valuation_cache"

    registration: Mapped[str] = mapped_column(String(10), primary_key=True)
    webuyanycar: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    parkers_retail: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    parkers_private: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    raw_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RecallCache(Base):
    __tablename__ = "recall_cache"

    registration: Mapped[str] = mapped_column(String(10), primary_key=True)
    recalls: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
