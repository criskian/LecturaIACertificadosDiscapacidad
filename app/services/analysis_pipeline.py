from __future__ import annotations

from app.core.logging import logger
from app.schemas.analysis import CertificateAnalysisSchema
from app.schemas.document import DocumentPayload, OpenAIAnalysisRequest
from app.services.file_service import FileService
from app.services.openai_service import OpenAIAnalysisService


class CertificateAnalysisPipeline:
    def __init__(
        self,
        file_service: FileService,
        openai_service: OpenAIAnalysisService,
    ) -> None:
        self.file_service = file_service
        self.openai_service = openai_service

    async def analyze(self, payload: DocumentPayload) -> CertificateAnalysisSchema:
        extracted = self.file_service.extract_document_content(payload)
        logger.info(
            "Documento procesado. source_type=%s page_count=%s used_vision=%s",
            extracted.source_type,
            extracted.page_count,
            extracted.used_vision,
        )
        request = OpenAIAnalysisRequest(
            text=extracted.extracted_text,
            image_data_urls=extracted.image_data_urls,
            filename=payload.filename,
            content_type=payload.content_type,
        )
        return await self.openai_service.analyze_certificate(
            request,
            used_vision=extracted.used_vision,
        )


def get_analysis_pipeline() -> CertificateAnalysisPipeline:
    return CertificateAnalysisPipeline(
        file_service=FileService(),
        openai_service=OpenAIAnalysisService(),
    )
