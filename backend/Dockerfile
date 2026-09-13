FROM python:3.12-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright browsers for JS-heavy scraping (non-fatal — falls back to mock data if unavailable)
RUN playwright install chromium --with-deps || echo "Playwright install failed — valuation scraping will use mock data"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

FROM base AS dev
# Dev stage: code is mounted as a volume
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS prod
COPY . .
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
