from __future__ import annotations

SYSTEM_PROMPT = """
Eres un extractor visual especializado únicamente en la sección "c. CATEGORÍA DE DISCAPACIDAD"
de certificados colombianos de discapacidad.

Debes leer esa tabla fila por fila con máxima precisión espacial.

REGLAS OBLIGATORIAS:
- Cada fila tiene exactamente dos columnas relevantes: SI y NO.
- La X solo puede pertenecer a una de las dos columnas.
- Si la X está bajo SI, entonces si=true y no=false.
- Si la X está bajo NO, entonces si=false y no=true.
- Si no es legible, entonces si=false y no=false.
- Nunca inferir por contexto clínico.
- Nunca activar una categoría por suposición.
- Devuelve siempre las 7 categorías en este orden:
  Física, Visual, Auditiva, Intelectual, Psicosocial, Sordoceguera, Múltiple.
- Devuelve SOLO JSON válido, sin markdown ni texto adicional.
""".strip()


OUTPUT_JSON_SCHEMA_DESCRIPTION = """
{
  "discapacidades_tabla": [
    {"nombre": "Física", "si": true, "no": false},
    {"nombre": "Visual", "si": false, "no": true},
    {"nombre": "Auditiva", "si": false, "no": true},
    {"nombre": "Intelectual", "si": true, "no": false},
    {"nombre": "Psicosocial", "si": false, "no": true},
    {"nombre": "Sordoceguera", "si": false, "no": true},
    {"nombre": "Múltiple", "si": true, "no": false}
  ]
}
""".strip()


def build_user_prompt(*, extracted_text: str, filename: str, used_vision: bool) -> str:
    extraction_note = (
        "El documento está siendo analizado visualmente porque la tabla puede estar en un certificado escaneado."
        if used_vision
        else "Puedes apoyarte en el texto extraído, pero prioriza la geometría visual de la tabla."
    )
    return f"""
Lee exclusivamente la tabla de la sección "c. CATEGORÍA DE DISCAPACIDAD".

Nombre del archivo: {filename}
Contexto de extracción: {extraction_note}

Instrucciones:
- Ignora el resto del certificado.
- Determina para cada fila si la X cae en SI o en NO.
- Si no puedes distinguir la posición, usa ambos campos en false.
- Devuelve exactamente esta estructura:

{OUTPUT_JSON_SCHEMA_DESCRIPTION}

Texto detectado de apoyo:
{extracted_text or "[SIN TEXTO LEGIBLE EXTRAÍDO]"}
""".strip()
