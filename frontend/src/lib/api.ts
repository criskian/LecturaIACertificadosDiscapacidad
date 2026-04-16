import type { AnalysisResult, BackendAnalyzeResponse } from "../types/analysis";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

function buildUrl(path: string): string {
  return `${API_BASE_URL}${path}`;
}

export function validateCertificateFile(file: File | null): string | null {
  if (!file) {
    return "Selecciona un archivo para continuar.";
  }

  const allowed = [
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/webp",
  ];

  if (!allowed.includes(file.type)) {
    return "Solo se permiten archivos PDF, PNG, JPG o WEBP.";
  }

  const maxSizeBytes = 10 * 1024 * 1024;
  if (file.size > maxSizeBytes) {
    return "El archivo supera el límite recomendado de 10 MB.";
  }

  return null;
}

export async function analyzeCertificate(file: File): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(buildUrl("/api/v1/analyses"), {
    method: "POST",
    body: formData,
  });

  let payload: BackendAnalyzeResponse | { detail?: string };
  try {
    payload = await response.json();
  } catch {
    throw new Error("El servidor respondió en un formato inesperado.");
  }

  if (!response.ok) {
    const detail =
      typeof payload === "object" && payload && "detail" in payload
        ? payload.detail
        : undefined;
    throw new Error(detail || "No fue posible analizar el certificado.");
  }

  const data = payload as BackendAnalyzeResponse;
  return {
    analysisId: data.analysis_id || data.id || "sin-id",
    analysis: data.analysis,
  };
}
