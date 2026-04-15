from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from typing import Protocol
from uuid import uuid4

from app.models.analysis_record import AnalysisRecord
from app.schemas.analysis import CertificateAnalysisSchema


class AnalysisStorage(Protocol):
    def create(
        self,
        *,
        filename: str,
        content_type: str,
        size_bytes: int,
        source_bytes: bytes,
        analysis: CertificateAnalysisSchema,
    ) -> AnalysisRecord: ...

    def get(self, analysis_id: str) -> AnalysisRecord | None: ...

    def update_analysis(
        self, analysis_id: str, analysis: CertificateAnalysisSchema
    ) -> AnalysisRecord | None: ...


class InMemoryAnalysisStorage:
    def __init__(self) -> None:
        self._records: dict[str, AnalysisRecord] = {}
        self._lock = Lock()

    def create(
        self,
        *,
        filename: str,
        content_type: str,
        size_bytes: int,
        source_bytes: bytes,
        analysis: CertificateAnalysisSchema,
    ) -> AnalysisRecord:
        record = AnalysisRecord(
            id=str(uuid4()),
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
            source_bytes=source_bytes,
            analysis=analysis,
        )
        with self._lock:
            self._records[record.id] = record
        return record

    def get(self, analysis_id: str) -> AnalysisRecord | None:
        with self._lock:
            return self._records.get(analysis_id)

    def update_analysis(
        self, analysis_id: str, analysis: CertificateAnalysisSchema
    ) -> AnalysisRecord | None:
        with self._lock:
            record = self._records.get(analysis_id)
            if not record:
                return None
            record.analysis = analysis
            record.updated_at = datetime.now(timezone.utc)
            self._records[analysis_id] = record
            return record


storage = InMemoryAnalysisStorage()


def get_storage() -> InMemoryAnalysisStorage:
    return storage
