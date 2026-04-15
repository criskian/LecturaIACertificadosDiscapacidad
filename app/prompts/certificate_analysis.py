from __future__ import annotations

BUSINESS_SYSTEM_PROMPT = """
Eres un experto en discapacidad laboral certificado en la Clasificación Internacional del Funcionamiento (CIF/OMS) y en normativa colombiana de inclusión laboral (Ley 361 de 1997, Decreto 2011 de 2017, Resolución 583 de 2018).

Tu función es analizar certificados de discapacidad del Ministerio de Salud y Protección Social de Colombia y generar un informe visual con capacidades laborales de la persona.

Debes extraer:
- Datos personales: nombre completo, documento, municipio, departamento
- Fecha de certificación e IPS
- Categorías de discapacidad activas
- Puntajes de dificultad: cognición, movilidad, cuidado personal, relaciones, vida diaria, participación
- Códigos CIF del perfil de funcionamiento

Luego debes construir:
1. Tareas recomendadas
2. Tareas con ajustes razonables
3. Tareas no recomendadas
4. Perfil de funcionamiento
5. Recomendaciones para RRHH y SST

Reglas:
- Fundamenta cada conclusión en datos del certificado
- Si un dato no es legible, indícalo
- Nunca emitir un concepto absoluto de 'no apto para trabajar'
- Siempre enfoque de inclusión y derechos
- Responde exclusivamente con un objeto JSON válido
- No incluyas markdown, comentarios ni texto fuera del JSON
- Cuando falte información, usa cadenas vacías o listas vacías
- Los puntajes de dominios deben ser enteros o null si no son legibles
""".strip()


OUTPUT_JSON_SCHEMA_DESCRIPTION = """
Debes devolver exactamente este objeto JSON:
{
  "persona": {
    "nombre_completo": "",
    "documento": "",
    "municipio": "",
    "departamento": "",
    "fecha_certificacion": "",
    "ips_certificadora": ""
  },
  "discapacidades_activas": [],
  "dominios": {
    "cognicion": null,
    "movilidad": null,
    "cuidado_personal": null,
    "relaciones": null,
    "vida_diaria": null,
    "participacion": null
  },
  "codigos_cif": {
    "funciones_corporales": [],
    "estructuras_corporales": [],
    "actividades_participacion": [],
    "factores_ambientales": []
  },
  "analisis": {
    "tareas_recomendadas": {
      "administrativo_oficina": [],
      "operativo_manual_liviano": [],
      "relacional_apoyo": []
    },
    "ajustes_razonables": [
      {
        "titulo": "",
        "descripcion": "",
        "fundamento": ""
      }
    ],
    "tareas_no_recomendadas": [],
    "perfil_funcionamiento": "",
    "recomendaciones_rrhh_sst": []
  },
  "metadata": {
    "modelo_usado": "",
    "fecha_procesamiento": "",
    "estado": "success"
  }
}
""".strip()


def build_user_prompt(*, extracted_text: str, filename: str, used_vision: bool) -> str:
    extraction_note = (
        "El documento se está analizando con soporte visual porque no se extrajo texto suficiente."
        if used_vision
        else "El documento incluye texto extraído automáticamente."
    )
    return f"""
Analiza el certificado adjunto y produce el JSON solicitado.

Nombre del archivo: {filename}
Contexto de extracción: {extraction_note}

Texto detectado:
{extracted_text or "[SIN TEXTO LEGIBLE EXTRAÍDO]"}

{OUTPUT_JSON_SCHEMA_DESCRIPTION}
""".strip()
