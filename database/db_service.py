# Servicio de base de datos para SIMO
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from database.models import (
    Empleo, Entidad, Departamento, Municipio, Convocatoria, 
    ScrapingLog, UsuarioTelegram, NotificacionEnviada,
    create_database_engine, create_tables, get_session
)
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging
import json

class SimoDatabaseService:
    """Servicio para manejar operaciones de base de datos de SIMO"""
    
    def __init__(self, db_type: str = "sqlite"):
        self.engine = create_database_engine(db_type)
        create_tables(self.engine)
        self.logger = logging.getLogger("simo_db_service")
    
    def get_session(self) -> Session:
        """Obtener nueva sesión de base de datos"""
        return get_session(self.engine)
    
    def get_or_create_entidad(self, session: Session, nit: str, nombre: str, tipo_entidad: str = None) -> Entidad:
        """Obtener o crear entidad"""
        if not nit:
            # Si no hay NIT, buscar por nombre
            entidad = session.query(Entidad).filter(Entidad.nombre == nombre).first()
        else:
            entidad = session.query(Entidad).filter(Entidad.nit == nit).first()
        
        if not entidad:
            entidad = Entidad(
                nit=nit,
                nombre=nombre,
                tipo_entidad=tipo_entidad
            )
            session.add(entidad)
            session.flush()  # Para obtener el ID
        
        return entidad
    
    def get_or_create_departamento(self, session: Session, nombre: str) -> Departamento:
        """Obtener o crear departamento"""
        if not nombre:
            return None
            
        departamento = session.query(Departamento).filter(Departamento.nombre == nombre).first()
        
        if not departamento:
            departamento = Departamento(nombre=nombre)
            session.add(departamento)
            session.flush()
        
        return departamento
    
    def get_or_create_municipio(self, session: Session, nombre: str, departamento: Departamento) -> Municipio:
        """Obtener o crear municipio"""
        if not nombre or not departamento:
            return None
            
        municipio = session.query(Municipio).filter(
            and_(Municipio.nombre == nombre, Municipio.departamento_id == departamento.id)
        ).first()
        
        if not municipio:
            municipio = Municipio(
                nombre=nombre,
                departamento_id=departamento.id
            )
            session.add(municipio)
            session.flush()
        
        return municipio
    
    def get_or_create_convocatoria(self, session: Session, nombre: str, codigo: str = None, agno: int = None, tipo_proceso: str = None) -> Convocatoria:
        """Obtener o crear convocatoria"""
        if not nombre:
            return None
        
        # Buscar por nombre y código si existe
        query = session.query(Convocatoria).filter(Convocatoria.nombre == nombre)
        if codigo:
            query = query.filter(Convocatoria.codigo == codigo)
        
        convocatoria = query.first()
        
        if not convocatoria:
            convocatoria = Convocatoria(
                nombre=nombre,
                codigo=codigo,
                agno=agno,
                tipo_proceso=tipo_proceso
            )
            session.add(convocatoria)
            session.flush()
        
        return convocatoria
    
    def create_or_update_empleo(self, session: Session, empleo_data: Dict) -> Tuple[Empleo, bool]:
        """Crear o actualizar empleo. Retorna (empleo, es_nuevo)"""
        simo_id = empleo_data.get('id')
        
        # Buscar empleo existente
        empleo_existente = session.query(Empleo).filter(Empleo.simo_id == simo_id).first()
        es_nuevo = empleo_existente is None
        
        # Crear relaciones
        entidad = None
        if empleo_data.get('entidad_nombre'):
            entidad = self.get_or_create_entidad(
                session,
                empleo_data.get('entidad_nit', ''),
                empleo_data.get('entidad_nombre'),
                empleo_data.get('tipo_entidad')
            )
        
        departamento = None
        if empleo_data.get('departamento'):
            departamento = self.get_or_create_departamento(session, empleo_data.get('departamento'))
        
        municipio = None
        if empleo_data.get('municipio') and departamento:
            municipio = self.get_or_create_municipio(session, empleo_data.get('municipio'), departamento)
        
        convocatoria = None
        if empleo_data.get('convocatoria_nombre'):
            convocatoria = self.get_or_create_convocatoria(
                session,
                empleo_data.get('convocatoria_nombre'),
                empleo_data.get('convocatoria_codigo'),
                empleo_data.get('convocatoria_agno'),
                empleo_data.get('tipo_proceso')
            )
        
        # Datos del empleo
        empleo_fields = {
            'simo_id': simo_id,
            'empleo_id': empleo_data.get('empleo_id'),
            'codigo_empleo': empleo_data.get('codigo_empleo', '').strip(),
            'denominacion': empleo_data.get('denominacion', '').strip(),
            'denominacion_id': empleo_data.get('denominacion_id'),
            'nivel': empleo_data.get('nivel', '').strip(),
            'grado': empleo_data.get('grado', ''),
            'descripcion': empleo_data.get('descripcion', '').strip(),
            'asignacion_salarial': empleo_data.get('asignacion_salarial'),
            'vigencia_salarial': empleo_data.get('vigencia_salarial'),
            'convocatoria_nombre': empleo_data.get('convocatoria_nombre', '').strip(),
            'convocatoria_codigo': empleo_data.get('convocatoria_codigo', ''),
            'convocatoria_agno': empleo_data.get('convocatoria_agno'),
            'tipo_proceso': empleo_data.get('tipo_proceso', ''),
            'departamento': empleo_data.get('departamento', ''),
            'municipio': empleo_data.get('municipio', ''),
            'dependencia': empleo_data.get('dependencia', ''),
            'cantidad_vacantes': empleo_data.get('cantidad_vacantes', 0),
            'vacantes_disponibles': empleo_data.get('vacantes_disponibles', 0),
            'estudio_requerido': empleo_data.get('estudio_requerido', ''),
            'experiencia_requerida': empleo_data.get('experiencia_requerida', ''),
            'otros_requisitos': empleo_data.get('otros_requisitos', ''),
            'funciones': empleo_data.get('funciones', ''),
            'concurso_ascenso': empleo_data.get('concurso_ascenso', False),
            'condicion_discapacidad': empleo_data.get('condicion_discapacidad', False),
            'favorito': empleo_data.get('favorito', False),
            'fecha_inscripcion': empleo_data.get('fecha_inscripcion'),
            'activo': True,
            # Relaciones
            'entidad_id': entidad.id if entidad else None,
            'departamento_id': departamento.id if departamento else None,
            'municipio_id': municipio.id if municipio else None,
            'convocatoria_id': convocatoria.id if convocatoria else None,
        }
        
        if es_nuevo:
            # Crear nuevo empleo
            empleo_fields['fecha_scraping'] = datetime.fromisoformat(empleo_data.get('fecha_scraping', datetime.now().isoformat()))
            empleo = Empleo(**empleo_fields)
            session.add(empleo)
        else:
            # Actualizar empleo existente
            empleo_fields['fecha_actualizacion'] = datetime.now()
            for field, value in empleo_fields.items():
                setattr(empleo_existente, field, value)
            empleo = empleo_existente
        
        session.flush()
        return empleo, es_nuevo
    
    def bulk_insert_empleos(self, empleos_data: List[Dict]) -> Dict[str, int]:
        """Inserción masiva de empleos"""
        stats = {
            'procesados': 0,
            'nuevos': 0,
            'actualizados': 0,
            'errores': 0
        }
        
        session = self.get_session()
        try:
            for empleo_data in empleos_data:
                try:
                    empleo, es_nuevo = self.create_or_update_empleo(session, empleo_data)
                    
                    stats['procesados'] += 1
                    if es_nuevo:
                        stats['nuevos'] += 1
                    else:
                        stats['actualizados'] += 1
                    
                    # Commit cada 100 registros
                    if stats['procesados'] % 100 == 0:
                        session.commit()
                        self.logger.info(f"Procesados {stats['procesados']} empleos...")
                
                except Exception as e:
                    stats['errores'] += 1
                    self.logger.error(f"Error procesando empleo {empleo_data.get('id', 'N/A')}: {e}")
                    session.rollback()
                    continue
            
            # Commit final
            session.commit()
            self.logger.info(f"Inserción completada: {stats}")
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error en inserción masiva: {e}")
            raise
        finally:
            session.close()
        
        return stats
    
    def crear_log_scraping(self, fecha_inicio: datetime, empleos_encontrados: int = 0, 
                          empleos_nuevos: int = 0, empleos_actualizados: int = 0,
                          paginas_procesadas: int = 0, exitoso: bool = False,
                          mensaje_error: str = None, tiempo_ejecucion: float = None) -> int:
        """Crear registro de log de scraping"""
        session = self.get_session()
        try:
            log = ScrapingLog(
                fecha_inicio=fecha_inicio,
                fecha_fin=datetime.now(),
                empleos_encontrados=empleos_encontrados,
                empleos_nuevos=empleos_nuevos,
                empleos_actualizados=empleos_actualizados,
                paginas_procesadas=paginas_procesadas,
                exitoso=exitoso,
                mensaje_error=mensaje_error,
                tiempo_ejecucion=tiempo_ejecucion
            )
            session.add(log)
            session.commit()
            return log.id
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error creando log de scraping: {e}")
            raise
        finally:
            session.close()
    
    def buscar_empleos(self, filtros: Dict = None, pagina: int = 1, por_pagina: int = 20) -> Dict:
        """Buscar empleos con filtros y paginación"""
        session = self.get_session()
        try:
            query = session.query(Empleo).filter(Empleo.activo == True)
            
            # Aplicar filtros
            if filtros:
                if filtros.get('denominacion'):
                    query = query.filter(Empleo.denominacion.ilike(f"%{filtros['denominacion']}%"))
                
                if filtros.get('nivel'):
                    query = query.filter(Empleo.nivel.ilike(f"%{filtros['nivel']}%"))
                
                if filtros.get('departamento'):
                    query = query.filter(Empleo.departamento.ilike(f"%{filtros['departamento']}%"))
                
                if filtros.get('municipio'):
                    query = query.filter(Empleo.municipio.ilike(f"%{filtros['municipio']}%"))
                
                if filtros.get('salario_minimo'):
                    query = query.filter(Empleo.asignacion_salarial >= filtros['salario_minimo'])
                
                if filtros.get('salario_maximo'):
                    query = query.filter(Empleo.asignacion_salarial <= filtros['salario_maximo'])
                
                if filtros.get('entidad'):
                    query = query.join(Entidad).filter(Entidad.nombre.ilike(f"%{filtros['entidad']}%"))
            
            # Total de registros
            total = query.count()
            
            # Paginación
            offset = (pagina - 1) * por_pagina
            empleos = query.order_by(Empleo.fecha_scraping.desc()).offset(offset).limit(por_pagina).all()
            
            return {
                'empleos': empleos,
                'total': total,
                'pagina': pagina,
                'por_pagina': por_pagina,
                'total_paginas': (total + por_pagina - 1) // por_pagina
            }
            
        finally:
            session.close()
    
    def obtener_estadisticas(self) -> Dict:
        """Obtener estadísticas generales"""
        session = self.get_session()
        try:
            from sqlalchemy import func
            
            stats = {}
            
            # Total empleos activos
            stats['total_empleos'] = session.query(Empleo).filter(Empleo.activo == True).count()
            
            # Por nivel
            stats['por_nivel'] = dict(
                session.query(Empleo.nivel, func.count(Empleo.id))
                .filter(Empleo.activo == True)
                .group_by(Empleo.nivel)
                .all()
            )
            
            # Por departamento (top 10)
            stats['top_departamentos'] = dict(
                session.query(Empleo.departamento, func.count(Empleo.id))
                .filter(Empleo.activo == True, Empleo.departamento.isnot(None))
                .group_by(Empleo.departamento)
                .order_by(func.count(Empleo.id).desc())
                .limit(10)
                .all()
            )
            
            # Rango salarial
            salarios = session.query(
                func.min(Empleo.asignacion_salarial),
                func.max(Empleo.asignacion_salarial),
                func.avg(Empleo.asignacion_salarial)
            ).filter(
                Empleo.activo == True,
                Empleo.asignacion_salarial.isnot(None)
            ).first()
            
            if salarios[0]:
                stats['salarios'] = {
                    'minimo': float(salarios[0]),
                    'maximo': float(salarios[1]),
                    'promedio': float(salarios[2])
                }
            
            # Últimos scraping logs
            logs = session.query(ScrapingLog).order_by(ScrapingLog.fecha_inicio.desc()).limit(5).all()
            stats['ultimos_scrapings'] = [
                {
                    'fecha': log.fecha_inicio.isoformat(),
                    'exitoso': log.exitoso,
                    'empleos_encontrados': log.empleos_encontrados,
                    'empleos_nuevos': log.empleos_nuevos
                }
                for log in logs
            ]
            
            return stats
            
        finally:
            session.close()
    
    def registrar_usuario_telegram(self, chat_id: str, username: str = None, nombre_completo: str = None) -> UsuarioTelegram:
        """Registrar nuevo usuario de Telegram"""
        session = self.get_session()
        try:
            # Verificar si ya existe
            usuario = session.query(UsuarioTelegram).filter(UsuarioTelegram.chat_id == chat_id).first()
            
            if not usuario:
                usuario = UsuarioTelegram(
                    chat_id=chat_id,
                    username=username,
                    nombre_completo=nombre_completo
                )
                session.add(usuario)
                session.commit()
            
            return usuario
            
        finally:
            session.close()
    
    def actualizar_preferencias_usuario(self, chat_id: str, preferencias: Dict) -> bool:
        """Actualizar preferencias de notificación del usuario"""
        session = self.get_session()
        try:
            usuario = session.query(UsuarioTelegram).filter(UsuarioTelegram.chat_id == chat_id).first()
            
            if usuario:
                if 'niveles_interes' in preferencias:
                    usuario.niveles_interes = json.dumps(preferencias['niveles_interes'])
                
                if 'departamentos_interes' in preferencias:
                    usuario.departamentos_interes = json.dumps(preferencias['departamentos_interes'])
                
                if 'palabras_clave' in preferencias:
                    usuario.palabras_clave = json.dumps(preferencias['palabras_clave'])
                
                if 'salario_minimo' in preferencias:
                    usuario.salario_minimo = preferencias['salario_minimo']
                
                if 'frecuencia_notificaciones' in preferencias:
                    usuario.frecuencia_notificaciones = preferencias['frecuencia_notificaciones']
                
                usuario.fecha_actualizacion = datetime.now()
                session.commit()
                return True
            
            return False
            
        finally:
            session.close()
    
    def obtener_empleos_para_notificar(self, usuario: UsuarioTelegram, desde: datetime = None) -> List[Empleo]:
        """Obtener empleos que coinciden con las preferencias del usuario"""
        session = self.get_session()
        try:
            query = session.query(Empleo).filter(Empleo.activo == True)
            
            # Filtrar por fecha si se especifica
            if desde:
                query = query.filter(Empleo.fecha_scraping >= desde)
            
            # Aplicar filtros de usuario
            if usuario.niveles_interes:
                niveles = json.loads(usuario.niveles_interes)
                if niveles:
                    query = query.filter(Empleo.nivel.in_(niveles))
            
            if usuario.departamentos_interes:
                departamentos = json.loads(usuario.departamentos_interes)
                if departamentos:
                    query = query.filter(Empleo.departamento.in_(departamentos))
            
            if usuario.salario_minimo:
                query = query.filter(Empleo.asignacion_salarial >= usuario.salario_minimo)
            
            if usuario.palabras_clave:
                palabras = json.loads(usuario.palabras_clave)
                if palabras:
                    # Buscar en denominación o descripción
                    conditions = []
                    for palabra in palabras:
                        conditions.append(Empleo.denominacion.ilike(f"%{palabra}%"))
                        conditions.append(Empleo.descripcion.ilike(f"%{palabra}%"))
                    
                    if conditions:
                        query = query.filter(or_(*conditions))
            
            return query.order_by(Empleo.fecha_scraping.desc()).limit(50).all()
            
        finally:
            session.close()
