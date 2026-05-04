from __future__ import annotations

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from app.schemas.analysis import CertificateAnalysisSchema

ALL_CATEGORIES = (
    "Física",
    "Visual",
    "Auditiva",
    "Intelectual",
    "Psicosocial",
    "Sordoceguera",
    "Múltiple",
)

CATEGORY_KEYWORDS = {
    "Física": (
        "física",
        "fisica",
        "movilidad",
        "motora",
        "motor",
        "desplaz",
        "postural",
        "carga",
        "cargue",
        "peso",
        "esfuerzo físico",
        "trabajo en alturas",
        "alturas",
        "limitación motora",
    ),
    "Visual": ("visual", "visión", "vision", "ceguera", "baja visión"),
    "Auditiva": ("auditiva", "audición", "audicion", "hipoacusia", "sordera"),
    "Intelectual": ("intelectual",),
    "Psicosocial": ("psicosocial",),
    "Sordoceguera": ("sordoceguera",),
    "Múltiple": ("múltiple", "multiple"),
}

CATEGORY_GUIDANCE = {
    "Auditiva": {
        "summary": (
            "La persona presenta una condición auditiva identificada en el certificado. "
            "El análisis debe enfocarse en apoyos de comunicación, instrucciones claras, "
            "confirmación de comprensión, reducción de ruido y ajustes razonables relacionados con la comunicación."
        ),
        "capabilities": [
            "Puede desempeñarse en funciones con instrucciones claras, secuencias definidas y confirmación de comprensión.",
            "Puede aportar en tareas administrativas, documentales, de soporte o atención estructurada cuando existan canales de comunicación accesibles.",
            "Puede desarrollar actividades laborales si el entorno garantiza comunicación comprensible, coordinación clara y ajustes razonables apropiados.",
        ],
        "supports": [
            "Confirmación de comprensión de instrucciones clave mediante lenguaje claro, apoyos escritos o recapitulación breve.",
            "Reducción de ruido ambiental y priorización de espacios de trabajo con comunicación más nítida.",
            "Uso de apoyos de comunicación o tecnología auditiva cuando existan y hayan sido validados por la persona y el equipo responsable.",
        ],
        "not_recommended": [
            "Tareas que dependan exclusivamente de instrucciones orales en ambientes con ruido alto y sin mecanismos de confirmación.",
            "Funciones con comunicación crítica en tiempo real sin apoyos accesibles, sin redundancia escrita o sin validación de comprensión.",
        ],
        "observations": [
            "Conviene validar desde el ingreso cuáles apoyos de comunicación facilitan mejor el desempeño seguro y autónomo.",
            "No se identifican otras categorías de discapacidad activas en la tabla del certificado.",
        ],
    }
}


