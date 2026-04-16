import type { Analysis } from "../types/analysis";
import { DomainMetricCard } from "./DomainMetricCard";
import { ProfileHeaderCard } from "./ProfileHeaderCard";
import { RecommendedTasksPanel } from "./RecommendedTasksPanel";
import { AdjustmentsPanel } from "./AdjustmentsPanel";
import { NotRecommendedPanel } from "./NotRecommendedPanel";
import { FunctioningProfilePanel } from "./FunctioningProfilePanel";
import { HrRecommendationsPanel } from "./HrRecommendationsPanel";

interface AnalysisDashboardProps {
  analysis: Analysis;
  onReset: () => void;
}

export function AnalysisDashboard({
  analysis,
  onReset,
}: AnalysisDashboardProps) {
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-almia-700/60">
            Resultado del análisis
          </p>
          <h2 className="mt-1 text-2xl font-extrabold tracking-tight text-ink">
            Dashboard laboral del certificado
          </h2>
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={() => window.print()}
            className="rounded-2xl border border-almia-100 bg-white px-4 py-2 text-sm font-bold text-almia-700 transition hover:bg-almia-50"
          >
            Imprimir
          </button>
          <button
            type="button"
            onClick={onReset}
            className="rounded-2xl bg-gradient-to-r from-almia-400 to-almia-500 px-4 py-2 text-sm font-bold text-white transition hover:from-almia-500 hover:to-almia-700"
          >
            Analizar otro certificado
          </button>
        </div>
      </div>

      <ProfileHeaderCard analysis={analysis} />

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-6">
        <DomainMetricCard domain="cognicion" value={analysis.dominios.cognicion} />
        <DomainMetricCard domain="movilidad" value={analysis.dominios.movilidad} />
        <DomainMetricCard
          domain="cuidado_personal"
          value={analysis.dominios.cuidado_personal}
        />
        <DomainMetricCard domain="relaciones" value={analysis.dominios.relaciones} />
        <DomainMetricCard domain="vida_diaria" value={analysis.dominios.vida_diaria} />
        <DomainMetricCard
          domain="participacion"
          value={analysis.dominios.participacion}
        />
      </section>

      <section className="grid gap-5 xl:grid-cols-2">
        <RecommendedTasksPanel tasks={analysis.analisis.tareas_recomendadas} />
        <AdjustmentsPanel adjustments={analysis.analisis.ajustes_razonables} />
      </section>

      <NotRecommendedPanel items={analysis.analisis.tareas_no_recomendadas} />

      <section className="grid gap-5 xl:grid-cols-2">
        <FunctioningProfilePanel text={analysis.analisis.perfil_funcionamiento} />
        <HrRecommendationsPanel items={analysis.analisis.recomendaciones_rrhh_sst} />
      </section>
    </div>
  );
}
