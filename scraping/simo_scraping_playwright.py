

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
import json
from typing import List, Optional
import sys
import os
# Asegura que el path raíz esté en sys.path para importar backend.schemas
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)
from backend.schemas import Empleo

def pedir_filtros():
    print("\n=== Filtros disponibles ===")
    departamento = input("Departamento (dejar vacío para todos, debe coincidir exactamente con la opción del selector): ").strip() or None
    ciudad = input("Ciudad (dejar vacío para todos, debe coincidir exactamente con la opción del selector): ").strip() or None
    salario_min = input("Salario mínimo (solo número, dejar vacío para todos): ").strip()
    salario_max = input("Salario máximo (solo número, dejar vacío para todos): ").strip()
    tipo_concurso = input("Tipo de concurso (Abierto/Ascenso, dejar vacío para todos): ").strip() or None
    discapacidad = input("Discapacidad (dejar vacío para todos): ").strip() or None
    entidad = input("Entidad (dejar vacío para todas): ").strip() or None
    nivel = input("Nivel (dejar vacío para todos): ").strip() or None
    numero_opec = input("Número OPEC (dejar vacío para todos): ").strip() or None
    return {
        'departamento': departamento,
        'ciudad': ciudad,
        'salario_min': int(salario_min) if salario_min else None,
        'salario_max': int(salario_max) if salario_max else None,
        'tipo_concurso': tipo_concurso,
        'discapacidad': discapacidad,
        'entidad': entidad,
        'nivel': nivel,
        'numero_opec': numero_opec
    }

# --- Utilidades de extracción ---
def extraer_empleo(texto: str) -> Empleo:
    def buscar_patron(pat, default=None):
        m = re.search(pat, texto, re.IGNORECASE)
        return m.group(1).strip() if m else default
    return Empleo(
        titulo=buscar_patron(r"Denominación: ([^\n]+)") or buscar_patron(r"PROFESIONAL UNIVERSITARIO|TÉCNICO OPERATIVO|AUXILIAR ADMINISTRATIVO|OPERARIO|SECRETARIO EJECUTIVO", ""),
        nivel=buscar_patron(r"Nivel: ([^\n]+)"),
        denominacion=buscar_patron(r"Denominación: ([^\n]+)"),
        grado=buscar_patron(r"Grado: ([^\n]+)"),
        codigo=buscar_patron(r"Código: ([^\n]+)"),
        numero_opec=buscar_patron(r"Número OPEC: ([^\n]+)"),
        entidad=buscar_patron(r"CONVOCATORIA [^\n]+ ([^-]+) -"),
        asignacion_salarial=buscar_patron(r"Asignación salarial: ([^\n$]+\$? ?[\d\.]+)"),
        vigencia_salarial=buscar_patron(r"Vigencia salarial: ([^\n]+)"),
        convocatoria=buscar_patron(r"CONVOCATORIA ([^\n]+)"),
        tipo_concurso=buscar_patron(r"- (Abierto|Ascenso)"),
        fecha_cierre=buscar_patron(r"Cierre de inscripciones: ([^\n]+)"),
        total_vacantes=buscar_patron(r"Total de vacantes del empleo: ([^\n]+)"),
        requisitos_estudio=buscar_patron(r"Requisitos Estudio: ([^\n]+)"),
        requisitos_experiencia=buscar_patron(r"Experiencia: ([^\n]+)"),
        dependencia=buscar_patron(r"Dependencia: ([^,\n]+)"),
        municipio=buscar_patron(r"Municipio: ([^,\n]+)"),
        discapacidad=buscar_patron(r"reservados para personas con discapacidad ([^\n]+)"),
        raw=texto
    )

