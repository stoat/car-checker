"""
Simple DB-backed cache layer for the unified report.
We store the full JSON report in vehicle_reports so repeat requests within
the TTL are served instantly without hitting external APIs.
"""
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.report import VehicleReport as VehicleReportModel
from app.schemas.report import VehicleReport

logger = logging.getLogger(__name__)

REPORT_TTL = timedelta(seconds=settings.vehicle_cache_ttl)


async def get_cached_report(db: AsyncSession, registration: str) -> VehicleReport | None:
    result = await db.execute(
        select(VehicleReportModel)
        .where(VehicleReportModel.registration == registration)
        .order_by(VehicleReportModel.generated_at.desc())
        .limit(1)
    )
    row = result.scalar_one_or_none()
    if row is None:
        return None

    age = datetime.now(timezone.utc) - row.generated_at.replace(tzinfo=timezone.utc)
    if age > REPORT_TTL:
        logger.debug("Cached report for %s is stale (%s old)", registration, age)
        return None

    try:
        return VehicleReport.model_validate(row.full_report)
    except Exception as exc:
        logger.warning("Failed to deserialise cached report: %s", exc)
        return None


async def save_report(db: AsyncSession, registration: str, report: VehicleReport) -> None:
    try:
        row = VehicleReportModel(
            registration=registration,
            risk_summary=report.risk_analysis.model_dump() if report.risk_analysis else None,
            full_report=report.model_dump(),
        )
        db.add(row)
        await db.commit()
    except Exception as exc:
        logger.warning("Failed to save report for %s: %s", registration, exc)
        await db.rollback()
