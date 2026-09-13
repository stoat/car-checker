import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import vehicles

logging.basicConfig(level=settings.log_level)

app = FastAPI(
    title="Car Checker API",
    description="Vehicle provenance checker using DVLA/DVSA data",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(vehicles.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
