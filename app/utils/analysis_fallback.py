from __future__ import annotations

from typing import Any


def is_analysis_empty(payload: dict[str, Any]) -> bool:
    analisis = payload.get("analisis")
    if not isinstance(analisis, dict):
        return True

    tareas = analisis.get("tareas_recomendadas")
    admin = _safe_list((tareas or {}).get("administrativo_oficina"))
    operativo = _safe_list((tareas or {}).get("operativo_manual_liviano"))
    relacional = _safe_list((tareas or {}).get("relacional_apoyo"))
    tareas_no = _safe_list(analisis.get("tareas_no_recomendadas"))
    recomendaciones = _safe_list(analisis.get("recomendaciones_rrhh_sst"))
    perfil = str(analisis.get("perfil_funcionamiento") or "").strip()
    ajustes = analisis.get("ajustes_razonables")

    ajustes_validos = 0
    if isinstance(ajustes, list):
        for item in ajustes:
            if not isinstance(item, dict):
                continue
            titulo = str(item.get("titulo") or "").strip()
            descripcion = str(item.get("descripcion") or "").strip()
            fundamento = str(item.get("fundamento") or "").strip()
            if titulo and descripcion and fundamento:
                ajustes_validos += 1

    useful_recommended = len(admin) + len(operativo) + len(relacional)

    if useful_recommended == 0:
        return True
    if not perfil:
        return True
    if len(tareas_no) == 0:
        return True
    if len(recomendaciones) == 0:
        return True
    if ajustes_validos == 0:
        return True

    return False


