from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Any, Iterable, Literal

from app.core.logging import logger

CanonicalMark = Literal["SI", "NO", "ILEGIBLE"]

ALLOWED_DISABILITY_CATEGORIES: tuple[str, ...] = (
    "Física",
    "Visual",
    "Auditiva",
    "Intelectual",
    "Psicosocial",
    "Sordoceguera",
    "Múltiple",
)

ALLOWED_MARKS: tuple[CanonicalMark, ...] = ("SI", "NO", "ILEGIBLE")

_CATEGORY_MAP = {
    "FISICA": "Física",
    "VISUAL": "Visual",
    "AUDITIVA": "Auditiva",
    "INTELECTUAL": "Intelectual",
    "PSICOSOCIAL": "Psicosocial",
    "SORDOCEGUERA": "Sordoceguera",
    "MULTIPLE": "Múltiple",
}

_MARK_MAP: dict[str, CanonicalMark] = {
    "SI": "SI",
    "NO": "NO",
    "ILEGIBLE": "ILEGIBLE",
    "ILLEGIBLE": "ILEGIBLE",
    "NO LEGIBLE": "ILEGIBLE",
    "DESCONOCIDO": "ILEGIBLE",
    "INCIERTO": "ILEGIBLE",
}


@dataclass(frozen=True)
class DisabilityProcessingResult:
    discapacidades_raw: list[dict[str, str]]
    discapacidades_activas: list[str]


@dataclass(frozen=True)
class DisabilityTableRow:
    nombre: str
    si: bool
    no: bool


def _strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def normalize_token(value: str) -> str:
    cleaned = " ".join((value or "").strip().split())
    cleaned = _strip_accents(cleaned)
    return cleaned.upper()


def normalize_disability_name(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    return _CATEGORY_MAP.get(normalize_token(value))


def normalize_mark(value: Any) -> CanonicalMark | None:
    if not isinstance(value, str):
        return None
    return _MARK_MAP.get(normalize_token(value))


def _resolve_duplicate(
    category: str, previous_mark: CanonicalMark, new_mark: CanonicalMark
) -> CanonicalMark:
    if previous_mark == new_mark:
        return previous_mark

    logger.warning(
        "Conflicto detectado en discapacidad '%s': %s vs %s. Se marcará como ILEGIBLE.",
        category,
        previous_mark,
        new_mark,
    )
    return "ILEGIBLE"


def clean_disabilities(raw_items: Iterable[dict[str, Any]] | None) -> DisabilityProcessingResult:
    normalized_by_category: dict[str, CanonicalMark] = {}

    for item in raw_items or []:
        if not isinstance(item, dict):
            logger.warning("Se ignoró un elemento de discapacidades_raw por no ser un objeto.")
            continue

        category = normalize_disability_name(item.get("nombre"))
        mark = normalize_mark(item.get("marcado"))

        if not category:
            logger.warning(
                "Se ignoró una categoría de discapacidad no permitida: %r",
                item.get("nombre"),
            )
            continue

        if not mark:
            logger.warning(
                "Se ignoró un marcado no permitido para '%s': %r",
                category,
                item.get("marcado"),
            )
            continue

        existing_mark = normalized_by_category.get(category)
        if existing_mark:
            normalized_by_category[category] = _resolve_duplicate(
                category, existing_mark, mark
            )
        else:
            normalized_by_category[category] = mark

    return _build_processing_result(normalized_by_category)


def parse_disability_table(payload: dict[str, Any] | None) -> DisabilityProcessingResult:
    normalized_by_category: dict[str, CanonicalMark] = {}
    table_rows = payload.get("discapacidades_tabla") if isinstance(payload, dict) else None

    if not isinstance(table_rows, list):
        logger.warning(
            "La extracción especializada de discapacidad no devolvió una lista válida. Se marcarán categorías como ILEGIBLE."
        )
        return _build_processing_result(normalized_by_category)

    for item in table_rows:
        if not isinstance(item, dict):
            logger.warning("Se ignoró una fila de la tabla de discapacidad por no ser un objeto.")
            continue

        category = normalize_disability_name(item.get("nombre"))
        if not category:
            logger.warning(
                "Se ignoró una fila de tabla con categoría no permitida: %r",
                item.get("nombre"),
            )
            continue

        mark = table_row_to_mark(si=item.get("si"), no=item.get("no"))
        existing_mark = normalized_by_category.get(category)
        if existing_mark:
            normalized_by_category[category] = _resolve_duplicate(
                category, existing_mark, mark
            )
        else:
            normalized_by_category[category] = mark

    return _build_processing_result(normalized_by_category)


def table_row_to_mark(*, si: Any, no: Any) -> CanonicalMark:
    is_si = bool(si) if isinstance(si, bool) else False
    is_no = bool(no) if isinstance(no, bool) else False

    if is_si and not is_no:
        return "SI"
    if not is_si and is_no:
        return "NO"
    return "ILEGIBLE"


def discapacidad_tabla_a_raw(payload: dict[str, Any] | None) -> list[dict[str, str]]:
    return parse_disability_table(payload).discapacidades_raw


def _build_processing_result(
    normalized_by_category: dict[str, CanonicalMark],
) -> DisabilityProcessingResult:
    for category in ALLOWED_DISABILITY_CATEGORIES:
        if category not in normalized_by_category:
            normalized_by_category[category] = "ILEGIBLE"
            logger.info(
                "La categoría '%s' faltó en la respuesta del modelo y se completó como ILEGIBLE.",
                category,
            )

    cleaned_raw = [
        {"nombre": category, "marcado": normalized_by_category[category]}
        for category in ALLOWED_DISABILITY_CATEGORIES
    ]
    active = [
        category
        for category in ALLOWED_DISABILITY_CATEGORIES
        if normalized_by_category[category] == "SI"
    ]

    if len(active) > 3:
        logger.warning(
            "Se detectaron %s discapacidades activas en un mismo certificado: %s",
            len(active),
            ", ".join(active),
        )

    return DisabilityProcessingResult(
        discapacidades_raw=cleaned_raw,
        discapacidades_activas=active,
    )
