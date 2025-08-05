# Modelos de base de datos para SIMO
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import create_engine
from datetime import datetime
from typing import Optional

Base = declarative_base()

class Entidad(Base):
    """Tabla de entidades empleadoras"""
    __tablename__ = "entidades"
    
    id = Column(Integer, primary_key=True, index=True)
    nit = Column(String(20), unique=True, index=True)
    nombre = Column(String(500), nullable=False, index=True)
    tipo_entidad = Column(String(100))
    
    # Relaciones
    empleos = relationship("Empleo", back_populates="entidad")
    
    # Índices
    __table_args__ = (
        Index('idx_entidad_nombre', 'nombre'),
        Index('idx_entidad_tipo', 'tipo_entidad'),
    )

class Departamento(Base):
    """Tabla de departamentos"""
    __tablename__ = "departamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    
    # Relaciones
    municipios = relationship("Municipio", back_populates="departamento")
    empleos = relationship("Empleo", back_populates="departamento_obj")

class Municipio(Base):
    """Tabla de municipios"""
    __tablename__ = "municipios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    
    # Relaciones
    departamento = relationship("Departamento", back_populates="municipios")
    empleos = relationship("Empleo", back_populates="municipio_obj")
    
    # Índices
    __table_args__ = (
        Index('idx_municipio_departamento', 'departamento_id'),
    )

class Convocatoria(Base):
    """Tabla de convocatorias"""
    __tablename__ = "convocatorias"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(500), nullable=False)
    codigo = Column(String(50), index=True)
    agno = Column(Integer, index=True)
    tipo_proceso = Column(String(100))
    
    # Relaciones
    empleos = relationship("Empleo", back_populates="convocatoria_obj")
    
    # Índices
    __table_args__ = (
        Index('idx_convocatoria_agno', 'agno'),
        Index('idx_convocatoria_codigo', 'codigo'),
    )

class Empleo(Base):
    """Tabla principal de empleos"""
    __tablename__ = "empleos"
    
    # IDs
    id = Column(Integer, primary_key=True, index=True)
    simo_id = Column(Integer, unique=True, index=True)  # ID original de SIMO
    empleo_id = Column(Integer, index=True)  # ID del empleo en SIMO
    
    # Información básica del empleo
    codigo_empleo = Column(String(20), index=True)
    denominacion = Column(String(200), nullable=False, index=True)
    denominacion_id = Column(Integer)
    nivel = Column(String(50), nullable=False, index=True)
    grado = Column(String(10), index=True)
    descripcion = Column(Text)
    
    # Información salarial
    asignacion_salarial = Column(Float, index=True)
    vigencia_salarial = Column(Integer)
    
    # Referencias a otras tablas
    entidad_id = Column(Integer, ForeignKey("entidades.id"), index=True)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"), index=True)
    municipio_id = Column(Integer, ForeignKey("municipios.id"), index=True)
    convocatoria_id = Column(Integer, ForeignKey("convocatorias.id"), index=True)
    
    # Información de convocatoria
    convocatoria_nombre = Column(String(500))
    convocatoria_codigo = Column(String(50))
    convocatoria_agno = Column(Integer)
    tipo_proceso = Column(String(100))
    
    # Información de ubicación (desnormalizada para consultas rápidas)
    departamento = Column(String(100), index=True)
    municipio = Column(String(100), index=True)
    dependencia = Column(String(300))
    
    # Información de vacantes
    cantidad_vacantes = Column(Integer, default=0)
    vacantes_disponibles = Column(Integer, default=0)
    
    # Requisitos
    estudio_requerido = Column(Text)
    experiencia_requerida = Column(Text)
    otros_requisitos = Column(Text)
    
    # Funciones
    funciones = Column(Text)
    
    # Banderas
    concurso_ascenso = Column(Boolean, default=False)
    condicion_discapacidad = Column(Boolean, default=False)
    favorito = Column(Boolean, default=False)
    
    # Fechas
    fecha_inscripcion = Column(String(20))  # Formato string de SIMO
    fecha_scraping = Column(DateTime, default=datetime.utcnow, index=True)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Estado del registro
    activo = Column(Boolean, default=True, index=True)
    
    # Relaciones
    entidad = relationship("Entidad", back_populates="empleos")
    departamento_obj = relationship("Departamento", back_populates="empleos")
    municipio_obj = relationship("Municipio", back_populates="empleos")
    convocatoria_obj = relationship("Convocatoria", back_populates="empleos")
    
    # Índices compuestos para búsquedas comunes
    __table_args__ = (
        Index('idx_empleo_nivel_departamento', 'nivel', 'departamento'),
        Index('idx_empleo_denominacion_nivel', 'denominacion', 'nivel'),
        Index('idx_empleo_salario_nivel', 'asignacion_salarial', 'nivel'),
        Index('idx_empleo_fecha_activo', 'fecha_scraping', 'activo'),
        Index('idx_empleo_busqueda', 'denominacion', 'nivel', 'departamento', 'activo'),
    )

