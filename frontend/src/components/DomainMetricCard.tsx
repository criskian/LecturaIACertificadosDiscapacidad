import type { DomainKey } from "../types/analysis";
import {
  DOMAIN_LABELS,
  clampMetric,
  getDomainTone,
} from "../utils/analysis";

interface DomainMetricCardProps {
  domain: DomainKey;
  value: number;
}

export function DomainMetricCard({ domain, value }: DomainMetricCardProps) {
  const metric = clampMetric(value);
  const tone = getDomainTone(metric);

  return (
    <article className={`panel-card border-white/60 p-5 ${tone.halo}`}>
      <div className="space-y-3">
        <p className="text-center text-sm font-semibold uppercase tracking-[0.12em] text-slate-500">
          {DOMAIN_LABELS[domain]}
        </p>
        <p className={`text-center text-4xl font-extrabold ${tone.text}`}>
          {metric.toFixed(metric % 1 === 0 ? 0 : 2)}
        </p>
        <div className="h-2.5 rounded-full bg-white/90 shadow-inner">
          <div
            className={`h-2.5 rounded-full ${tone.bar} transition-all`}
            style={{ width: `${metric}%` }}
          />
        </div>
      </div>
    </article>
  );
}
