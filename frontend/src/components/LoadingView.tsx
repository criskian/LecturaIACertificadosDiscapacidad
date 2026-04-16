export function LoadingView() {
  return (
    <section className="space-y-5">
      <div className="panel-card overflow-hidden p-8 sm:p-10">
        <div className="flex items-center gap-4">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-100 border-t-blue-500" />
          <div>
            <h2 className="text-2xl font-extrabold text-ink">
              Procesando certificado
            </h2>
            <p className="mt-1 text-sm text-slate-500">
              Estamos extrayendo datos, interpretando el perfil funcional y
              preparando el dashboard visual.
            </p>
          </div>
        </div>
      </div>

      <div className="grid gap-5 lg:grid-cols-3">
        {Array.from({ length: 3 }).map((_, index) => (
          <div key={index} className="panel-card animate-pulse p-6">
            <div className="h-5 w-28 rounded-full bg-slate-200" />
            <div className="mt-6 h-10 w-24 rounded-full bg-slate-200" />
            <div className="mt-8 h-2 rounded-full bg-slate-200" />
            <div className="mt-3 h-2 w-4/5 rounded-full bg-slate-100" />
            <div className="mt-2 h-2 w-3/5 rounded-full bg-slate-100" />
          </div>
        ))}
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        {Array.from({ length: 2 }).map((_, index) => (
          <div key={index} className="panel-card animate-pulse p-6">
            <div className="h-6 w-48 rounded-full bg-slate-200" />
            <div className="mt-6 space-y-4">
              <div className="h-20 rounded-2xl bg-slate-100" />
              <div className="h-20 rounded-2xl bg-slate-100" />
              <div className="h-20 rounded-2xl bg-slate-100" />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
