import { useRef } from "react";

interface FileUploadCardProps {
  file: File | null;
  onFileChange: (file: File | null) => void;
  onAnalyze: () => void;
  isBusy: boolean;
}

export function FileUploadCard({
  file,
  onFileChange,
  onAnalyze,
  isBusy,
}: FileUploadCardProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  return (
    <section className="panel-card overflow-hidden">
      <div className="grid gap-8 p-8 lg:grid-cols-[1.1fr_0.9fr] lg:p-10">
        <div className="space-y-5">
          <span className="inline-flex rounded-full bg-almia-50 px-4 py-1 text-sm font-bold text-almia-700">
            Informe laboral visual
          </span>
          <div className="space-y-3">
            <h1 className="max-w-2xl text-4xl font-extrabold tracking-tight text-ink sm:text-5xl">
              Lectura IA de certificados de discapacidad
            </h1>
            <p className="max-w-2xl text-base leading-8 text-slate-600 sm:text-lg">
              Carga un certificado en imagen o PDF y recibe un dashboard
              corporativo con perfil funcional, tareas sugeridas, ajustes
              razonables y recomendaciones para RRHH y SST.
            </p>
          </div>
          <div className="flex flex-wrap gap-3 text-sm text-slate-500">
            <span className="rounded-full bg-sage-50 px-3 py-1 font-semibold text-sage-700">
              PDF, JPG, PNG o WEBP
            </span>
            <span className="rounded-full bg-almia-50 px-3 py-1 font-semibold text-almia-700">
              Flujo conectado al backend
            </span>
            <span className="rounded-full bg-terracotta-50 px-3 py-1 font-semibold text-terracotta-700">
              Resultado listo para imprimir
            </span>
          </div>
        </div>

        <div className="rounded-[28px] border border-dashed border-almia-100 bg-white/85 p-5">
          <div className="flex h-full flex-col justify-between rounded-[24px] bg-gradient-to-br from-canvas via-white to-almia-50/70 p-5">
            <button
              type="button"
              onClick={() => inputRef.current?.click()}
              className="group flex min-h-[220px] flex-col items-center justify-center rounded-[22px] border border-dashed border-almia-200 bg-white px-6 py-10 text-center transition hover:border-almia-300 hover:bg-almia-50/50"
            >
              <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-[24px] bg-almia-50 text-2xl text-almia-700 transition group-hover:scale-105">
                ↑
              </div>
              <h2 className="text-lg font-extrabold text-ink">
                {file ? "Archivo listo para analizar" : "Sube tu certificado"}
              </h2>
              <p className="mt-2 max-w-sm text-sm leading-6 text-slate-500">
                {file
                  ? `${file.name} · ${(file.size / 1024 / 1024).toFixed(2)} MB`
                  : "Arrastra el archivo aquí o selecciónalo desde tu equipo. Validamos formato y enviamos el documento al backend existente."}
              </p>
            </button>

            <input
              ref={inputRef}
              type="file"
              accept=".pdf,.png,.jpg,.jpeg,.webp"
              className="hidden"
              onChange={(event) => onFileChange(event.target.files?.[0] ?? null)}
            />

            <div className="mt-5 flex flex-col gap-3 sm:flex-row">
              <button
                type="button"
                onClick={onAnalyze}
                disabled={isBusy}
                className="inline-flex flex-1 items-center justify-center rounded-2xl bg-gradient-to-r from-almia-400 to-almia-500 px-5 py-3 text-sm font-bold text-white transition hover:from-almia-500 hover:to-almia-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isBusy ? "Procesando..." : "Analizar certificado"}
              </button>
              <button
                type="button"
                onClick={() => onFileChange(null)}
                disabled={!file || isBusy}
                className="inline-flex items-center justify-center rounded-2xl border border-line bg-white px-5 py-3 text-sm font-bold text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
              >
                Limpiar
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
