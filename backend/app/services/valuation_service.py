"""
Valuation scraper.

Scrapes WeBuyAnyCar for an instant buy price. Because WeBuyAnyCar uses
JavaScript-rendered pages, we use Playwright (headless Chromium) to fetch
the final DOM, then extract the value with BeautifulSoup.

Note: Always verify compliance with the site's Terms of Service before
running this in production. This scraper is provided for development and
personal research purposes.
"""
from __future__ import annotations

import logging
import re

from bs4 import BeautifulSoup

from app.schemas.report import Valuation

logger = logging.getLogger(__name__)

WBAC_URL = "https://www.webuyanycar.com/car-valuation/"


async def fetch(registration: str) -> Valuation:
    """
    Attempt to scrape WeBuyAnyCar for a valuation.
    Returns mock data if Playwright is unavailable (dev mode).
    """
    try:
        from playwright.async_api import async_playwright  # noqa: F401 — check import works
    except ImportError:
        logger.info("Playwright not available — returning mock valuation for %s", registration)
        from app.services.mock_data import VALUATION_MOCK
        return Valuation(**VALUATION_MOCK)

    try:
        price = await _scrape_wbac(registration)
        return Valuation(
            webuyanycar=price,
            source_note="Scraped from WeBuyAnyCar — indicative trade price only",
        )
    except Exception as exc:
        logger.warning("WeBuyAnyCar scrape failed for %s: %s", registration, exc)
        from app.services.mock_data import VALUATION_MOCK
        return Valuation(**VALUATION_MOCK, source_note=f"Mock data (scrape failed: {exc})")


async def _scrape_wbac(registration: str) -> float | None:
    """
    Use Playwright to navigate the WeBuyAnyCar valuation flow and extract price.

    The flow:
      1. Go to /car-valuation/
      2. Enter registration and mileage (we use 0 as a dummy mileage for the
         purpose of getting a ballpark figure)
      3. Wait for the valuation result page
      4. Parse the price from the page HTML
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        logger.warning("Playwright not installed — valuation scraping unavailable")
        return None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(WBAC_URL, wait_until="networkidle", timeout=30_000)

            # Accept cookies if present
            try:
                await page.click("button:has-text('Accept')", timeout=3000)
            except Exception:
                pass

            # Enter registration plate
            reg_input = page.locator("input[name='vrm'], input[placeholder*='reg'], #vehicleReg")
            await reg_input.fill(registration)

            # Submit / continue
            await page.keyboard.press("Enter")
            await page.wait_for_load_state("networkidle", timeout=15_000)

            html = await page.content()
            return _parse_price(html)
        finally:
            await browser.close()


def _parse_price(html: str) -> float | None:
    """Extract a £ price from rendered HTML."""
    soup = BeautifulSoup(html, "html.parser")

    # Try common price element patterns
    candidates = [
        soup.find(class_=re.compile(r"price|valuation|offer", re.IGNORECASE)),
        soup.find("span", string=re.compile(r"£[\d,]+")),
        soup.find(attrs={"data-testid": re.compile(r"price|valuation")}),
    ]

    for element in candidates:
        if element:
            text = element.get_text()
            match = re.search(r"£([\d,]+)", text)
            if match:
                return float(match.group(1).replace(",", ""))

    # Fallback: search all text for £amount
    full_text = soup.get_text()
    matches = re.findall(r"£([\d,]{3,})", full_text)
    if matches:
        # Take the largest figure that looks like a car price (£500–£100k)
        prices = [float(m.replace(",", "")) for m in matches]
        valid = [p for p in prices if 500 <= p <= 100_000]
        if valid:
            return max(valid)

    return None