def fallback_build_analysis(payload: dict[str, Any]) -> dict[str, Any]:
    discapacidades_activas = _safe_list(payload.get("discapacidades_activas"))
    dominios = payload.get("dominios") if isinstance(payload.get("dominios"), dict) else {}

    cognicion = _safe_float(dominios.get("cognicion"))
    movilidad = _safe_float(dominios.get("movilidad"))
    cuidado_personal = _safe_float(dominios.get("cuidado_personal"))
    relaciones = _safe_float(dominios.get("relaciones"))
    vida_diaria = _safe_float(dominios.get("vida_diaria"))
    participacion = _safe_float(dominios.get("participacion"))

    administrativo = [
        "Registro y actualización básica de información en sistemas o formatos estandarizados.",
        "Apoyo en organización documental, archivo y clasificación de soportes físicos o digitales.",
    ]
    operativo = [
        "Empaque liviano o alistamiento simple en puesto fijo con tiempos y secuencia definidos.",
        "Verificación visual básica de materiales o productos de baja complejidad y baja exigencia física.",
    ]
    relacional = [
        "Orientación inicial o apoyo al usuario con guiones, protocolos y funciones claramente definidas.",
        "Acompañamiento en actividades de apoyo interno con comunicación estructurada y supervisión accesible.",
    ]
    tareas_no = [
        "Cargue y manipulación repetitiva de peso o tareas con esfuerzo físico sostenido.",
        "Labores con desplazamientos frecuentes, cambios constantes de puesto o recorridos prolongados.",
        "Funciones de alta multitarea, presión continua o exigencia de respuesta simultánea sin apoyos.",
    ]
    ajustes = [
        {
            "titulo": "Inducción y consignas claras",
            "descripcion": "Entregar instrucciones concretas, por pasos y con criterios de logro verificables para facilitar el desempeño inicial.",
            "fundamento": "Medida conservadora útil cuando hay necesidad de estructuración de tareas o adaptación del proceso de aprendizaje.",
        },
        {
            "titulo": "Pausas y organización del puesto",
            "descripcion": "Programar pausas breves y mantener un puesto estable, ordenado y con elementos de trabajo al alcance.",
            "fundamento": "Reduce sobrecarga física y mejora continuidad operativa cuando existen restricciones de movilidad o participación.",
        },
    ]
    recomendaciones = [
        "Realizar inducción al cargo con funciones priorizadas, tiempos realistas y seguimiento durante el periodo inicial.",
        "Definir ajustes razonables documentados entre RRHH, SST y liderazgo directo, con revisión periódica.",
        "Promover comunicación clara, metas observables y retroalimentación breve para favorecer inclusión y autonomía.",
        "Monitorear exigencias físicas, cognitivas y de interacción del puesto para ajustar la carga de trabajo si es necesario.",
    ]

    if movilidad >= 50:
        operativo = [
            "Alistamiento liviano en estación fija con herramientas a la mano y mínima necesidad de desplazamiento.",
            "Apoyo en control básico de inventario o revisión simple de materiales desde un puesto estable.",
        ]
        tareas_no.extend(
            [
                "Desplazamientos continuos en planta, mensajería interna o recorridos operativos extensos.",
                "Trabajo en alturas, superficies inestables o actividades que exijan cambios posturales frecuentes.",
            ]
        )
        ajustes.append(
            {
                "titulo": "Puesto fijo y apoyo ergonómico",
                "descripcion": "Ubicar a la persona en un puesto estable con ayudas ergonómicas, distancias cortas y acceso fácil a insumos.",
                "fundamento": "La movilidad moderada o alta sugiere reducir traslados, sobreesfuerzo y exigencia postural.",
            }
        )
        recomendaciones.append(
            "Evitar asignaciones que dependan de desplazamientos frecuentes y priorizar puestos con estabilidad espacial."
        )

    if cognicion >= 50:
        administrativo = [
            "Digitación o registro de datos en formatos simples con validación previa y pasos definidos.",
            "Actualización de bases de apoyo o listados cuando exista estructura, secuencia y supervisión inicial.",
        ]
        relacional = [
            "Apoyo a usuarios en interacciones breves con guion o protocolo previamente establecido.",
            "Funciones de enlace interno con mensajes claros, tareas acotadas y seguimiento cercano al inicio.",
        ]
        tareas_no.extend(
            [
                "Toma de decisiones críticas en solitario o manejo simultáneo de múltiples frentes complejos.",
                "Cargos con alta exigencia de priorización dinámica, respuesta inmediata y autonomía total desde el inicio.",
            ]
        )
        ajustes.append(
            {
                "titulo": "Estructuración de tareas y supervisión inicial",
                "descripcion": "Organizar actividades por pasos, con apoyos visuales, secuencia estable y acompañamiento inicial para consolidar rutina.",
                "fundamento": "La presencia de dificultad cognitiva moderada o alta aconseja tareas estructuradas y curva de adaptación guiada.",
            }
        )
        recomendaciones.append(
            "Asignar funciones con instrucciones paso a paso y validar comprensión antes de incrementar complejidad o autonomía."
        )

    if cuidado_personal <= 25:
        recomendaciones.append(
            "Reconocer la buena autonomía en autocuidado y favorecer roles que aprovechen esa capacidad preservada dentro de un entorno inclusivo."
        )

    if relaciones >= 40:
        relacional = [
            "Apoyo relacional en contextos previsibles, con roles claros, tiempos definidos y bajo nivel de ambigüedad social.",
            "Acompañamiento al usuario o al equipo en funciones de soporte con interacción guiada y canales claros de comunicación.",
        ]
        tareas_no.append(
            "Mediación de conflictos complejos o roles con exigencia constante de negociación social ambigua."
        )
        ajustes.append(
            {
                "titulo": "Entorno relacional estructurado",
                "descripcion": "Definir funciones, interlocutores y protocolos de interacción para reducir ambigüedad y facilitar adaptación social.",
                "fundamento": "Las dificultades en relaciones sugieren mayor claridad de rol y contextos de interacción previsibles.",
            }
        )

    if participacion >= 45:
        tareas_no.extend(
            [
                "Roles totalmente autónomos sin apoyos, cambios frecuentes de prioridad o coordinación simultánea de múltiples demandas.",
                "Funciones de alta exposición externa con requerimientos variables y poca estructura operativa.",
            ]
        )
        recomendaciones.append(
            "Evitar multitarea compleja y privilegiar funciones con prioridades visibles, secuencia estable y soporte de seguimiento."
        )

    if vida_diaria >= 50:
        ajustes.append(
            {
                "titulo": "Flexibilización operativa",
                "descripcion": "Organizar horarios, tiempos de ejecución y distribución de tareas de manera gradual para sostener desempeño funcional.",
                "fundamento": "Una afectación relevante en vida diaria sugiere administrar cargas y tiempos de trabajo con mayor previsibilidad.",
            }
        )

    administrativo = _dedupe(administrativo)[:3]
    operativo = _dedupe(operativo)[:3]
    relacional = _dedupe(relacional)[:3]
    tareas_no = _dedupe(tareas_no)[:6]
    recomendaciones = _dedupe(recomendaciones)[:6]
    ajustes = _dedupe_adjustments(ajustes)[:4]

    discapacidades_texto = ", ".join(discapacidades_activas) if discapacidades_activas else "sin categorías activas claramente legibles"
    perfil = (
        f"La persona presenta un perfil funcional que requiere lectura conservadora del certificado, "
        f"con categorías activas reportadas como {discapacidades_texto}. "
        f"Los puntajes sugieren mayor atención en cognición={cognicion:.2f}, movilidad={movilidad:.2f}, "
        f"relaciones={relaciones:.2f} y participación={participacion:.2f}. "
        f"Se recomiendan funciones estructuradas, con demandas previsibles, ajustes razonables y acompañamiento inicial. "
        f"También se reconoce la necesidad de evitar conclusiones absolutas y priorizar inclusión, adaptación del puesto y aprovechamiento de capacidades preservadas."
    )

    return {
        "tareas_recomendadas": {
            "administrativo_oficina": administrativo,
            "operativo_manual_liviano": operativo,
            "relacional_apoyo": relacional,
        },
        "ajustes_razonables": ajustes,
        "tareas_no_recomendadas": tareas_no,
        "perfil_funcionamiento": perfil,
        "recomendaciones_rrhh_sst": recomendaciones,
    }


def _safe_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _safe_float(value: Any) -> float:
    try:
        if value is None or value == "":
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item.strip())
    return result


def _dedupe_adjustments(items: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    result: list[dict[str, str]] = []
    for item in items:
        titulo = str(item.get("titulo") or "").strip()
        descripcion = str(item.get("descripcion") or "").strip()
        fundamento = str(item.get("fundamento") or "").strip()
        if not titulo or not descripcion or not fundamento:
            continue
        key = titulo.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(
            {
                "titulo": titulo,
                "descripcion": descripcion,
                "fundamento": fundamento,
            }
        )
    return result
