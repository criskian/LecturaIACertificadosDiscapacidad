from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.schemas.analysis import CertificateAnalysisSchema


class AnalysisRecord(BaseModel):
    id: str
    filename: str
    content_type: str
    size_bytes: int
    source_bytes: bytes = Field(repr=False)
    analysis: CertificateAnalysisSchema
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
