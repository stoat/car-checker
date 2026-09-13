# Car Checker

A vehicle provenance checker for UK-registered cars. Enter a number plate and
get back MOT history, a maintenance risk assessment, mileage consistency
checks, an indicative valuation, and any outstanding safety recalls — all in
one report.

## What it does

Given a registration plate, the backend fans out to several data sources in
parallel and combines the results into a single report:

- **Vehicle details** — make, colour, fuel type, engine size, tax/MOT status,
  CO2 emissions — from the [DVLA Vehicle Enquiry Service](https://developer-portal.driver-vehicle-licensing.api.gov.uk/).
- **MOT history** — full test history, pass/fail results, and defects — from
  the [DVSA MOT History API](https://documentation.history.mot.api.gov.uk/).
- **Maintenance risk analysis** — MOT defects are classified into categories
  (tyres, brakes, suspension, rust/corrosion, lights, emissions, structural)
  and checked for recurring issues across test cycles, producing an overall
  low/medium/high risk rating (`backend/app/services/mot_analysis.py`).
- **Mileage consistency** — odometer readings across MOT tests are checked
  for decreases (possible clocking) or implausible jumps.
- **Valuation** — an indicative trade-in price scraped from WeBuyAnyCar.
- **Recalls** — outstanding manufacturer safety recalls scraped from
  gov.uk's vehicle recall checker.

Reports are cached in Postgres per registration with a configurable TTL, so
repeat lookups are served instantly instead of re-hitting external APIs.

If API keys aren't configured, the backend transparently falls back to
realistic mock data (a sample 2018 Ford Focus) so the app is fully
exercisable in development without any credentials.

## Architecture

- **`backend/`** — FastAPI + SQLAlchemy (async) + Postgres, with Alembic
  migrations. Single endpoint: `GET /api/vehicles/{registration}`.
- **`frontend/`** — Next.js (App Router) + React + Tailwind, with React
  Query for data fetching. UK-plate-styled search box on the homepage, full
  report view at `/vehicle/[reg]`.
- **`docker-compose.yml`** — runs Postgres, backend, and frontend together
  for local development.

## Running locally

Requires Docker and Docker Compose.

```bash
cp .env.example .env
# optionally fill in DVLA/DVSA API keys — the app works with mock data without them
docker compose up
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000 (health check at `/health`)

Database migrations run automatically on backend startup
(`backend/entrypoint.sh` runs `alembic upgrade head` before starting uvicorn).

### API keys

- **DVLA VES**: register at the
  [DVLA developer portal](https://developer-portal.driver-vehicle-licensing.api.gov.uk/)
  for `DVLA_API_KEY`.
- **DVSA MOT History**: register at the
  [DVSA API docs](https://documentation.history.mot.api.gov.uk/) for
  `DVSA_API_KEY`, `DVSA_CLIENT_ID`, `DVSA_CLIENT_SECRET`, and the OAuth2
  token URL.

Without these, `dvla_service` and `dvsa_service` return mock data instead of
calling the real APIs.

## Notes

- The valuation and recall lookups work by scraping WeBuyAnyCar and gov.uk
  respectively (there's no public API for either), using Playwright and
  BeautifulSoup. Both fall back to mock data if the scrape fails or
  Playwright isn't installed. Check each site's Terms of Service before
  relying on this in anything beyond personal/development use.
- This project is for personal research use only — it is not a substitute
  for an official vehicle history check.
