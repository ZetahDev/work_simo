from typing import List, Optional
from pydantic import BaseModel

class Empleo(BaseModel):
    titulo: str
    nivel: Optional[str]
    denominacion: Optional[str]
    grado: Optional[str]
    codigo: Optional[str]
    numero_opec: Optional[str]
    entidad: Optional[str]
    asignacion_salarial: Optional[str]
    vigencia_salarial: Optional[str]
    convocatoria: Optional[str]
    tipo_concurso: Optional[str]
    fecha_cierre: Optional[str]
    total_vacantes: Optional[str]
    requisitos_estudio: Optional[str]
    requisitos_experiencia: Optional[str]
    dependencia: Optional[str]
    municipio: Optional[str]
    discapacidad: Optional[str]
    raw: Optional[str]

class FiltroBusqueda(BaseModel):
    departamento: Optional[str]
    ciudad: Optional[str]
    salario_min: Optional[int]
    salario_max: Optional[int]
    tipo_concurso: Optional[str]
    discapacidad: Optional[str]
    entidad: Optional[str]
    nivel: Optional[str]
    numero_opec: Optional[str]

class RespuestaBusqueda(BaseModel):
    empleos: List[Empleo]
    total: int
    filtros_aplicados: Optional[dict]
