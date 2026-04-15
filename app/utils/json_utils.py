from __future__ import annotations

import json


def extract_json_object(raw_text: str) -> dict:
    raw_text = raw_text.strip()
    if not raw_text:
        raise ValueError("La respuesta del modelo llegó vacía.")

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No se encontró un objeto JSON válido en la respuesta.") from None

        candidate = raw_text[start : end + 1]
        return json.loads(candidate)
