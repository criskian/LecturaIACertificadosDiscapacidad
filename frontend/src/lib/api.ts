import type { AnalysisResult, BackendAnalyzeResponse } from "../types/analysis";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "";
const ALLOWED_FILE_TYPES = [
  "application/pdf",
  "image/png",
  "image/jpeg",
  "image/webp",
];
const MAX_SIZE_BYTES = 10 * 1024 * 1024;

export interface CertificateAnalysisInput {
  file: File;
  formFile?: File | null;
  observations?: string;
}

function buildUrl(path: string): string {
  if (!API_BASE_URL) {
    throw new Error(
      "Configura VITE_API_BASE_URL para apuntar al backend de FastAPI.",
    );
  }
  return `${API_BASE_URL}${path}`;
}

export async function downloadCompanyReportPdf(analysisId: string): Promise<void> {
  if (!analysisId || analysisId === "sin-id") {
    throw new Error(
      "No se encontró un identificador válido del análisis para generar el reporte.",
    );
  }

  let response: Response;
  try {
    response = await fetch(buildUrl(`/api/v1/analyses/${analysisId}/pdf`), {
      headers: {
        Accept: "application/pdf",
      },
    });
  } catch {
    throw new Error(
      "No fue posible conectar con el backend para generar el informe PDF.",
    );
  }

  if (!response.ok) {
    throw new Error(
      "El backend no pudo generar el informe PDF para este análisis.",
    );
  }

  const blob = await response.blob();
  const contentDisposition = response.headers.get("Content-Disposition") || "";
  const filenameMatch = contentDisposition.match(/filename=\"?([^\"]+)\"?/i);
  const filename = filenameMatch?.[1] || "informe-laboral-inclusivo.pdf";

  const objectUrl = window.URL.createObjectURL(blob);
  const link = window.document.createElement("a");
  link.href = objectUrl;
  link.download = filename;
  window.document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(objectUrl);
}

export function validateCertificateFile(file: File | null): string | null {
  if (!file) {
    return "Selecciona un archivo para continuar.";
  }

  if (!ALLOWED_FILE_TYPES.includes(file.type)) {
    return "Solo se permiten archivos PDF, PNG, JPG o WEBP.";
  }

  if (file.size > MAX_SIZE_BYTES) {
    return "El archivo supera el límite recomendado de 10 MB.";
  }

  return null;
}

export function validateOptionalSupportingFile(file: File | null): string | null {
  if (!file) {
    return null;
  }

  if (!ALLOWED_FILE_TYPES.includes(file.type)) {
    return "El formulario opcional debe estar en PDF, PNG, JPG o WEBP.";
  }

  if (file.size > MAX_SIZE_BYTES) {
    return "El formulario opcional supera el límite recomendado de 10 MB.";
  }

  return null;
}

export async function analyzeCertificate({
  file,
  formFile,
  observations,
}: CertificateAnalysisInput): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append("file", file);
  if (formFile) {
    formData.append("form_file", formFile);
  }
  if (observations?.trim()) {
    formData.append("observations", observations.trim());
  }

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
