"""
DVSA MOT History API integration.
Docs: https://documentation.history.mot.api.gov.uk/
Auth: OAuth2 client credentials (MS Entra ID) + x-api-key header.
"""
import logging
import time
from typing import Any

import httpx

from app.config import settings
from app.schemas.report import MotDefect, MotTest

logger = logging.getLogger(__name__)

# In-memory token cache — sufficient for single-process dev; replace with Redis for multi-worker
_token_cache: dict[str, Any] = {"access_token": None, "expires_at": 0}


async def _get_access_token() -> str:
    """Fetch or return cached OAuth2 access token from MS Entra ID."""
    now = time.time()
    if _token_cache["access_token"] and now < _token_cache["expires_at"] - 30:
        return _token_cache["access_token"]

    logger.info(f"Requesting DVSA token with scope: {settings.dvsa_scope}")
    logger.info(f"Token URL: {settings.dvsa_token_url}")
    logger.info(f"Client ID: {settings.dvsa_client_id}")
    
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.post(
                settings.dvsa_token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": settings.dvsa_client_id,
                    "client_secret": settings.dvsa_client_secret,
                    "scope": settings.dvsa_scope,
                },
            )
            logger.info(f"Token response status: {response.status_code}")
            if response.status_code != 200:
                logger.warning(f"Token request failed with {response.status_code}: {response.text}")
            response.raise_for_status()
            token_data = response.json()
        except Exception as e:
            logger.error(f"Token request error: {e}")
            raise

    _token_cache["access_token"] = token_data["access_token"]
    _token_cache["expires_at"] = now + token_data.get("expires_in", 3600)
    logger.info("DVSA OAuth token refreshed")
    return _token_cache["access_token"]


def _is_mock_mode() -> bool:
    return not settings.dvsa_api_key or settings.dvsa_api_key == "your_dvsa_api_key_here"


async def fetch(registration: str) -> dict:
    """Fetch MOT history from DVSA API, or return mock data in dev."""
    if _is_mock_mode():
        logger.info("DVSA_API_KEY not set — returning mock data for %s", registration)
        from app.services.mock_data import DVSA_MOCK
        return {**DVSA_MOCK, "registration": registration}

    access_token = await _get_access_token()
    url = settings.dvsa_mot_url.format(registration=registration)

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(
            url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "x-api-key": settings.dvsa_api_key,
                "Accept": "application/json",
            },
        )
        response.raise_for_status()
        return response.json()


def parse_mot_tests(data: dict) -> list[MotTest]:
    """
    Parse raw DVSA response into a list of MotTest objects.

    The DVSA API returns a single vehicle object (or list of one) with a
    `motTests` array. Each test has `rfrAndComments` for defects.
    """
    # API may return a list (bulk) or a single object
    if isinstance(data, list):
        vehicle = data[0] if data else {}
    else:
        vehicle = data

    raw_tests = vehicle.get("motTests", [])
    tests: list[MotTest] = []

    for raw in raw_tests:
        defects = [
            MotDefect(
                text=d.get("text", ""),
                type=d.get("type", "ADVISORY"),
                dangerous=d.get("dangerous", False),
            )
            for d in raw.get("rfrAndComments", [])
        ]

        odometer = raw.get("odometerValue")
        tests.append(
            MotTest(
                completed_date=raw.get("completedDate", ""),
                test_result=raw.get("testResult", ""),
                expiry_date=raw.get("expiryDate"),
                odometer_value=int(odometer) if odometer and str(odometer).isdigit() else None,
                odometer_unit=raw.get("odometerUnit"),
                mot_test_number=raw.get("motTestNumber"),
                defects=defects,
            )
        )

    return tests