class ScrapingLog(Base):
    """Log de ejecuciones de scraping"""
    __tablename__ = "scraping_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_fin = Column(DateTime)
    empleos_encontrados = Column(Integer, default=0)
    empleos_nuevos = Column(Integer, default=0)
    empleos_actualizados = Column(Integer, default=0)
    paginas_procesadas = Column(Integer, default=0)
    exitoso = Column(Boolean, default=False)
    mensaje_error = Column(Text)
    tiempo_ejecucion = Column(Float)  # En segundos
    
    # Índices
    __table_args__ = (
        Index('idx_scraping_fecha', 'fecha_inicio'),
        Index('idx_scraping_exitoso', 'exitoso'),
    )

class UsuarioTelegram(Base):
    """Usuarios suscritos a notificaciones por Telegram"""
    __tablename__ = "usuarios_telegram"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String(50), unique=True, nullable=False, index=True)
    username = Column(String(100))
    nombre_completo = Column(String(200))
    
    # Preferencias de filtros
    niveles_interes = Column(String(200))  # JSON string con niveles de interés
    departamentos_interes = Column(String(500))  # JSON string con departamentos
    palabras_clave = Column(String(500))  # JSON string con palabras clave
    salario_minimo = Column(Float)
    
    # Control de notificaciones
    activo = Column(Boolean, default=True)
    frecuencia_notificaciones = Column(String(20), default="inmediato")  # inmediato, diario, semanal
    ultima_notificacion = Column(DateTime)
    
    # Metadatos
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índices
    __table_args__ = (
        Index('idx_telegram_activo', 'activo'),
        Index('idx_telegram_frecuencia', 'frecuencia_notificaciones'),
    )

class NotificacionEnviada(Base):
    """Log de notificaciones enviadas"""
    __tablename__ = "notificaciones_enviadas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_telegram_id = Column(Integer, ForeignKey("usuarios_telegram.id"))
    empleo_id = Column(Integer, ForeignKey("empleos.id"))
    fecha_envio = Column(DateTime, default=datetime.utcnow)
    exitosa = Column(Boolean, default=True)
    mensaje_error = Column(Text)
    
    # Relaciones
    usuario = relationship("UsuarioTelegram")
    empleo = relationship("Empleo")
    
    # Índices
    __table_args__ = (
        Index('idx_notificacion_usuario_fecha', 'usuario_telegram_id', 'fecha_envio'),
        Index('idx_notificacion_empleo', 'empleo_id'),
    )

# Configuración de base de datos
def get_database_url(db_type: str = "sqlite") -> str:
    """Obtener URL de conexión según el tipo de base de datos"""
    if db_type == "sqlite":
        return "sqlite:///./simo_empleos.db"
    elif db_type == "postgresql":
        # Para producción en Render
        import os
        db_url = os.getenv("DATABASE_URL")
        if db_url and db_url.startswith("postgres://"):
            # Render usa postgres:// pero SQLAlchemy requiere postgresql://
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        return db_url or "postgresql://user:password@localhost:5432/simo_empleos"
    else:
        raise ValueError(f"Tipo de base de datos no soportado: {db_type}")

def create_database_engine(db_type: str = "sqlite"):
    """Crear engine de base de datos"""
    database_url = get_database_url(db_type)
    
    if db_type == "sqlite":
        engine = create_engine(
            database_url, 
            connect_args={"check_same_thread": False},
            echo=False  # Cambiar a True para debug SQL
        )
    else:
        engine = create_engine(database_url, echo=False)
    
    return engine

def create_tables(engine):
    """Crear todas las tablas"""
    Base.metadata.create_all(bind=engine)

def get_session(engine) -> Session:
    """Obtener sesión de base de datos"""
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

# Funciones de utilidad para consultas comunes
def buscar_empleos_por_criterios(
    session: Session,
    denominacion: Optional[str] = None,
    nivel: Optional[str] = None,
    departamento: Optional[str] = None,
    salario_minimo: Optional[float] = None,
    activo: bool = True,
    limit: int = 100,
    offset: int = 0
):
    """Buscar empleos con criterios específicos"""
    query = session.query(Empleo).filter(Empleo.activo == activo)
    
    if denominacion:
        query = query.filter(Empleo.denominacion.ilike(f"%{denominacion}%"))
    
    if nivel:
        query = query.filter(Empleo.nivel.ilike(f"%{nivel}%"))
    
    if departamento:
        query = query.filter(Empleo.departamento.ilike(f"%{departamento}%"))
    
    if salario_minimo:
        query = query.filter(Empleo.asignacion_salarial >= salario_minimo)
    
    return query.order_by(Empleo.fecha_scraping.desc()).offset(offset).limit(limit).all()

def obtener_estadisticas_empleos(session: Session):
    """Obtener estadísticas generales de empleos"""
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
        .filter(Empleo.activo == True)
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
            'minimo': salarios[0],
            'maximo': salarios[1],
            'promedio': salarios[2]
        }
    
    return stats
