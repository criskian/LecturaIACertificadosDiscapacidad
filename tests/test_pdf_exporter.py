from __future__ import annotations

from app.schemas.analysis import CertificateAnalysisSchema
from app.services.pdf_exporter import PDFExportService


def test_pdf_exporter_sanitizes_contradictory_physical_mentions_for_auditiva() -> None:
    analysis = CertificateAnalysisSchema.model_validate(
        {
            "persona": {
                "nombre_completo": "Caso Auditivo",
                "documento": "123",
            },
            "discapacidades_raw": [
                {"nombre": "Física", "marcado": "NO"},
                {"nombre": "Visual", "marcado": "NO"},
                {"nombre": "Auditiva", "marcado": "SI"},
                {"nombre": "Intelectual", "marcado": "NO"},
                {"nombre": "Psicosocial", "marcado": "NO"},
                {"nombre": "Sordoceguera", "marcado": "NO"},
                {"nombre": "Múltiple", "marcado": "NO"},
            ],
            "discapacidades_activas": ["Auditiva"],
            "analisis": {
                "tareas_recomendadas": {
                    "administrativo_oficina": ["Gestión documental con instrucciones claras"],
                    "operativo_manual_liviano": ["Apoyo básico de archivo"],
                    "relacional_apoyo": ["Atención estructurada con confirmación escrita"],
                },
                "ajustes_razonables": [
                    {
                        "titulo": "Apoyo de comunicación",
                        "descripcion": "Confirmar instrucciones por escrito y reducir ruido ambiental.",
                        "fundamento": "Condición auditiva confirmada en la tabla del certificado.",
                    }
                ],
                "tareas_no_recomendadas": [
                    "Cargue de peso repetitivo",
                    "Funciones con comunicación crítica en tiempo real sin apoyos accesibles",
                ],
                "perfil_funcionamiento": "La persona presenta discapacidad física y auditiva con limitación motora moderada.",
                "recomendaciones_rrhh_sst": [
                    "Asegurar instrucciones claras y confirmación de comprensión.",
                    "Evitar ambientes con ruido alto sin apoyos de comunicación.",
                ],
            },
        }
    )

    exporter = PDFExportService()

    summary = exporter._build_functional_summary(analysis, ["Auditiva"])
    capabilities = exporter._capabilities_items(analysis, ["Auditiva"])
    not_recommended = exporter._not_recommended_items(analysis, ["Auditiva"])

    assert "física" not in summary.lower()
    assert "motora" not in summary.lower()
    assert "auditiva" in summary.lower()
    assert all("física" not in item.lower() for item in capabilities)
    assert all("motora" not in item.lower() for item in capabilities)
    assert all("cargue de peso" not in item.lower() for item in not_recommended)
