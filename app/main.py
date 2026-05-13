from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analyses import router as analyses_router
from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.core.logging import logger, setup_logging

setup_logging()
settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Iniciando %s v%s", settings.app_name, settings.app_version)
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Backend para analisis de certificados de discapacidad en Colombia "
            "y generacion de un informe laboral estructurado."
        ),
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_origin_regex=settings.cors_allow_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health_router)
    application.include_router(analyses_router, prefix=settings.api_v1_prefix)
    return application


app = create_app()
