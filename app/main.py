from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analyses import router as analyses_router
from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.core.logging import logger, setup_logging

setup_logging()
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Backend para análisis de certificados de discapacidad en Colombia "
        "y generación de un informe laboral estructurado."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(analyses_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Iniciando %s v%s", settings.app_name, settings.app_version)
