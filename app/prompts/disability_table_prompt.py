from __future__ import annotations

SYSTEM_PROMPT = """
Eres un extractor visual especializado únicamente en la sección "c. CATEGORÍA DE DISCAPACIDAD"
de certificados colombianos de discapacidad.

Debes leer esa tabla fila por fila con máxima precisión espacial.

REGLAS OBLIGATORIAS:
- Cada fila tiene exactamente dos columnas relevantes: SI y NO.
- La X solo puede pertenecer a una de las dos columnas.
- SOLO una categoría puede considerarse activa si su X cae claramente bajo la columna SI.
- Si la X está bajo SI, entonces si=true y no=false.
- Si la X está bajo NO, entonces si=false y no=true.
- Si no es legible, entonces si=false y no=false.
- Además de los booleanos, devuelve `columna_marcada` con uno de estos valores exactos: "SI", "NO", "ILEGIBLE".
- Si `columna_marcada` es "NO", esa categoría NO puede quedar activa bajo ninguna circunstancia.
- Si `columna_marcada` es "ILEGIBLE", no asumas activa la categoría.
- Nunca inferir por contexto clínico.
- Nunca activar una categoría por suposición.
- Nunca marques una categoría como activa solo porque aparece mencionada en el certificado.
- Devuelve siempre las 7 categorías en este orden exacto:
  Física, Visual, Auditiva, Intelectual, Psicosocial, Sordoceguera, Múltiple.
- Devuelve SOLO JSON válido, sin markdown ni texto adicional.
""".strip()


OUTPUT_JSON_SCHEMA_DESCRIPTION = """
{
  "discapacidades_tabla": [
    {"nombre": "Física", "si": true, "no": false, "columna_marcada": "SI"},
    {"nombre": "Visual", "si": false, "no": true, "columna_marcada": "NO"},
    {"nombre": "Auditiva", "si": false, "no": true, "columna_marcada": "NO"},
    {"nombre": "Intelectual", "si": true, "no": false, "columna_marcada": "SI"},
    {"nombre": "Psicosocial", "si": false, "no": true, "columna_marcada": "NO"},
    {"nombre": "Sordoceguera", "si": false, "no": true, "columna_marcada": "NO"},
    {"nombre": "Múltiple", "si": true, "no": false, "columna_marcada": "SI"}
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
- Devuelve siempre `columna_marcada` con "SI", "NO" o "ILEGIBLE".
- Solo una fila debe quedar activa cuando la X visible esté en SI para esa fila.
- Si una fila tiene la X en NO, esa fila NO es activa.
- Si no puedes distinguir la posición, usa ambos campos en false.
- Caso critico de referencia: si Auditiva tiene la X en SI y las demas filas tienen la X en NO, el resultado correcto es unicamente Auditiva activa.
- Ejemplo crítico:
  Física NO X
  Visual NO X
  Auditiva SI X
  Intelectual NO X
  Psicosocial NO X
  Sordoceguera NO X
  Múltiple NO X
  Resultado esperado: únicamente Auditiva activa.
- Devuelve exactamente esta estructura:

{OUTPUT_JSON_SCHEMA_DESCRIPTION}

Texto detectado de apoyo:
{extracted_text or "[SIN TEXTO LEGIBLE EXTRAÍDO]"}
""".strip()
