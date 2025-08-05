# Scraper mejorado que usa la API REST de SIMO
import asyncio
import json
import logging
from datetime import datetime
import aiohttp
from typing import List, Dict, Optional
import re

class SimoApiScraper:
    """Scraper que extrae datos directamente de la API REST de SIMO"""
    
    def __init__(self):
        self.base_url = "https://simo.cnsc.gov.co/empleos/ofertaPublica/"
        self.session = None
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """Configurar logging"""
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger("simo_api_scraper")
    
    async def __aenter__(self):
        """Context manager para sesión HTTP"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cerrar sesión HTTP"""
        if self.session:
            await self.session.close()
    
    def parse_content_range(self, content_range: str) -> tuple[int, int, int]:
        """Parsear header Content-Range para obtener información de paginación"""
        # Formato: "0-9/5220" significa elementos 0-9 de un total de 5220
        if content_range:
            match = re.match(r'(\d+)-(\d+)/(\d+)', content_range)
            if match:
                start = int(match.group(1))
                end = int(match.group(2))
                total = int(match.group(3))
                return start, end, total
        return 0, 0, 0
    
    async def get_page_data(self, page: int = 0, size: int = 20) -> tuple[List[Dict], int]:
        """Obtener datos de una página específica y total de elementos"""
        url = f"{self.base_url}?page={page}&size={size}"
        
        try:
            self.logger.info(f"📡 Obteniendo página {page} (tamaño: {size})")
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    # Obtener total de elementos del header Content-Range
                    content_range = response.headers.get('Content-Range', '')
                    start, end, total_elements = self.parse_content_range(content_range)
                    
                    data = await response.json()
                    self.logger.info(f"✅ Página {page}: {len(data)} empleos obtenidos (total: {total_elements})")
                    
                    return data, total_elements
                else:
                    self.logger.error(f"❌ Error HTTP {response.status} en página {page}")
                    return [], 0
                    
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo página {page}: {e}")
            return [], 0
    
    async def get_total_elements(self) -> int:
        """Obtener el total de elementos disponibles"""
        _, total = await self.get_page_data(page=0, size=1)
        return total
    
    def process_job_data(self, job_item: Dict) -> Dict:
        """Procesar y normalizar datos de un empleo"""
        empleo = job_item.get('empleo', {})
        convocatoria = empleo.get('convocatoria', {})
        entidad = convocatoria.get('entidad', {})
        denominacion = empleo.get('denominacion', {})
        grado_nivel = empleo.get('gradoNivel', {})
        
        # Obtener primera vacante (suele haber una)
        vacantes = empleo.get('vacantes', [])
        primera_vacante = vacantes[0] if vacantes else {}
        municipio = primera_vacante.get('municipio', {})
        departamento = municipio.get('departamento', {})
        
        # Obtener requisitos
        requisitos = empleo.get('requisitosMinimos', [])
        primer_requisito = requisitos[0] if requisitos else {}
        
        # Obtener funciones (concatenar todas)
        funciones = empleo.get('funciones', [])
        funciones_texto = ' | '.join([f['descripcion'] for f in funciones])
        
        return {
            "id": job_item.get('id'),
            "empleo_id": empleo.get('id'),
            "codigo_empleo": empleo.get('codigoEmpleo', '').strip(),
            "denominacion": denominacion.get('nombre', '').strip(),
            "denominacion_id": denominacion.get('id'),
            "nivel": grado_nivel.get('nivelNombre', '').strip(),
            "grado": grado_nivel.get('grado', ''),
            "descripcion": empleo.get('descripcion', '').strip(),
            "asignacion_salarial": empleo.get('asignacionSalarial'),
            "vigencia_salarial": empleo.get('vigenciaSalarial'),
            
            # Entidad
            "entidad_nombre": entidad.get('nombre', '').strip(),
            "entidad_nit": entidad.get('nit', ''),
            "tipo_entidad": entidad.get('tipoEntidad', {}).get('nombre', ''),
            
            # Convocatoria
            "convocatoria_nombre": convocatoria.get('nombre', ''),
            "convocatoria_codigo": convocatoria.get('codigo', ''),
            "convocatoria_agno": convocatoria.get('agno'),
            "tipo_proceso": convocatoria.get('tipoProceso', ''),
            
            # Ubicación
            "departamento": departamento.get('nombre', ''),
            "municipio": municipio.get('nombre', ''),
            "dependencia": primera_vacante.get('dependencia', {}).get('nombre', ''),
            
            # Vacantes
            "cantidad_vacantes": primera_vacante.get('cantidad', 0),
            "vacantes_disponibles": primera_vacante.get('disponible', 0),
            
            # Requisitos
            "estudio_requerido": primer_requisito.get('estudio', '').strip(),
            "experiencia_requerida": primer_requisito.get('experiencia', '').strip(),
            "otros_requisitos": primer_requisito.get('otros', ''),
            
            # Funciones (texto concatenado)
            "funciones": funciones_texto,
            
            # Banderas
            "concurso_ascenso": empleo.get('concursoAscenso', False),
            "condicion_discapacidad": empleo.get('condicionDiscapacidad', False),
            "favorito": job_item.get('favorito', False),
            "fecha_inscripcion": job_item.get('fechaInscripcion'),
            
            # Metadatos
            "fecha_scraping": datetime.now().isoformat()
        }
    
    async def scrape_all_jobs(self, max_pages: Optional[int] = None, page_size: int = 50) -> List[Dict]:
        """Scraper completo de todas las ofertas de empleo"""
        self.logger.info("🚀 Iniciando scraping completo de SIMO API...")
        
        # Obtener total de elementos
        total_elements = await self.get_total_elements()
        
        if total_elements == 0:
            self.logger.error("❌ No se pudo obtener información de total de elementos")
            return []
        
        # Calcular número de páginas necesarias
        total_pages = (total_elements + page_size - 1) // page_size  # Ceiling division
        
        # Limitar páginas si se especifica
        pages_to_scrape = min(total_pages, max_pages) if max_pages else total_pages
        
        self.logger.info(f"📊 Total elementos: {total_elements}")
        self.logger.info(f"📄 Páginas necesarias: {total_pages} (tamaño: {page_size})")
        self.logger.info(f"📄 Procesando {pages_to_scrape} páginas")
        
        all_jobs = []
        
        # Procesar todas las páginas
        for page in range(pages_to_scrape):
            page_data, _ = await self.get_page_data(page=page, size=page_size)
            
            if page_data:
                for job_item in page_data:
                    try:
                        processed_job = self.process_job_data(job_item)
                        all_jobs.append(processed_job)
                    except Exception as e:
                        self.logger.warning(f"⚠️ Error procesando empleo en página {page}: {e}")
                        continue
                
                self.logger.info(f"✅ Página {page + 1}/{pages_to_scrape} completada - {len(page_data)} empleos")
                
                # Pequeña pausa para no sobrecargar el servidor
                await asyncio.sleep(0.3)
            else:
                self.logger.warning(f"⚠️ Página {page} vacía o con error")
        
        self.logger.info(f"🎉 Scraping completado! Total empleos obtenidos: {len(all_jobs)}")
        return all_jobs
    
    async def search_jobs_by_criteria(self, filters: Dict = None, max_pages: int = None) -> List[Dict]:
        """Buscar empleos con criterios específicos"""
        all_jobs = await self.scrape_all_jobs(max_pages=max_pages)
        
        if not filters:
            return all_jobs
        
        filtered_jobs = []
        
        for job in all_jobs:
            match = True
            
            # Filtro por denominación (ej: "técnico")
            if 'denominacion' in filters:
                if filters['denominacion'].lower() not in job['denominacion'].lower():
                    match = False
            
            # Filtro por nivel
            if 'nivel' in filters:
                if filters['nivel'].lower() != job['nivel'].lower():
                    match = False
            
            # Filtro por entidad
            if 'entidad' in filters:
                if filters['entidad'].lower() not in job['entidad_nombre'].lower():
                    match = False
            
            # Filtro por departamento
            if 'departamento' in filters:
                if filters['departamento'].lower() not in job['departamento'].lower():
                    match = False
            
            # Filtro por salario mínimo
            if 'salario_minimo' in filters:
                if job['asignacion_salarial'] and job['asignacion_salarial'] < filters['salario_minimo']:
                    match = False
            
            if match:
                filtered_jobs.append(job)
        
        self.logger.info(f"🔍 Filtros aplicados: {len(filtered_jobs)} empleos encontrados de {len(all_jobs)} totales")
        return filtered_jobs
