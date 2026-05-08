interface ErrorViewProps {
  message: string;
  onRetry: () => void;
}

export function ErrorView({ message, onRetry }: ErrorViewProps) {
  return (
    <section className="panel-card overflow-hidden border-rose-100">
      <div className="grid gap-6 bg-rose-50/70 p-8 sm:p-10 md:grid-cols-[auto_1fr_auto] md:items-center">
        <div className="flex h-14 w-14 items-center justify-center rounded-full bg-white text-2xl text-rose-700">
          !
        </div>
        <div>
          <h2 className="text-2xl font-extrabold text-rose-700">
            No pudimos completar la revision
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-7 text-rose-900/75">
            {message}
          </p>
        </div>
        <button
          type="button"
          onClick={onRetry}
          className="inline-flex items-center justify-center rounded-2xl bg-rose-600 px-5 py-3 text-sm font-bold text-white transition hover:bg-rose-700"
        >
          Volver a intentar
        </button>
      </div>
    </section>
  );
}
