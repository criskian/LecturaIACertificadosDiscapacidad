from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from app.schemas.analysis import CertificateAnalysisSchema

_ESTADOS = {"success", "error", "processing"}
_MARCADOS = {"SI", "NO", "ILEGIBLE"}


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _clamped_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    return min(max(score, 0.0), 100.0)


def _clean(payload: dict[str, Any]) -> dict[str, Any]:
    """Repara los campos que suelen romper la validación en análisis guardados por
    clientes (historial viejo, texto normalizado para mostrar). Nunca inventa
    contenido: lo que no se puede leer queda vacío."""
    analisis = _dict(payload.get("analisis"))
    tareas = _dict(analisis.get("tareas_recomendadas"))
    metadata = _dict(payload.get("metadata"))

    return {
        **payload,
        "persona": {
            key: value
            for key, value in _dict(payload.get("persona")).items()
            if isinstance(value, str)
        },
        "discapacidades_raw": [
            item
            for item in payload.get("discapacidades_raw") or []
            if isinstance(item, dict)
            and isinstance(item.get("nombre"), str)
            and item.get("marcado") in _MARCADOS
        ],
        "discapacidades_activas": _string_list(payload.get("discapacidades_activas")),
        "dominios": {
            key: _clamped_score(value) for key, value in _dict(payload.get("dominios")).items()
        },
        "codigos_cif": {
            key: _string_list(value) for key, value in _dict(payload.get("codigos_cif")).items()
        },
        "analisis": {
            "tareas_recomendadas": {
                key: _string_list(value) for key, value in tareas.items()
            },
            "ajustes_razonables": [
                {
                    "titulo": str(item.get("titulo") or ""),
                    "descripcion": str(item.get("descripcion") or ""),
                    "fundamento": str(item.get("fundamento") or ""),
                }
                for item in analisis.get("ajustes_razonables") or []
                if isinstance(item, dict)
            ],
            "tareas_no_recomendadas": _string_list(analisis.get("tareas_no_recomendadas")),
            "perfil_funcionamiento": str(analisis.get("perfil_funcionamiento") or ""),
            "recomendaciones_rrhh_sst": _string_list(analisis.get("recomendaciones_rrhh_sst")),
        },
        "metadata": {
            "modelo_usado": str(metadata.get("modelo_usado") or ""),
            "estado": metadata.get("estado") if metadata.get("estado") in _ESTADOS else "success",
        },
    }


def coerce_saved_analysis(payload: dict[str, Any]) -> CertificateAnalysisSchema:
    try:
        return CertificateAnalysisSchema.model_validate(payload)
    except ValidationError:
        return CertificateAnalysisSchema.model_validate(_clean(payload))
