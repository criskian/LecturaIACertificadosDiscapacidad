import type { AnalysisResult, BackendAnalyzeResponse } from "../types/analysis";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "";

function buildUrl(path: string): string {
  if (!API_BASE_URL) {
    throw new Error(
      "Configura VITE_API_BASE_URL para apuntar al backend de FastAPI.",
    );
  }
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

  let response: Response;
  try {
    response = await fetch(buildUrl("/api/v1/analyses"), {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error(
      "No fue posible conectar con el backend. Verifica VITE_API_BASE_URL y el despliegue del API.",
    );
  }

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
