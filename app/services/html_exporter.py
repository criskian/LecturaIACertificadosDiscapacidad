from __future__ import annotations

from html import escape

from app.schemas.analysis import CertificateAnalysisSchema


class HTMLExportService:
    def render(self, analysis: CertificateAnalysisSchema) -> str:
        persona = analysis.persona
        dominios = analysis.dominios.model_dump()
        analisis = analysis.analisis
        cards = "".join(
            f"<div class='metric'><span>{escape(key.replace('_', ' ').title())}</span><strong>{escape(str(value if value is not None else 'No legible'))}</strong></div>"
            for key, value in dominios.items()
        )
        recommended = "".join(
            f"<li>{escape(item)}</li>"
            for bucket in analisis.tareas_recomendadas.model_dump().values()
            for item in bucket
        ) or "<li>Sin información</li>"
        not_recommended = "".join(
            f"<li>{escape(item)}</li>" for item in analisis.tareas_no_recomendadas
        ) or "<li>Sin información</li>"
        adjustments = "".join(
            (
                f"<li><strong>{escape(item.titulo)}</strong>: "
                f"{escape(item.descripcion)} "
                f"<em>({escape(item.fundamento)})</em></li>"
            )
            for item in analisis.ajustes_razonables
        ) or "<li>Sin información</li>"
        rrhh = "".join(
            f"<li>{escape(item)}</li>" for item in analisis.recomendaciones_rrhh_sst
        ) or "<li>Sin información</li>"

        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Informe laboral de discapacidad</title>
  <style>
    :root {{
      --bg: #f4efe6;
      --surface: #fffaf3;
      --ink: #1f2933;
      --accent: #0f766e;
      --accent-soft: #d9f3ef;
      --warn: #b45309;
      --line: #d9cfc0;
    }}
    body {{ margin: 0; font-family: Georgia, 'Times New Roman', serif; background: linear-gradient(135deg, #f7f2ea, #e7f3f1); color: var(--ink); }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px 20px 60px; }}
    .hero {{ background: var(--surface); border: 1px solid var(--line); border-radius: 24px; padding: 28px; box-shadow: 0 18px 45px rgba(31,41,51,.08); }}
    .hero h1 {{ margin: 0 0 12px; font-size: 2rem; }}
    .sub {{ color: #52606d; margin-bottom: 18px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-top: 24px; }}
    .metric {{ background: var(--accent-soft); padding: 16px; border-radius: 18px; border: 1px solid rgba(15,118,110,.15); }}
    .metric span {{ display: block; font-size: .85rem; color: #365c58; }}
    .metric strong {{ font-size: 1.4rem; }}
    .section {{ margin-top: 22px; background: rgba(255,250,243,.92); border-radius: 20px; border: 1px solid var(--line); padding: 22px; }}
    .section h2 {{ margin: 0 0 10px; }}
    ul {{ padding-left: 20px; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
    .chip {{ background: #e8eef7; color: #1d4d8b; padding: 8px 12px; border-radius: 999px; font-size: .92rem; }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>{escape(persona.nombre_completo or "Persona no identificada")}</h1>
      <div class="sub">Documento: {escape(persona.documento or "No legible")} | Municipio: {escape(persona.municipio or "No legible")} | Departamento: {escape(persona.departamento or "No legible")}</div>
      <div class="sub">Fecha certificación: {escape(persona.fecha_certificacion or "No legible")} | IPS: {escape(persona.ips_certificadora or "No legible")}</div>
      <div class="chips">
        {''.join(f"<span class='chip'>{escape(item)}</span>" for item in analysis.discapacidades_activas) or "<span class='chip'>Sin categorías identificadas</span>"}
      </div>
      <div class="grid">{cards}</div>
    </section>
    <section class="section">
      <h2>Perfil de funcionamiento</h2>
      <p>{escape(analisis.perfil_funcionamiento or "Sin información estructurada.")}</p>
    </section>
    <section class="section">
      <h2>Tareas recomendadas</h2>
      <ul>{recommended}</ul>
    </section>
    <section class="section">
      <h2>Ajustes razonables</h2>
      <ul>{adjustments}</ul>
    </section>
    <section class="section">
      <h2>Tareas no recomendadas</h2>
      <ul>{not_recommended}</ul>
    </section>
    <section class="section">
      <h2>Recomendaciones para RRHH y SST</h2>
      <ul>{rrhh}</ul>
    </section>
  </div>
</body>
</html>
""".strip()


def get_html_export_service() -> HTMLExportService:
    return HTMLExportService()
