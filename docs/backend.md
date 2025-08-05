# SIMO Scraping Backend

Documentación técnica del backend para scraping de ofertas de empleo en SIMO.

## Endpoints

- POST /subscribe
- GET /jobs
- POST /start-monitoring
- POST /stop-monitoring

## Flujo de scraping

- Navegación dinámica con Playwright
- Extracción de vacantes filtradas
- Almacenamiento en base de datos
- Notificaciones vía Telegram

## Despliegue

- Dockerfile y variables de entorno
- Requisitos para Render
