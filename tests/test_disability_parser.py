from __future__ import annotations

from app.utils.disability_parser import parse_disability_table


def test_parse_disability_table_marks_only_auditiva_as_active() -> None:
    payload = {
        "discapacidades_tabla": [
            {"nombre": "Física", "si": False, "no": True, "columna_marcada": "NO"},
            {"nombre": "Visual", "si": False, "no": True, "columna_marcada": "NO"},
            {"nombre": "Auditiva", "si": True, "no": False, "columna_marcada": "SI"},
            {"nombre": "Intelectual", "si": False, "no": True, "columna_marcada": "NO"},
            {"nombre": "Psicosocial", "si": False, "no": True, "columna_marcada": "NO"},
            {"nombre": "Sordoceguera", "si": False, "no": True, "columna_marcada": "NO"},
            {"nombre": "Múltiple", "si": False, "no": True, "columna_marcada": "NO"},
        ]
    }

    result = parse_disability_table(payload)

    assert result.discapacidades_activas == ["Auditiva"]
    assert result.discapacidades_raw == [
        {"nombre": "Física", "marcado": "NO"},
        {"nombre": "Visual", "marcado": "NO"},
        {"nombre": "Auditiva", "marcado": "SI"},
        {"nombre": "Intelectual", "marcado": "NO"},
        {"nombre": "Psicosocial", "marcado": "NO"},
        {"nombre": "Sordoceguera", "marcado": "NO"},
        {"nombre": "Múltiple", "marcado": "NO"},
    ]