async def scraping_simo(filtros: Optional[dict] = None) -> List[Empleo]:
    url = "https://simo.cnsc.gov.co/#ofertaEmpleo"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(3500)
        frames = page.frames
        target = page
        for frame in frames:
            try:
                if await frame.query_selector("[id^='dgrid_0-row-']"):
                    target = frame
                    break
            except Exception:
                continue
        await target.wait_for_selector("[id^='dgrid_0-row-']", timeout=40000)
        # Aplicar filtros usando select_option para Departamento y Ciudad
        if filtros:
            if filtros.get('departamento'):
                try:
                    dep_selector = await target.query_selector("select[name='departamento']")
                    if dep_selector:
                        await dep_selector.select_option(label=filtros['departamento'])
                        await target.wait_for_timeout(800)
                except Exception as e:
                    print(f"No se pudo seleccionar departamento: {e}")
            if filtros.get('ciudad'):
                try:
                    ciudad_selector = await target.query_selector("select[name='ciudad']")
                    if ciudad_selector:
                        await ciudad_selector.select_option(label=filtros['ciudad'])
                        await target.wait_for_timeout(800)
                except Exception as e:
                    print(f"No se pudo seleccionar ciudad: {e}")
            # Otros filtros pueden implementarse aquí usando select_option o fill según corresponda
        # Click en BUSCAR si existe
        try:
            buscar_btn = await target.query_selector("text=BUSCAR")
            if buscar_btn:
                await buscar_btn.click()
                await target.wait_for_timeout(2000)
        except Exception:
            pass
        from datetime import datetime
        empleos = []
        pagina = 1
        def fecha_valida(fecha):
            if not fecha or 'por definir' in fecha.lower():
                return False
            try:
                fecha_dt = datetime.strptime(fecha.strip().split()[0], "%d/%m/%Y")
                return fecha_dt >= datetime.now()
            except Exception:
                return False
        while True:
            await target.wait_for_selector("[id^='dgrid_0-row-']", timeout=40000)
            html = await target.content()
            soup = BeautifulSoup(html, 'html.parser')
            filas = soup.select("[id^='dgrid_0-row-']")
            print(f"Página {pagina}: {len(filas)} empleos extraídos")
            for fila in filas:
                texto = fila.get_text(separator=' ', strip=True)
                empleo = extraer_empleo(texto)
                # Solo guardar empleos activos
                if fecha_valida(getattr(empleo, 'fecha_cierre', None)):
                    empleos.append(empleo)
            # Scroll manual hacia el pie de página antes de buscar el botón
            await target.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await target.wait_for_timeout(800)
            next_btn = await target.query_selector('button[aria-label="Ir a la siguiente página"]')
            if next_btn:
                disabled = await next_btn.is_disabled()
                print(f"Botón siguiente habilitado: {not disabled}")
            if next_btn and not await next_btn.is_disabled():
                first_row_id = await target.get_attribute("[id^='dgrid_0-row-']", "id")
                print(f"ID primera fila antes: {first_row_id}")
                await next_btn.scroll_into_view_if_needed()
                # Intento de doble click si click simple no avanza
                try:
                    await next_btn.click()
                    await target.wait_for_timeout(500)
                except Exception:
                    print("Click simple falló, intentando doble click...")
                    await next_btn.dblclick()
                for _ in range(30):
                    await target.wait_for_timeout(300)
                    new_first_row_id = await target.get_attribute("[id^='dgrid_0-row-']", "id")
                    if new_first_row_id != first_row_id:
                        print(f"Cambio de página detectado. ID nueva fila: {new_first_row_id}")
                        break
                pagina += 1
            else:
                print("No hay más páginas o el botón está deshabilitado.")
                break
        await browser.close()
    return empleos


if __name__ == "__main__":
    filtros = pedir_filtros()
    empleos = asyncio.run(scraping_simo(filtros))
    with open("empleos_simo.json", "w", encoding="utf-8") as f:
        json.dump([e.model_dump() if hasattr(e, 'model_dump') else e.dict() for e in empleos], f, ensure_ascii=False, indent=2)
    print(f"Se extrajeron {len(empleos)} empleos y se guardaron en empleos_simo.json")
