from __future__ import annotations

SYSTEM_PROMPT = """
Eres un experto en discapacidad laboral certificado en la Clasificación Internacional del Funcionamiento (CIF/OMS)
y en normativa colombiana de inclusión laboral (Ley 361 de 1997, Decreto 2011 de 2017, Resolución 583 de 2018).

Tu función es analizar certificados de discapacidad del Ministerio de Salud y Protección Social de Colombia y devolver
EXCLUSIVAMENTE un JSON válido, sin markdown, sin comentarios y sin texto adicional.

REGLAS GENERALES:
- Fundamenta todo en el certificado.
- Si se adjunta formulario u observaciones, úsalos solo para complementar, precisar o contextualizar el análisis del certificado.
- Prioriza siempre el certificado como fuente principal; usa formulario y observaciones como evidencia adicional.
- Si algo no se lee, deja cadena vacía o usa "ILEGIBLE" según aplique.
- No emitas "no apto para trabajar".
- Usa enfoque de inclusión, capacidades preservadas y ajustes razonables.
- Identifica capacidades conservadas y reflejalas claramente en `perfil_funcionamiento`, `tareas_recomendadas`, `tareas_no_recomendadas` y `ajustes_razonables`.
- Si aparecen apoyos técnicos o funcionales como silla de ruedas, bastón, caminador, audífonos, implante coclear u otros, incorpóralos de forma explícita en el análisis narrativo y en las recomendaciones.
- No uses porcentaje de discapacidad como eje principal del resultado, aunque aparezca en el material de entrada.
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
- Si la evidencia es limitada, construye recomendaciones conservadoras basadas en dominios, discapacidades activas, capacidades preservadas y apoyos identificados.
- Solo deja una lista vacía cuando realmente no aplique, y evita strings vacíos.
- Haz que `perfil_funcionamiento` mencione, cuando exista evidencia, capacidades conservadas, restricciones funcionales, apoyos técnicos y necesidades de comunicación o movilidad.
- Haz que `tareas_recomendadas` y `tareas_no_recomendadas` sean específicas al contexto funcional y no genéricas.
- Haz que `ajustes_razonables` sean precisos, accionables y coherentes con certificado, formulario y observaciones.
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


def build_user_prompt(
    *,
    extracted_text: str,
    filename: str,
    used_vision: bool,
    form_text: str | None = None,
    observations: str | None = None,
) -> str:
    extraction_note = (
        "El documento se analiza con soporte visual porque el texto extraído es insuficiente o el certificado está escaneado."
        if used_vision
        else "El documento incluye texto extraído automáticamente y también puede apoyarse en la imagen adjunta."
    )
    form_section = (
        f"""

Texto complementario del formulario o entrevista:
{form_text}
""".rstrip()
        if form_text
        else """

Texto complementario del formulario o entrevista:
[NO SE ADJUNTO FORMULARIO O NO FUE POSIBLE EXTRAER TEXTO LEGIBLE]
""".rstrip()
    )
    observations_section = (
        f"""

Observaciones adicionales del evaluador o reclutador:
{observations}
""".rstrip()
        if observations
        else """

Observaciones adicionales del evaluador o reclutador:
[SIN OBSERVACIONES ADICIONALES]
""".rstrip()
    )
    return f"""
Analiza el certificado adjunto y produce el JSON solicitado.

Nombre del archivo: {filename}
Contexto de extracción: {extraction_note}

IMPORTANTE:
- Realiza una lectura general del documento completo.
- Extrae los datos personales, dominios, códigos CIF y análisis laboral.
- Si existe formulario o entrevista, úsalo para enriquecer el análisis funcional y laboral sin contradecir el certificado salvo que la observación adicional aclare una capacidad conservada o una necesidad de apoyo.
- Si existen observaciones adicionales, intégralas en el razonamiento para precisar apoyos técnicos, capacidades conservadas, restricciones funcionales y ajustes razonables.
- En `discapacidades_raw`, si no estás seguro de una fila, usa `ILEGIBLE`.
- No agregues categorías fuera de la lista esperada.
- El bloque `analisis` debe venir completo, útil y listo para mostrarse en interfaz.
- No centres el resultado en porcentajes; centra el resultado en funcionamiento, capacidades, tareas, apoyos y ajustes.
- Si la evidencia del certificado es limitada, construye recomendaciones prudentes basadas en dominios, discapacidades activas, capacidades conservadas, formulario y observaciones, sin dejar vacíos.

Texto detectado:
{extracted_text or "[SIN TEXTO LEGIBLE EXTRAÍDO]"}

{form_section}

{observations_section}

{OUTPUT_JSON_SCHEMA_DESCRIPTION}
""".strip()
