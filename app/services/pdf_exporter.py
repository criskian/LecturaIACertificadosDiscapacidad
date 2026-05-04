from __future__ import annotations

from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer

from app.schemas.analysis import CertificateAnalysisSchema
from app.services.html_exporter import HTMLExportService, get_html_export_service


class PDFExportService:
    def __init__(self, html_exporter: HTMLExportService | None = None) -> None:
        self.html_exporter = html_exporter or get_html_export_service()

    def render(self, analysis: CertificateAnalysisSchema) -> bytes:
        html = self.html_exporter.render_pdf_document(analysis)

        try:
            return self._render_with_weasyprint(html)
        except (ImportError, OSError):
            try:
                return self._render_with_pdfkit(html)
            except (ImportError, OSError):
                return self._render_with_reportlab_fallback(analysis)

    def _render_with_weasyprint(self, html: str) -> bytes:
        from weasyprint import HTML

        return HTML(string=html).write_pdf()

    def _render_with_pdfkit(self, html: str) -> bytes:
        import pdfkit

        configuration = pdfkit.configuration()
        return pdfkit.from_string(
            html,
            False,
            configuration=configuration,
            options={"quiet": ""},
        )

    def _render_with_reportlab_fallback(
        self, analysis: CertificateAnalysisSchema
    ) -> bytes:
        buffer = BytesIO()
        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=1.8 * cm,
            rightMargin=1.8 * cm,
            topMargin=1.6 * cm,
            bottomMargin=1.6 * cm,
            title="Informe laboral inclusivo",
        )
        styles = getSampleStyleSheet()
        title = styles["Heading1"]
        heading = styles["Heading2"]
        body = styles["BodyText"]
        sections = self.html_exporter.pdf_sections(analysis)

        story = [Paragraph("Informe laboral inclusivo", title), Spacer(1, 0.2 * cm)]
        story.append(
            Paragraph(
                "Documento generado a partir del análisis del certificado de discapacidad.",
                body,
            )
        )
        story.append(Spacer(1, 0.2 * cm))
        for section in sections:
            story.append(Paragraph(str(section["title"]), heading))
            if section["kind"] == "paragraph":
                story.append(Paragraph(str(section.get("text") or "Sin información."), body))
            else:
                items = [
                    str(item)
                    for item in (section.get("items") or ["Sin información."])
                    if str(item).strip()
                ]
                story.append(
                    ListFlowable(
                        [
                            ListItem(Paragraph(item, body), leftIndent=8)
                            for item in items
                        ],
                        bulletType="bullet",
                        leftIndent=14,
                    )
                )
            story.append(Spacer(1, 0.15 * cm))

        story.append(
            Paragraph(
                "Nota final: Este informe es una orientación laboral basada en la información disponible del certificado y debe complementarse con criterio humano y validación profesional.",
                body,
            )
        )

        document.build(story)
        return buffer.getvalue()


def get_pdf_export_service() -> PDFExportService:
    return PDFExportService()
