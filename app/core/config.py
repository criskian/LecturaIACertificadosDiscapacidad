from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    app_name: str = "Lectura IA Certificados Discapacidad"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    openai_model: str = Field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    max_file_size_mb: int = Field(
        default_factory=lambda: int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    )
    storage_backend: str = Field(default_factory=lambda: os.getenv("STORAGE_BACKEND", "memory"))
    allow_origins: list[str] = Field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv(
                "ALLOW_ORIGINS",
                "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173",
            ).split(",")
            if origin.strip()
        ]
    )
    request_timeout_seconds: float = Field(
        default_factory=lambda: float(os.getenv("REQUEST_TIMEOUT_SECONDS", "90"))
    )
    max_pdf_pages_for_vision: int = Field(
        default_factory=lambda: int(os.getenv("MAX_PDF_PAGES_FOR_VISION", "5"))
    )
    max_image_dimension: int = Field(
        default_factory=lambda: int(os.getenv("MAX_IMAGE_DIMENSION", "1600"))
    )
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
