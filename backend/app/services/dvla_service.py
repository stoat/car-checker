"""
DVLA Vehicle Enquiry Service (VES) integration.
Docs: https://developer-portal.driver-vehicle-licensing.api.gov.uk/
"""
import logging

import httpx

from app.config import settings
from app.schemas.report import VehicleDetails

logger = logging.getLogger(__name__)

_HEADERS = {
    "x-api-key": settings.dvla_api_key,
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def _is_mock_mode() -> bool:
    return not settings.dvla_api_key or settings.dvla_api_key == "your_dvla_api_key_here"


async def fetch(registration: str) -> dict:
    """Fetch raw vehicle data from DVLA VES API, or return mock data in dev."""
    if _is_mock_mode():
        logger.info("DVLA_API_KEY not set — returning mock data for %s", registration)
        from app.services.mock_data import DVLA_MOCK
        return {**DVLA_MOCK, "registrationNumber": registration}

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            settings.dvla_ves_url,
            headers=_HEADERS,
            json={"registrationNumber": registration},
        )
        response.raise_for_status()
        return response.json()


def parse_vehicle(data: dict, registration: str) -> VehicleDetails:
    """Map DVLA VES response to VehicleDetails schema."""
    return VehicleDetails(
        registration=registration,
        make=data.get("make"),
        colour=data.get("colour"),
        fuel_type=data.get("fuelType"),
        engine_capacity=data.get("engineCapacity"),
        year_of_manufacture=data.get("yearOfManufacture"),
        tax_status=data.get("taxStatus"),
        mot_status=data.get("motStatus"),
        co2_emissions=data.get("co2Emissions"),
        date_of_last_v5c_issued=data.get("dateOfLastV5CIssued"),
        # DVLA VES does not return model — DVSA MOT history does
        model=None,
    )
