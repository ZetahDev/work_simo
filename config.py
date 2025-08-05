"""
Configuración de la aplicación SIMO Scraper Backend.
"""
import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación usando variables de entorno."""
    
    # Configuración de la aplicación
    app_name: str = "SIMO Scraper Backend"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Configuración de la base de datos
    database_url: str = "sqlite:///./data/simo_empleos.db"
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # Configuración del scraper
    simo_api_url: str = "https://simo.cnsc.gov.co/empleos/ofertaPublica/"
    scraper_max_concurrent: int = 5
    scraper_delay_seconds: float = 1.0
    scraper_timeout_seconds: int = 30
    scraper_retry_attempts: int = 3
    
    # Configuración del scheduler
    scheduler_enabled: bool = True
    scraper_cron_hour: int = 6  # 6 AM
    scraper_cron_minute: int = 0
    
    # Configuración de Telegram
    telegram_bot_token: Optional[str] = None
    telegram_admin_chat_id: Optional[str] = None
    telegram_enabled: bool = False
    
    # Configuración de API
    api_prefix: str = "/api/v1"
    api_title: str = "SIMO Scraper API"
    api_description: str = "API para consultar ofertas de empleo de SIMO"
    
    # Configuración de logs
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuración de seguridad
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # Configuración de CORS
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()


def get_database_url() -> str:
    """
    Obtiene la URL de la base de datos.
    En producción, usa PostgreSQL. En desarrollo, usa SQLite.
    """
    if os.getenv("RENDER"):  # Detecta si está en Render
        return settings.database_url.replace("sqlite:///", "postgresql://")
    return settings.database_url


def is_production() -> bool:
    """Detecta si la aplicación está ejecutándose en producción."""
    return bool(os.getenv("RENDER") or os.getenv("PRODUCTION"))


def get_log_config() -> dict:
    """Configuración de logging para la aplicación."""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": settings.log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": settings.log_level,
            "handlers": ["default"],
        },
        "loggers": {
            "uvicorn": {
                "level": "INFO",
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["default"],
                "propagate": False,
            },
        },
    }
