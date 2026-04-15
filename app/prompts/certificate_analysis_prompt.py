from __future__ import annotations

SYSTEM_PROMPT = """
Eres un experto en discapacidad laboral certificado en la Clasificación Internacional del Funcionamiento (CIF/OMS)
y en normativa colombiana de inclusión laboral (Ley 361 de 1997, Decreto 2011 de 2017, Resolución 583 de 2018).

Tu función es analizar certificados de discapacidad del Ministerio de Salud y Protección Social de Colombia y devolver
EXCLUSIVAMENTE un JSON válido, sin markdown, sin comentarios y sin texto adicional.

REGLAS GENERALES:
- Fundamenta todo en el certificado.
- Si algo no se lee, deja cadena vacía o usa "ILEGIBLE" según aplique.
- No emitas "no apto para trabajar".
- Usa enfoque de inclusión, capacidades preservadas y ajustes razonables.
- Devuelve SOLO JSON.

REGLAS SOBRE CATEGORÍAS DE DISCAPACIDAD:
- Puedes intentar leer la sección de categorías, pero no inventes marcas.
- No infieras categorías activas por contexto clínico.
- Si no es claro, usa "ILEGIBLE".
- El backend aplicará una validación especializada adicional sobre esa tabla.

REGLAS OBLIGATORIAS PARA `analisis`:
- No dejes vacías las secciones de `analisis`.
- Genera mínimo 2 tareas en `administrativo_oficina` si aplica.
- Genera mínimo 2 tareas en `operativo_manual_liviano` si aplica.
- Genera mínimo 2 tareas en `relacional_apoyo` si aplica.
- Genera entre 2 y 4 `ajustes_razonables` reales y concretos.
- Genera entre 3 y 6 `tareas_no_recomendadas`.
- Genera 1 párrafo de `perfil_funcionamiento` de 3 a 5 líneas.
- Genera entre 4 y 6 `recomendaciones_rrhh_sst`.
- Si la evidencia es limitada, construye recomendaciones conservadoras basadas en dominios y discapacidades activas.
- Solo deja una lista vacía cuando realmente no aplique, y evita strings vacíos.
""".strip()


OUTPUT_JSON_SCHEMA_DESCRIPTION = """
ESTRUCTURA OBLIGATORIA DEL JSON:
{
  "persona": {
    "nombre_completo": "",
    "documento": "",
    "municipio": "",
    "departamento": "",
    "fecha_certificacion": "",
    "ips_certificadora": ""
  },
  "discapacidades_raw": [
    {"nombre": "Física", "marcado": "SI"},
    {"nombre": "Visual", "marcado": "NO"},
    {"nombre": "Auditiva", "marcado": "NO"},
    {"nombre": "Intelectual", "marcado": "NO"},
    {"nombre": "Psicosocial", "marcado": "NO"},
    {"nombre": "Sordoceguera", "marcado": "NO"},
    {"nombre": "Múltiple", "marcado": "NO"}
  ],
  "dominios": {
    "cognicion": 0,
    "movilidad": 0,
    "cuidado_personal": 0,
    "relaciones": 0,
    "vida_diaria": 0,
    "participacion": 0
  },
  "codigos_cif": {
    "funciones_corporales": [],
    "estructuras_corporales": [],
    "actividades_participacion": [],
    "factores_ambientales": []
  },
  "analisis": {
    "tareas_recomendadas": {
      "administrativo_oficina": [
        "Ejemplo 1",
        "Ejemplo 2"
      ],
      "operativo_manual_liviano": [
        "Ejemplo 1",
        "Ejemplo 2"
      ],
      "relacional_apoyo": [
        "Ejemplo 1",
        "Ejemplo 2"
      ]
    },
    "ajustes_razonables": [
      {
        "titulo": "Ajuste real",
        "descripcion": "Descripción concreta y útil.",
        "fundamento": "Fundamentado en dominios, categorías activas o información del certificado."
      }
    ],
    "tareas_no_recomendadas": [
      "Ejemplo 1",
      "Ejemplo 2",
      "Ejemplo 3"
    ],
    "perfil_funcionamiento": "Párrafo útil y concreto de 3 a 5 líneas.",
    "recomendaciones_rrhh_sst": [
      "Ejemplo 1",
      "Ejemplo 2",
      "Ejemplo 3",
      "Ejemplo 4"
    ]
  }
}
""".strip()


def build_user_prompt(*, extracted_text: str, filename: str, used_vision: bool) -> str:
    extraction_note = (
        "El documento se analiza con soporte visual porque el texto extraído es insuficiente o el certificado está escaneado."
        if used_vision
        else "El documento incluye texto extraído automáticamente y también puede apoyarse en la imagen adjunta."
    )
    return f"""
Analiza el certificado adjunto y produce el JSON solicitado.

Nombre del archivo: {filename}
Contexto de extracción: {extraction_note}

IMPORTANTE:
- Realiza una lectura general del documento completo.
- Extrae los datos personales, dominios, códigos CIF y análisis laboral.
- En `discapacidades_raw`, si no estás seguro de una fila, usa `ILEGIBLE`.
- No agregues categorías fuera de la lista esperada.
- El bloque `analisis` debe venir completo, útil y listo para mostrarse en interfaz.
- Si la evidencia del certificado es limitada, construye recomendaciones prudentes basadas en dominios y discapacidades activas, sin dejar vacíos.

Texto detectado:
{extracted_text or "[SIN TEXTO LEGIBLE EXTRAÍDO]"}

{OUTPUT_JSON_SCHEMA_DESCRIPTION}
""".strip()
