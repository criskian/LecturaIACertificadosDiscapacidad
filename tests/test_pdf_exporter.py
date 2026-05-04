from __future__ import annotations

from app.schemas.analysis import CertificateAnalysisSchema
from app.services.html_exporter import HTMLExportService
from app.services.pdf_exporter import PDFExportService


def _build_analysis() -> CertificateAnalysisSchema:
    return CertificateAnalysisSchema.model_validate(
        {
            "persona": {
                "nombre_completo": "Caso Demo",
                "documento": "123",
                "municipio": "Bogota",
                "departamento": "Cundinamarca",
                "fecha_certificacion": "2025-01-15",
                "ips_certificadora": "IPS Demo",
            },
            "discapacidades_activas": ["Fisica"],
            "analisis": {
                "tareas_recomendadas": {
                    "administrativo_oficina": ["Digitacion basica"],
                    "operativo_manual_liviano": ["Empaque liviano"],
                    "relacional_apoyo": ["Atencion al usuario"],
                },
                "ajustes_razonables": [
                    {
                        "titulo": "Pausas activas",
                        "descripcion": "Programar pausas cada 2 horas.",
                        "fundamento": "Dificultad moderada en movilidad.",
                    }
                ],
                "tareas_no_recomendadas": ["Cargue de peso repetitivo"],
                "perfil_funcionamiento": "Mantiene habilidades cognitivas conservadas.",
                "recomendaciones_rrhh_sst": ["Ajustar estacion de trabajo."],
            },
        }
    )


def test_pdf_html_export_uses_print_friendly_sections() -> None:
    analysis = _build_analysis()
    exporter = HTMLExportService()
    html = exporter.render_pdf_document(analysis)
    body = exporter.extract_body_content(html)

    assert "<!DOCTYPE html>" in html
    assert '<meta charset="utf-8"' in html
    assert "<style>" in html
    assert "<body>" in html
    assert "@page {" in html
    assert "body {" in html
    assert ".document {" in html
    assert "@page {" not in body
    assert "body {" not in body
    assert ".document {" not in body
    assert "<h2>Datos generales</h2>" in html
    assert "<h2>Resumen funcional</h2>" in html
    assert "<h2>Habilidades y capacidades</h2>" in html
    assert "<h2>Apoyos requeridos / elementos de apoyo</h2>" in html
    assert "<h2>Tareas recomendadas</h2>" in html
    assert "<h2>Tareas no recomendadas</h2>" in html
    assert "<h2>Ajustes razonables</h2>" in html
    assert "<h2>Observaciones específicas</h2>" in html
    assert "<h2>Recomendaciones para RRHH y SST</h2>" in html
    assert "Nota final:" in html
    assert "Dominios funcionales reportados" not in body


def test_pdf_exporter_reportlab_fallback_does_not_use_css_as_visible_text(monkeypatch) -> None:
    analysis = _build_analysis()
    exporter = PDFExportService()

    monkeypatch.setattr(
        exporter,
        "_render_with_weasyprint",
        lambda html: (_ for _ in ()).throw(OSError("weasy unavailable")),
    )
    monkeypatch.setattr(
        exporter,
        "_render_with_pdfkit",
        lambda html: (_ for _ in ()).throw(OSError("pdfkit unavailable")),
    )

    pdf_bytes = exporter.render(analysis)

    assert pdf_bytes.startswith(b"%PDF")
