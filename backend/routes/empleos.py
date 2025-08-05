
from fastapi import APIRouter, Query, BackgroundTasks
from typing import List, Optional
from backend.schemas import Empleo
import json
import os
import datetime
from playwright.sync_api import sync_playwright

router = APIRouter()

# Endpoint para obtener los valores válidos de los selectores de la página SIMO
@router.get("/opciones-filtros")
def obtener_opciones_filtros():
    url = "https://simo.cnsc.gov.co/#ofertaEmpleo"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3500)
        frames = page.frames
        target = page
        for frame in frames:
            try:
                if frame.query_selector("[id^='dgrid_0-row-']"):
                    target = frame
                    break
            except Exception:
                continue
        # Extraer opciones de los selectores
        def get_options(selector):
            try:
                sel = target.query_selector(selector)
                if sel:
                    return [o.inner_text().strip() for o in sel.query_selector_all('option') if o.inner_text().strip()]
            except Exception:
                pass
            return []
        departamentos = get_options("select[name='departamento']")
        ciudades = get_options("select[name='ciudad']")
        entidades = get_options("select[name='entidad']")
        niveles = get_options("select[name='nivel']")
        tipos_concurso = get_options("select[name='tipoConcurso']")
        discapacidades = get_options("select[name='discapacidad']")
        browser.close()
    return {
        "departamentos": departamentos,
        "ciudades": ciudades,
        "entidades": entidades,
        "niveles": niveles,
        "tipos_concurso": tipos_concurso,
        "discapacidades": discapacidades
    }
from fastapi import APIRouter, Query, BackgroundTasks
from typing import List, Optional
from backend.schemas import Empleo
import json
import os
import datetime

router = APIRouter()

DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/empleos_simo.json')

@router.get("/empleos", response_model=List[Empleo])
def listar_empleos(
    departamento: Optional[str] = Query(None),
    ciudad: Optional[str] = Query(None),
    salario_min: Optional[int] = Query(None),
    salario_max: Optional[int] = Query(None),
    tipo_concurso: Optional[str] = Query(None),
    discapacidad: Optional[str] = Query(None),
    entidad: Optional[str] = Query(None),
    nivel: Optional[str] = Query(None),
    numero_opec: Optional[str] = Query(None)
):
    from datetime import datetime
    with open(DATA_PATH, encoding="utf-8") as f:
        empleos = json.load(f)
    def fecha_valida(fecha):
        if not fecha or 'por definir' in fecha.lower():
            return False
        try:
            # Formato esperado: dd/mm/yyyy o similar
            fecha_dt = datetime.strptime(fecha.strip().split()[0], "%d/%m/%Y")
            return fecha_dt >= datetime.now()
        except Exception:
            return False
    def match(e):
        # Solo ofertas activas
        if not fecha_valida(e.get('fecha_cierre')):
            return False
        if departamento and e.get('municipio') and departamento.lower() not in e.get('municipio','').lower():
            return False
        if ciudad and e.get('municipio') and ciudad.lower() not in e.get('municipio','').lower():
            return False
        if salario_min and e.get('asignacion_salarial'):
            try:
                salario = int(''.join(filter(str.isdigit, e['asignacion_salarial'])))
                if salario < salario_min:
                    return False
            except:
                pass
        if salario_max and e.get('asignacion_salarial'):
            try:
                salario = int(''.join(filter(str.isdigit, e['asignacion_salarial'])))
                if salario > salario_max:
                    return False
            except:
                pass
        if tipo_concurso and e.get('tipo_concurso') and tipo_concurso.lower() not in e['tipo_concurso'].lower():
            return False
        if discapacidad and e.get('discapacidad') and discapacidad.lower() not in e['discapacidad'].lower():
            return False
        if entidad and e.get('entidad') and entidad.lower() not in e['entidad'].lower():
            return False
        if nivel and e.get('nivel') and nivel.lower() not in e['nivel'].lower():
            return False
        if numero_opec and e.get('numero_opec') and numero_opec not in e['numero_opec']:
            return False
        return True
    return [e for e in empleos if match(e)]

@router.get("/empleos/{numero_opec}", response_model=Empleo)
def detalle_empleo(numero_opec: str):
    with open(DATA_PATH, encoding="utf-8") as f:
        empleos = json.load(f)
    for e in empleos:
        if e.get('numero_opec') == numero_opec:
            return e
    return {}

@router.post("/telegram/consulta")
def consulta_telegram(mensaje: str):
    palabras = mensaje.split()
    departamento = palabras[0] if palabras else None
    salario_min = int(palabras[1]) if len(palabras) > 1 and palabras[1].isdigit() else None
    salario_max = int(palabras[2]) if len(palabras) > 2 and palabras[2].isdigit() else None
    return listar_empleos(departamento=departamento, salario_min=salario_min, salario_max=salario_max)

# Tarea programada de actualización automática (ejemplo)
def actualizar_empleos():
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)
    print(f"Empleos actualizados: {datetime.datetime.now()}")

@router.post("/actualizar")
def trigger_actualizacion(background_tasks: BackgroundTasks):
    background_tasks.add_task(actualizar_empleos)
    return {"status": "Actualización en segundo plano iniciada"}
