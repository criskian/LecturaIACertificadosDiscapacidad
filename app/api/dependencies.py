from __future__ import annotations

from app.services.analysis_pipeline import CertificateAnalysisPipeline, get_analysis_pipeline
from app.services.file_service import FileService
from app.services.html_exporter import HTMLExportService, get_html_export_service
from app.services.storage import InMemoryAnalysisStorage, get_storage


def get_file_service() -> FileService:
    return FileService()


def get_pipeline() -> CertificateAnalysisPipeline:
    return get_analysis_pipeline()


def get_analysis_storage() -> InMemoryAnalysisStorage:
    return get_storage()


def get_export_service() -> HTMLExportService:
    return get_html_export_service()
