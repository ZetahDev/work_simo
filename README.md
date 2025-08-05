# SIMO Scraper Backend

Backend en Python con FastAPI para hacer scraping de ofertas de empleo del portal SIMO (Sistema de Información y Monitoreo de Ofertas de Empleo) del CNSC (Comisión Nacional del Servicio Civil) de Colombia.

## 🚀 Características

- **Scraping API-based**: Utiliza la API REST de SIMO para obtener datos de manera eficiente
- **Base de datos**: Almacenamiento en SQLite (desarrollo) y PostgreSQL (producción)
- **API REST**: Endpoints para consultar ofertas, estadísticas y filtros
- **Scheduler**: Ejecución automática del scraping con APScheduler
- **Notificaciones Telegram**: Bot para notificaciones y consultas
- **Configuración**: Sistema de configuración basado en variables de entorno
- **Docker**: Containerización para deployment

## 🛠️ Tecnologías

- **Backend**: Python 3.9+, FastAPI
- **Base de datos**: SQLAlchemy, SQLite/PostgreSQL
- **HTTP Client**: aiohttp para llamadas a la API de SIMO
- **Scheduler**: APScheduler para tareas programadas
- **Bot**: python-telegram-bot
- **Testing**: pytest, httpx
- **Deployment**: Docker, Render

## 📋 Requisitos

- Python 3.9 o superior
- pip
- Git

## 🔧 Instalación

1. **Clonar el repositorio**:

```bash
git clone https://github.com/ZetahDev/work_simo.git
cd work_simo
```

2. **Crear entorno virtual**:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Instalar dependencias**:

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Crear directorio de datos**:

```bash
mkdir -p data
```

## ⚙️ Configuración

El archivo `.env` contiene todas las configuraciones necesarias:

```env
# Base de datos
DATABASE_URL=sqlite:///./data/simo_empleos.db

# Scraper
SIMO_API_URL=https://simo.cnsc.gov.co/empleos/ofertaPublica/
SCRAPER_MAX_CONCURRENT=5

# Scheduler
SCHEDULER_ENABLED=true
SCRAPER_CRON_HOUR=6

# Telegram (opcional)
TELEGRAM_BOT_TOKEN=your-token
TELEGRAM_ENABLED=false

# Logs
LOG_LEVEL=INFO
```

## 🚀 Uso

### Ejecutar el scraper manualmente

```bash
python scraping/scraper.py
```

### Ejecutar la API (próximamente)

```bash
uvicorn main:app --reload
```

### Ejecutar tests

```bash
pytest
```

## 📊 Estructura del proyecto

```
work_simo/
├── scraping/           # Módulo de scraping
│   └── scraper.py     # Scraper principal
├── database/          # Modelos y servicios de BD
│   ├── models.py      # Modelos SQLAlchemy
│   └── db_service.py  # Servicios de base de datos
├── data/              # Archivos de datos
├── tests/             # Tests
├── config.py          # Configuración de la aplicación
├── main.py            # Aplicación FastAPI principal
├── requirements.txt   # Dependencias
├── Dockerfile         # Imagen Docker
└── .env.example       # Configuración de ejemplo
```

## 🔍 API de SIMO

El scraper utiliza la API REST oficial de SIMO:

- **Endpoint**: `https://simo.cnsc.gov.co/empleos/ofertaPublica/`
- **Método**: GET con parámetros de paginación
- **Respuesta**: JSON con ofertas de empleo
- **Total disponible**: ~5,220 ofertas activas

## 📈 Próximas características

- [ ] API REST completa con FastAPI
- [ ] Filtros avanzados por cargo, entidad, ubicación
- [ ] Bot de Telegram funcional
- [ ] Dashboard web
- [ ] Análisis de tendencias
- [ ] Notificaciones personalizadas
- [ ] Deployment en Render

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Js Industries** (NIT 901446179-2)

## 📞 Contacto

Para preguntas o soporte, abre un issue en GitHub.

---

⚡ **Nota**: Este proyecto está en desarrollo activo. Las características marcadas como "próximamente" están planificadas para implementación.
