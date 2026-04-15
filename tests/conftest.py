from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_analysis_storage, get_pipeline
from app.main import app
from app.schemas.analysis import CertificateAnalysisSchema
from app.services.storage import InMemoryAnalysisStorage


class DummyPipeline:
    async def analyze(self, payload):  # noqa: ANN001
        return CertificateAnalysisSchema.model_validate(
            {
                "persona": {
                    "nombre_completo": "Ana Perez",
                    "documento": "123456789",
                    "municipio": "Bogota",
                    "departamento": "Cundinamarca",
                    "fecha_certificacion": "2025-01-15",
                    "ips_certificadora": "IPS Demo",
                },
                "discapacidades_raw": [
                    {"nombre": "Física", "marcado": "SI"},
                    {"nombre": "Visual", "marcado": "NO"},
                    {"nombre": "Auditiva", "marcado": "NO"},
                    {"nombre": "Intelectual", "marcado": "NO"},
                    {"nombre": "Psicosocial", "marcado": "NO"},
                    {"nombre": "Sordoceguera", "marcado": "NO"},
                    {"nombre": "Múltiple", "marcado": "NO"},
                ],
                "discapacidades_activas": ["Física"],
                "discapacidades_activas": ["Discapacidad física"],
                "dominios": {
                    "cognicion": 20,
                    "movilidad": 45,
                    "cuidado_personal": 10,
                    "relaciones": 15,
                    "vida_diaria": 30,
                    "participacion": 25,
                },
                "codigos_cif": {
                    "funciones_corporales": ["b730"],
                    "estructuras_corporales": [],
                    "actividades_participacion": ["d450"],
                    "factores_ambientales": ["e150"],
                },
                "analisis": {
                    "tareas_recomendadas": {
                        "administrativo_oficina": ["Digitación básica"],
                        "operativo_manual_liviano": ["Empaque liviano"],
                        "relacional_apoyo": ["Atención al usuario"],
                    },
                    "ajustes_razonables": [
                        {
                            "titulo": "Pausas activas",
                            "descripcion": "Programar pausas cada 2 horas.",
                            "fundamento": "Dificultad moderada en movilidad.",
                        }
                    ],
                    "tareas_no_recomendadas": ["Cargue de peso repetitivo"],
                    "perfil_funcionamiento": "Mantiene habilidades cognitivas conservadas con limitación motora moderada.",
                    "recomendaciones_rrhh_sst": [
                        "Ajustar estación de trabajo.",
                        "Hacer seguimiento de ergonomía.",
                    ],
                },
                "metadata": {
                    "modelo_usado": "test-model",
                    "fecha_procesamiento": "2026-04-15T00:00:00Z",
                    "estado": "success",
                },
            }
        )


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    storage = InMemoryAnalysisStorage()
    app.dependency_overrides[get_pipeline] = lambda: DummyPipeline()
    app.dependency_overrides[get_analysis_storage] = lambda: storage
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
