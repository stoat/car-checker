from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class VehicleReport(Base):
    __tablename__ = "vehicle_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    registration: Mapped[str] = mapped_column(String(10), index=True, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    risk_summary: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    full_report: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
