from __future__ import annotations

from app.utils.analysis_guardrails import normalize_analysis_for_certificate


def test_auditiva_only_guardrails_keep_certificate_as_source_of_truth() -> None:
    payload = {
        "discapacidades_raw": [
            {"nombre": "FÃ­sica", "marcado": "NO"},
            {"nombre": "Visual", "marcado": "NO"},
            {"nombre": "Auditiva", "marcado": "SI"},
            {"nombre": "Intelectual", "marcado": "NO"},
            {"nombre": "Psicosocial", "marcado": "NO"},
            {"nombre": "Sordoceguera", "marcado": "NO"},
            {"nombre": "MÃºltiple", "marcado": "NO"},
        ],
        "discapacidades_activas": ["Auditiva"],
        "dominios": {
            "cognicion": 0,
            "movilidad": 0,
            "cuidado_personal": 0,
            "relaciones": 20,
            "vida_diaria": 0,
            "participacion": 34.38,
        },
        "analisis": {
            "tareas_recomendadas": {
                "administrativo_oficina": ["Digitacion con seguimiento escrito."],
                "operativo_manual_liviano": ["Evitar operaciones manuales pesadas."],
                "relacional_apoyo": ["Atencion telefonica directa."],
            },
            "ajustes_razonables": [
                {
                    "titulo": "Pausas por limitacion motora",
                    "descripcion": "Reducir esfuerzo fisico.",
                    "fundamento": "Discapacidad fisica.",
                }
            ],
            "tareas_no_recomendadas": [
                "Manipulacion de cargas.",
                "Atencion telefonica sin apoyo.",
            ],
            "perfil_funcionamiento": "La persona presenta discapacidad fisica y auditiva.",
            "recomendaciones_rrhh_sst": [
                "Evitar movilidad intensa.",
                "Usar instrucciones visuales.",
            ],
        },
    }

    normalized = normalize_analysis_for_certificate(
        payload,
        used_vision=False,
        observations="Usa audifono y puede comunicarse oralmente.",
    )
    serialized = str(normalized).lower()

    assert "discapacidad fisica" not in serialized
    assert "manipulacion de cargas" not in serialized
    assert "movilidad intensa" not in serialized
    assert "participacion presenta dificultad moderada" in serialized
    assert "incorporacion gradual" in serialized or "participacion gradual" in serialized
    assert "audifono" in serialized
    assert "no depender exclusivamente de llamadas" in serialized
    assert any(
        "escritas" in item.lower() or "visual" in item.lower()
        for item in normalized["recomendaciones_rrhh_sst"]
    )
    assert any(
        "telefon" in item.lower() or "alarma" in item.lower()
        for item in normalized["tareas_no_recomendadas"]
    )
