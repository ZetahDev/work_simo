from fastapi import APIRouter, Query
from typing import List, Optional
from backend.schemas import Empleo
from datetime import datetime
import asyncio
import sys
import os

# Agregar scraping al path
SCRAPING_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scraping'))
if SCRAPING_PATH not in sys.path:
    sys.path.insert(0, SCRAPING_PATH)

from simo_scraping_playwright import scraping_simo  # importa la función

router = APIRouter(prefix="/scraping", tags=["scraping"])

@router.get("/empleos", response_model=List[Empleo])
async def obtener_empleos(
    departamento: Optional[str] = None,
    ciudad: Optional[str] = None,
    salario_min: Optional[int] = None,
    salario_max: Optional[int] = None,
    tipo_concurso: Optional[str] = None,
    discapacidad: Optional[str] = None,
    entidad: Optional[str] = None,
    nivel: Optional[str] = None,
    numero_opec: Optional[str] = None,
):
    filtros = {
        'departamento': departamento,
        'ciudad': ciudad,
        'salario_min': salario_min,
        'salario_max': salario_max,
        'tipo_concurso': tipo_concurso,
        'discapacidad': discapacidad,
        'entidad': entidad,
        'nivel': nivel,
        'numero_opec': numero_opec
    }
    empleos = await scraping_simo(filtros)
    return empleos

@router.get("/empleo/{numero_opec}", response_model=Optional[Empleo])
async def buscar_por_opec(numero_opec: str):
    """
    Retorna los detalles de un empleo específico por número OPEC.
    """
    empleos = await scraping_simo({'numero_opec': numero_opec})
    for e in empleos:
        if e.numero_opec == numero_opec:
            return e
    return None

@router.get("/fechas-cierre")
async def fechas_de_cierre(
    departamento: Optional[str] = None,
    tipo_concurso: Optional[str] = None
):
    """
    Lista fechas de cierre de inscripciones para empleos según filtros (ej. ascenso en Valle del Cauca).
    """
    empleos = await scraping_simo({
        'departamento': departamento,
        'tipo_concurso': tipo_concurso
    })
    return [
        {
            "numero_opec": e.numero_opec,
            "titulo": e.titulo,
            "fecha_cierre": e.fecha_cierre
        }
        for e in empleos if e.fecha_cierre
    ]

@router.post("/guardar-empleos")
async def guardar_empleos_en_json(filtros: dict):
    """
    Guarda el resultado del scraping con filtros en un archivo JSON.
    """
    empleos = await scraping_simo(filtros)
    with open("empleos_filtrados.json", "w", encoding="utf-8") as f:
        json.dump([e.dict() for e in empleos], f, ensure_ascii=False, indent=2)
    return {"mensaje": f"Se guardaron {len(empleos)} empleos en empleos_filtrados.json"}

@router.get("/empleos/vencidos")
async def empleos_vencidos_o_por_definir():
    """
    Lista empleos cuya fecha de cierre ya venció o está por definir.
    """
    empleos = await scraping_simo()
    hoy = datetime.now()

    def vencido_o_indefinido(fecha: str):
        if not fecha or "por definir" in fecha.lower():
            return True
        try:
            fecha_dt = datetime.strptime(fecha.strip(), "%d/%m/%Y")
            return fecha_dt < hoy
        except ValueError:
            return True

    resultado = [e for e in empleos if vencido_o_indefinido(e.fecha_cierre or "")]
    return resultado