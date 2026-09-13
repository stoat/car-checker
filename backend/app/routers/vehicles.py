import asyncio
import logging
import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.schemas.report import VehicleReport
from app.services import dvla_service, dvsa_service, mot_analysis, valuation_service, recall_service
from app.services.cache import get_cached_report, save_report

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])

PLATE_RE = re.compile(r"^[A-Z0-9]{2,7}$")


def normalise_plate(plate: str) -> str:
    return plate.upper().replace(" ", "")


@router.get("/{registration}", response_model=VehicleReport)
async def get_vehicle_report(registration: str, db: AsyncSession = Depends(get_db)):
    reg = normalise_plate(registration)

    if not PLATE_RE.match(reg):
        raise HTTPException(status_code=422, detail="Invalid registration plate format")

    # Check for a recent cached full report
    cached = await get_cached_report(db, reg)
    if cached:
        return cached

    is_mock = (
        not settings.dvla_api_key or settings.dvla_api_key == "your_dvla_api_key_here"
    )
    errors: dict[str, str] = {}
    if is_mock:
        errors["_mock"] = "API keys not configured — showing sample data"

    # Fan out to all data sources in parallel
    dvla_task = asyncio.create_task(dvla_service.fetch(reg))
    dvsa_task = asyncio.create_task(dvsa_service.fetch(reg))
    valuation_task = asyncio.create_task(valuation_service.fetch(reg))
    recall_task = asyncio.create_task(recall_service.fetch(reg))

    dvla_data, dvsa_data, valuation_data, recall_data = await asyncio.gather(
        dvla_task, dvsa_task, valuation_task, recall_task, return_exceptions=True
    )

    if isinstance(dvla_data, Exception):
        logger.warning("DVLA fetch failed for %s: %s", reg, dvla_data)
        errors["dvla"] = str(dvla_data)
        dvla_data = None

    if isinstance(dvsa_data, Exception):
        logger.warning("DVSA fetch failed for %s: %s", reg, dvsa_data)
        errors["dvsa"] = str(dvsa_data)
        dvsa_data = None

    if isinstance(valuation_data, Exception):
        logger.warning("Valuation fetch failed for %s: %s", reg, valuation_data)
        errors["valuation"] = str(valuation_data)
        valuation_data = None

    if isinstance(recall_data, Exception):
        logger.warning("Recall fetch failed for %s: %s", reg, recall_data)
        errors["recalls"] = str(recall_data)
        recall_data = []

    # Parse MOT history
    mot_tests = dvsa_service.parse_mot_tests(dvsa_data) if dvsa_data else []
    vehicle_details = dvla_service.parse_vehicle(dvla_data, reg) if dvla_data else None

    # Run analysis
    risk_analysis = mot_analysis.analyse(mot_tests) if mot_tests else None
    mileage_consistency = mot_analysis.check_mileage(mot_tests) if mot_tests else None

    report = VehicleReport(
        registration=reg,
        vehicle=vehicle_details,
        mot_history=mot_tests,
        risk_analysis=risk_analysis,
        mileage_consistency=mileage_consistency,
        valuation=valuation_data,
        recalls=recall_data or [],
        errors=errors,
    )

    await save_report(db, reg, report)
    return report
