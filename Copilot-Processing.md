# Copilot Processing Log

## User Request
Desarrollar un backend en Python (FastAPI) para Js Industries (NIT 901446179-2) que realice scraping de ofertas de empleo en https://simo.cnsc.gov.co/#ofertaEmpleo, debe realizarse un analisis previo para visualizar que es lo que contiene dicha pagina para darle un buen manejo. El backend debe usar Playwright para scraping dinámico, almacenar datos en SQLite/PostgreSQL, enviar notificaciones vía Telegram, y exponer endpoints API en FastAPI. Debe desplegarse en Render, manejar errores robustamente, y cumplir con los requerimientos detallados en el prompt.

- Scraping con Playwright (manejo de DOM dinámico, filtros, paginación, extracción de datos clave)
- Endpoints API (FastAPI): /subscribe, /jobs, /start-monitoring, /stop-monitoring
- Notificaciones Telegram (evitar duplicados, formato específico)
- Base de datos: jobs y subscribers, índices
- Manejo de errores: tenacity, logging, validación Pydantic, excepciones
- Monitoreo periódico: APScheduler
- Despliegue: Dockerfile, requirements.txt, variables de entorno
- Pruebas y documentación: pytest, Markdown, ejemplos JSON, .env.example

## ChatMode Context
Especializado en scraping y análisis de la página de ofertas de empleo de SIMO, soportando filtros avanzados y extracción de información crítica para postulantes y analistas.

## Action Plan

1. **Diseño y configuración del proyecto**
   - [ ] Crear estructura de carpetas y archivos base (`main.py`, `models.py`, `scraper.py`, etc.)
   - [ ] Configurar entorno virtual y dependencias (`requirements.txt`)
   - [ ] Crear archivo de variables de entorno (`.env.example`)

2. **Implementación del scraper con Playwright**
   - [x] Configurar Playwright para scraping headless/headful
   - [ ] Implementar lógica de navegación y filtrado dinámico (rol, ubicación, fecha de cierre)
   - [ ] Extraer datos requeridos y estructurarlos en JSON
   - [ ] Manejar paginación y sesiones persistentes
   - [ ] Documentar selectores y estrategias genéricas

3. **Modelo de datos y base de datos**
   - [ ] Definir modelos Pydantic y ORM para `jobs` y `subscribers`
   - [ ] Configurar conexión a SQLite/PostgreSQL
   - [ ] Crear migraciones e índices para búsquedas rápidas

4. **API con FastAPI**
   - [ ] Implementar endpoint `POST /subscribe`
   - [ ] Implementar endpoint `GET /jobs`
   - [ ] Implementar endpoint `POST /start-monitoring`
   - [ ] Implementar endpoint `POST /stop-monitoring`
   - [ ] Validar entradas con Pydantic
   - [ ] Proveer ejemplos de respuestas JSON

5. **Notificaciones vía Telegram**
   - [ ] Integrar envío de mensajes usando Telegram Bot API
   - [ ] Evitar notificaciones duplicadas (verificación en base de datos)
   - [ ] Formatear mensajes según requerimiento

6. **Monitoreo periódico y scheduler**
   - [ ] Configurar APScheduler para scraping cada 10 minutos
   - [ ] Detectar y notificar solo nuevas vacantes

7. **Manejo robusto de errores y logging**
   - [ ] Implementar reintentos con tenacity
   - [ ] Configurar logging para errores y eventos clave
   - [ ] Manejar excepciones comunes (timeouts, elementos no encontrados, caídas de conexión)

8. **Despliegue y configuración para Render**
   - [ ] Crear Dockerfile optimizado
   - [ ] Documentar configuración de variables de entorno y Playwright

9. **Pruebas y documentación**
   - [ ] Escribir pruebas unitarias con pytest para endpoints y scraping
   - [ ] Documentar endpoints, flujo de scraping y despliegue (`docs/backend.md`)

## Task Tracking

- [x] Estructura base del proyecto creada
- [ ] Scraper Playwright funcional y documentado
- [ ] Modelos y base de datos operativos
- [ ] Endpoints FastAPI implementados y validados
- [ ] Notificaciones Telegram integradas y sin duplicados
- [ ] Scheduler y monitoreo periódico activos
- [ ] Manejo de errores y logging robusto
- [ ] Dockerfile y despliegue listos para Render
- [ ] Pruebas unitarias y documentación técnica completas
