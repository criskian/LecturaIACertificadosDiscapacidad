from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class PersonaSchema(BaseModel):
    nombre_completo: str = ""
    documento: str = ""
    municipio: str = ""
    departamento: str = ""
    fecha_certificacion: str = ""
    ips_certificadora: str = ""


class DiscapacidadRawSchema(BaseModel):
    nombre: str
    marcado: Literal["SI", "NO", "ILEGIBLE"]


class DominiosSchema(BaseModel):
    cognicion: float = Field(default=0.0, ge=0, le=100)
    movilidad: float = Field(default=0.0, ge=0, le=100)
    cuidado_personal: float = Field(default=0.0, ge=0, le=100)
    relaciones: float = Field(default=0.0, ge=0, le=100)
    vida_diaria: float = Field(default=0.0, ge=0, le=100)
    participacion: float = Field(default=0.0, ge=0, le=100)


class CodigosCIFSchema(BaseModel):
    funciones_corporales: list[str] = Field(default_factory=list)
    estructuras_corporales: list[str] = Field(default_factory=list)
    actividades_participacion: list[str] = Field(default_factory=list)
    factores_ambientales: list[str] = Field(default_factory=list)


class AjusteRazonableSchema(BaseModel):
    titulo: str
    descripcion: str
    fundamento: str


class TareasRecomendadasSchema(BaseModel):
    administrativo_oficina: list[str] = Field(default_factory=list)
    operativo_manual_liviano: list[str] = Field(default_factory=list)
    relacional_apoyo: list[str] = Field(default_factory=list)


class AnalisisLaboralSchema(BaseModel):
    tareas_recomendadas: TareasRecomendadasSchema = Field(
        default_factory=TareasRecomendadasSchema
    )
    ajustes_razonables: list[AjusteRazonableSchema] = Field(default_factory=list)
    tareas_no_recomendadas: list[str] = Field(default_factory=list)
    perfil_funcionamiento: str = ""
    recomendaciones_rrhh_sst: list[str] = Field(default_factory=list)


class MetadataSchema(BaseModel):
    modelo_usado: str = ""
    fecha_procesamiento: datetime | None = None
    estado: Literal["success", "error", "processing"] = "processing"


class CertificateAnalysisSchema(BaseModel):
    persona: PersonaSchema = Field(default_factory=PersonaSchema)
    discapacidades_raw: list[DiscapacidadRawSchema] = Field(default_factory=list)
    discapacidades_activas: list[str] = Field(default_factory=list)
    dominios: DominiosSchema = Field(default_factory=DominiosSchema)
    codigos_cif: CodigosCIFSchema = Field(default_factory=CodigosCIFSchema)
    analisis: AnalisisLaboralSchema = Field(default_factory=AnalisisLaboralSchema)
    metadata: MetadataSchema = Field(default_factory=MetadataSchema)


class AnalysisCreateResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    analysis: CertificateAnalysisSchema


class AnalysisRecordResponse(AnalysisCreateResponse):
    created_at: datetime
    updated_at: datetime


class UploadResponse(BaseModel):
    upload_id: str
    filename: str
    content_type: str
    size_bytes: int
    accepted: bool = True


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str
    version: str
