import { useState } from "react";
import { AnalysisDashboard } from "./components/AnalysisDashboard";
import { ErrorView } from "./components/ErrorView";
import { FileUploadCard } from "./components/FileUploadCard";
import { LoadingView } from "./components/LoadingView";
import { useCertificateAnalysis } from "./hooks/useCertificateAnalysis";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [formFile, setFormFile] = useState<File | null>(null);
  const [observations, setObservations] = useState("");
  const { state, error, result, isBusy, submit, reset } = useCertificateAnalysis();

  const handleReset = () => {
    setFile(null);
    setFormFile(null);
    setObservations("");
    reset();
  };

  return (
    <main className="min-h-screen px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
      <div className="mx-auto max-w-7xl space-y-6">
        <FileUploadCard
          file={file}
          formFile={formFile}
          observations={observations}
          onFileChange={setFile}
          onFormFileChange={setFormFile}
          onObservationsChange={setObservations}
          onAnalyze={() => void submit(file, formFile, observations)}
          isBusy={isBusy}
        />

        {state === "idle" && (
          <section className="panel-card border-dashed bg-white/70 p-12 text-center">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-[24px] bg-sage-50 text-3xl text-sage-700">
              ✓
            </div>
            <h2 className="mt-5 text-2xl font-extrabold tracking-tight text-ink">
              Estado inicial listo para cargar
            </h2>
            <p className="mx-auto mt-3 max-w-2xl text-sm leading-7 text-slate-500">
              Cuando subas un certificado, aquí aparecerá el dashboard visual con
              perfil funcional, métricas, tareas recomendadas, ajustes
              razonables y recomendaciones corporativas.
            </p>
          </section>
        )}

        {state === "loading" && <LoadingView />}

        {state === "error" && error && (
          <ErrorView
            message={error}
            onRetry={() => void submit(file, formFile, observations)}
          />
        )}

        {state === "success" && result && (
          <AnalysisDashboard
            analysisId={result.analysisId}
            analysis={result.analysis}
            onReset={handleReset}
          />
        )}
      </div>
    </main>
  );
}