class PDFExportService:
    def render(self, analysis: CertificateAnalysisSchema) -> bytes:
        buffer = BytesIO()
        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2.2 * cm,
            rightMargin=2.2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
            title="Informe laboral inclusivo",
            author="Lectura IA Certificados Discapacidad",
            pageCompression=0,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=22,
            textColor=colors.black,
            alignment=TA_LEFT,
            spaceAfter=10,
        )
        section_style = ParagraphStyle(
            "SectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.black,
            spaceBefore=10,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#2f2f2f"),
            spaceAfter=4,
        )
        note_style = ParagraphStyle(
            "Note",
            parent=body_style,
            fontName="Helvetica-Oblique",
            textColor=colors.HexColor("#4a4a4a"),
            spaceBefore=8,
        )

        active_categories = self._active_categories(analysis)

        story = [
            Paragraph("Informe laboral inclusivo", title_style),
            Paragraph(
                "Documento de orientación para empresas, RRHH y SST basado en la información disponible del proceso de análisis.",
                body_style,
            ),
            Spacer(1, 0.2 * cm),
        ]

        story.extend(
            self._section(
                "Datos generales",
                self._general_data_items(analysis, active_categories),
                section_style,
                body_style,
            )
        )
        story.extend(
            self._paragraph_section(
                "Resumen funcional",
                self._build_functional_summary(analysis, active_categories),
                section_style,
                body_style,
            )
        )
        story.extend(
            self._section(
                "Habilidades y capacidades",
                self._capabilities_items(analysis, active_categories),
                section_style,
                body_style,
            )
        )
        story.extend(
            self._section(
                "Apoyos requeridos / elementos de apoyo",
                self._support_items(analysis, active_categories),
                section_style,
                body_style,
            )
        )
        story.extend(
            self._section(
                "Tareas recomendadas",
                self._recommended_items(analysis, active_categories),
                section_style,
                body_style,
            )
        )
        story.extend(
            self._section(
                "Tareas no recomendadas",
                self._not_recommended_items(analysis, active_categories),
                section_style,
                body_style,
            )
        )
        story.extend(
            self._section(
                "Ajustes razonables",
                self._adjustment_items(analysis, active_categories),
                section_style,
                body_style,
            )
        )
        story.extend(
            self._section(
                "Observaciones específicas",
                self._observation_items(analysis, active_categories),
                section_style,
                body_style,
            )
        )
        story.extend(
            self._section(
                "Recomendaciones para RRHH y SST",
                self._rrhh_items(analysis, active_categories),
                section_style,
                body_style,
            )
        )
        story.append(
            Paragraph(
                "Este informe es una orientación laboral basada en la información disponible del certificado, formulario y observaciones. Debe complementarse con criterio humano y validación de profesionales responsables.",
                note_style,
            )
        )

        document.build(story)
        return buffer.getvalue()

    def _section(
        self,
        title: str,
        items: list[str],
        section_style: ParagraphStyle,
        body_style: ParagraphStyle,
    ) -> list:
        return [
            Paragraph(title, section_style),
            self._bullet_list(items, body_style),
        ]

    def _paragraph_section(
        self,
        title: str,
        text: str,
        section_style: ParagraphStyle,
        body_style: ParagraphStyle,
    ) -> list:
        return [
            Paragraph(title, section_style),
            Paragraph(self._sanitize(text), body_style),
        ]

    def _bullet_list(
        self, items: list[str], body_style: ParagraphStyle
    ) -> ListFlowable:
        return ListFlowable(
            [
                ListItem(Paragraph(self._sanitize(item), body_style), leftIndent=8)
                for item in items
            ],
            bulletType="bullet",
            leftIndent=14,
            bulletFontName="Helvetica",
            bulletFontSize=9,
            bulletColor=colors.black,
        )

    def _active_categories(self, analysis: CertificateAnalysisSchema) -> list[str]:
        active = [item for item in analysis.discapacidades_activas if item in ALL_CATEGORIES]
        return active

    def _general_data_items(
        self, analysis: CertificateAnalysisSchema, active_categories: list[str]
    ) -> list[str]:
        persona = analysis.persona
        active_disabilities = (
            ", ".join(active_categories)
            if active_categories
            else "No fue posible identificar categorías activas legibles."
        )
        generated_at = analysis.metadata.fecha_procesamiento
        generated_label = (
            generated_at.strftime("%Y-%m-%d %H:%M UTC")
            if generated_at is not None
            else "Fecha no disponible"
        )

        items = [
            f"Nombre de la persona: {persona.nombre_completo or 'No disponible'}",
            f"Tipo(s) de discapacidad identificados: {active_disabilities}",
            f"Fecha de generación: {generated_label}",
        ]
        if persona.documento:
            items.append(f"Documento de referencia: {persona.documento}")
        return items

    def _build_functional_summary(
        self, analysis: CertificateAnalysisSchema, active_categories: list[str]
    ) -> str:
        if active_categories == ["Auditiva"]:
            return (
                "La persona presenta una condición auditiva identificada en el certificado. "
                "El análisis debe enfocarse en apoyos de comunicación, instrucciones claras, "
                "reducción de ruido, confirmación de comprensión y ajustes razonables relacionados con la comunicación. "
                "No se identifican otras categorías de discapacidad activas en la tabla del certificado."
            )

        category_clauses = [
            CATEGORY_GUIDANCE[category]["summary"]
            for category in active_categories
            if category in CATEGORY_GUIDANCE
        ]
        if category_clauses:
            summary = " ".join(category_clauses)
            if len(active_categories) == 1:
                summary += " No se identifican otras categorías de discapacidad activas en la tabla del certificado."
            return summary

        safe_profile = self._filter_contradictory_sentences(
            self._split_sentences(analysis.analisis.perfil_funcionamiento),
            active_categories,
        )
        if safe_profile:
            return " ".join(safe_profile)

        if active_categories:
            return (
                f"La persona presenta la(s) categoría(s) activa(s) {', '.join(active_categories)} identificada(s) en la tabla del certificado. "
                "El análisis debe centrarse en capacidades funcionales, apoyos requeridos y ajustes razonables consistentes con esas categorías confirmadas."
            )

        return (
            "No fue posible confirmar categorías activas de discapacidad con lectura suficiente de la tabla del certificado. "
            "El informe se mantiene en clave conservadora y debe validarse con criterio humano y profesional."
        )

    def _capabilities_items(
        self, analysis: CertificateAnalysisSchema, active_categories: list[str]
    ) -> list[str]:
        items: list[str] = []
        for category in active_categories:
            guidance = CATEGORY_GUIDANCE.get(category, {})
            items.extend(guidance.get("capabilities", []))

        if not items:
            tasks = analysis.analisis.tareas_recomendadas
            items.extend(
                [
                    f"Capacidad funcional asociada a tareas administrativas o de oficina: {item}"
                    for item in tasks.administrativo_oficina
                ]
            )
            items.extend(
                [
                    f"Capacidad funcional asociada a tareas de apoyo relacional: {item}"
                    for item in tasks.relacional_apoyo
                ]
            )

        items = self._filter_items_by_inactive_categories(items, active_categories)
        return self._fallback_items(
            items,
            "Se recomienda tomar las tareas recomendadas y los ajustes razonables como referencia principal de capacidades observables, evitando inferir condiciones no confirmadas.",
        )

    def _support_items(
        self, analysis: CertificateAnalysisSchema, active_categories: list[str]
    ) -> list[str]:
        items = [
            f"{adjustment.titulo}: {adjustment.descripcion}"
            for adjustment in analysis.analisis.ajustes_razonables
        ]
        items = self._filter_items_by_inactive_categories(items, active_categories)

        if not items:
            for category in active_categories:
                items.extend(CATEGORY_GUIDANCE.get(category, {}).get("supports", []))

        return self._fallback_items(
            items,
            "No se identificaron apoyos estructurados en el análisis actual. Cualquier ayuda técnica o ajuste debe validarse con la persona y el equipo responsable.",
        )

    def _recommended_items(
        self, analysis: CertificateAnalysisSchema, active_categories: list[str]
    ) -> list[str]:
        tasks = analysis.analisis.tareas_recomendadas
        items = (
            [f"Administrativo / oficina: {item}" for item in tasks.administrativo_oficina]
            + [
                f"Operativo / manual liviano: {item}"
                for item in tasks.operativo_manual_liviano
            ]
            + [f"Relacional / apoyo: {item}" for item in tasks.relacional_apoyo]
        )
        items = self._filter_items_by_inactive_categories(items, active_categories)
        return self._fallback_items(
            items,
            "No se registraron tareas recomendadas específicas coherentes con las categorías activas confirmadas.",
        )

    def _not_recommended_items(
        self, analysis: CertificateAnalysisSchema, active_categories: list[str]
    ) -> list[str]:
        items = self._filter_items_by_inactive_categories(
            analysis.analisis.tareas_no_recomendadas,
            active_categories,
        )

        if not items:
            for category in active_categories:
                items.extend(CATEGORY_GUIDANCE.get(category, {}).get("not_recommended", []))

        return self._fallback_items(
            items,
            "No se registraron tareas no recomendadas específicas consistentes con las categorías activas confirmadas.",
        )

    def _adjustment_items(
        self, analysis: CertificateAnalysisSchema, active_categories: list[str]
    ) -> list[str]:
        items = [
            f"{adjustment.titulo}: {adjustment.descripcion}. Fundamento: {adjustment.fundamento}"
            for adjustment in analysis.analisis.ajustes_razonables
        ]
        items = self._filter_items_by_inactive_categories(items, active_categories)

        if not items:
            for category in active_categories:
                items.extend(CATEGORY_GUIDANCE.get(category, {}).get("supports", []))

        return self._fallback_items(
            items,
            "No se registraron ajustes razonables específicos consistentes con las categorías activas confirmadas.",
        )

    def _observation_items(
        self, analysis: CertificateAnalysisSchema, active_categories: list[str]
    ) -> list[str]:
        items = self._filter_contradictory_sentences(
            self._split_sentences(analysis.analisis.perfil_funcionamiento),
            active_categories,
        )

        if not items:
            for category in active_categories:
                items.extend(CATEGORY_GUIDANCE.get(category, {}).get("observations", []))

        return self._fallback_items(
            items,
            "No se registraron observaciones específicas coherentes con las categorías activas confirmadas.",
        )

    def _rrhh_items(
        self, analysis: CertificateAnalysisSchema, active_categories: list[str]
    ) -> list[str]:
        items = self._filter_items_by_inactive_categories(
            analysis.analisis.recomendaciones_rrhh_sst,
            active_categories,
        )
        return self._fallback_items(
            items,
            "Se recomienda validar con RRHH y SST los apoyos de comunicación, adaptación del puesto y mecanismos de seguimiento consistentes con las categorías activas confirmadas.",
        )

    def _filter_items_by_inactive_categories(
        self, items: list[str], active_categories: list[str]
    ) -> list[str]:
        return [
            item.strip()
            for item in items
            if item and item.strip() and self._text_matches_active_categories(item, active_categories)
        ]

    def _filter_contradictory_sentences(
        self, items: list[str], active_categories: list[str]
    ) -> list[str]:
        return [
            item
            for item in items
            if self._text_matches_active_categories(item, active_categories)
        ]

    def _text_matches_active_categories(
        self, text: str, active_categories: list[str]
    ) -> bool:
        lowered = text.lower()
        inactive_categories = [
            category for category in ALL_CATEGORIES if category not in active_categories
        ]

        for category in inactive_categories:
            for keyword in CATEGORY_KEYWORDS.get(category, ()):
                if keyword in lowered:
                    return False
        return True

    def _split_sentences(self, text: str) -> list[str]:
        normalized = text.replace("\n", " ").strip()
        if not normalized:
            return []
        return [
            sentence.strip(" .")
            for sentence in normalized.split(".")
            if sentence.strip(" .")
        ]

    def _fallback_items(self, items: list[str], fallback: str) -> list[str]:
        cleaned = [item.strip() for item in items if item and item.strip()]
        return cleaned or [fallback]

    def _sanitize(self, value: str) -> str:
        return (
            value.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )


def get_pdf_export_service() -> PDFExportService:
    return PDFExportService()
