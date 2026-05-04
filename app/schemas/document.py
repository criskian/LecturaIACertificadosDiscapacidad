from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class DocumentPayload(BaseModel):
    filename: str
    content_type: str
    size_bytes: int
    raw_bytes: bytes = Field(repr=False)


class ExtractedDocumentContent(BaseModel):
    extracted_text: str = ""
    image_data_urls: list[str] = Field(default_factory=list)
    source_type: str
    page_count: int = 1
    used_vision: bool = False


class OpenAIAnalysisRequest(BaseModel):
    text: str = ""
    image_data_urls: list[str] = Field(default_factory=list)
    filename: str
    content_type: str
    observations: Optional[str] = None
    form_text: Optional[str] = None
