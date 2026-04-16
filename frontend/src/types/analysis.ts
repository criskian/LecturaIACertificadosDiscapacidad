export type DomainKey =
  | "cognicion"
  | "movilidad"
  | "cuidado_personal"
  | "relaciones"
  | "vida_diaria"
  | "participacion";

export interface Persona {
  nombre_completo: string;
  documento: string;
  municipio: string;
  departamento: string;
  fecha_certificacion: string;
  ips_certificadora: string;
}

export interface Dominios {
  cognicion: number;
  movilidad: number;
  cuidado_personal: number;
  relaciones: number;
  vida_diaria: number;
  participacion: number;
}

export interface TareasRecomendadas {
  administrativo_oficina: string[];
  operativo_manual_liviano: string[];
  relacional_apoyo: string[];
}

export interface AjusteRazonable {
  titulo: string;
  descripcion: string;
  fundamento: string;
}

export interface AnalisisLaboral {
  tareas_recomendadas: TareasRecomendadas;
  ajustes_razonables: AjusteRazonable[];
  tareas_no_recomendadas: string[];
  perfil_funcionamiento: string;
  recomendaciones_rrhh_sst: string[];
}

export interface Metadata {
  modelo_usado: string;
  fecha_procesamiento: string;
  estado: string;
}

export interface Analysis {
  persona: Persona;
  discapacidades_activas: string[];
  dominios: Dominios;
  analisis: AnalisisLaboral;
  metadata: Metadata;
}

export interface BackendAnalyzeResponse {
  id?: string;
  analysis_id?: string;
  filename?: string;
  content_type?: string;
  analysis: Analysis;
}

export interface AnalysisResult {
  analysisId: string;
  analysis: Analysis;
}
