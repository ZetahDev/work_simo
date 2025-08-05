---
title: 'Integración del Bot de Telegram'
description: 'Guía para desarrollar e integrar un bot de Telegram que permita consultas y análisis de datos obtenidos del scraping de SIMO.'
applyTo: telegram/
---

# Integración del Bot de Telegram

## Objetivo
Desarrollar un bot de Telegram que permita realizar consultas sobre ofertas de empleo en SIMO y recibir información procesada directamente desde el backend con AI.

---

## Funcionalidades principales
1. **Consultas personalizadas:**
   - Filtros por concurso, departamento, salario, ciudad, discapacidad, entidad, nivel y número OPEC.
   - Respuestas claras y estructuradas sobre fecha de cierre, requisitos y características del cargo.

2. **Alertas automáticas:**
   - Notificaciones sobre nuevas ofertas o cambios relevantes.

3. **Recomendaciones AI:**
   - Generación de sugerencias personalizadas basadas en el perfil del usuario.

---

## Tecnologías utilizadas
- **Python:** Para desarrollo del bot.
- **Telegram Bot API:** Para comunicación con Telegram.
- **Backend AI:** Conexión vía API REST.

---

## Flujo de interacción
1. Usuario envía consulta al bot.
2. Bot procesa y envía la solicitud al backend.
3. Backend responde con datos procesados.
4. Bot muestra resultados y recomendaciones al usuario.

---

## Ejemplo de comandos soportados
- `/buscar concurso abierto departamento Valle del Cauca salario 1500001-2500000`
- `/alertas activar`
- `/recomendaciones perfil profesional`

---

## Consideraciones
- **Rendimiento:** Optimizar consultas para respuesta rápida.
- **Usabilidad:** Diseñar comandos intuitivos y fáciles de usar.
- **Seguridad:** Proteger datos personales y evitar abusos.

---