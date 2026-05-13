export function LoadingView() {
  return (
    <section className="space-y-5">
      <div className="panel-card overflow-hidden p-8 sm:p-10">
        <div className="flex items-center gap-4">
          <div className="relative flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-foam text-almia-700">
            <div className="absolute inset-0 animate-spin rounded-2xl border-2 border-almia-100 border-t-almia-500" />
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              className="h-6 w-6"
              aria-hidden="true"
            >
              <path
                d="M12 16V5"
                strokeWidth="2.2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M7.75 9.25L12 5L16.25 9.25"
                strokeWidth="2.2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M5 19H19"
                strokeWidth="2.2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <div>
            <h2 className="text-2xl font-extrabold text-ink">
              Procesando certificado
            </h2>
            <p className="mt-1 text-sm text-slate-500">
              Estamos revisando la informacion del certificado y preparando el
              resumen laboral.
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
