---
title: 'Instrucciones para Scraping de SIMO'
description: 'Instrucciones técnicas y consideraciones clave para implementar un scraping efectivo en la página de oferta de empleos de SIMO, considerando múltiples filtros y extracción de información crítica.'
applyTo: instructions/
---

# Instrucciones para scraping en SIMO

## 1. Acceso y navegación
- Ingresa a https://simo.cnsc.gov.co/#ofertaEmpleo
- Asegúrate de cargar completamente los filtros y resultados antes de extraer datos

## 2. Aplicación de filtros
- Identifica y utiliza correctamente los filtros disponibles: concurso, departamento, ciudad, salario, proceso de selección, entidad, nivel, discapacidad, número OPEC
- Los filtros de discapacidad admiten: Auditiva, Física, Intelectual, Múltiple, Psicosocial, Sordoceguera, Visual

## 3. Extracción de datos
- Por cada oferta encontrada, extrae:
  - Fecha de cierre de inscripciones
  - Requisitos y características del cargo
  - Salario estimado
  - Entidad ofertante
  - Departamento y ciudad
  - Nivel y tipo de concurso
  - Si aplica, reserva para discapacidad (tipo)
  - Número OPEC

## 4. Actualización y monitoreo
- Repite la extracción periódicamente para detectar nuevas ofertas o cambios en las existentes
- Almacena un historial de cambios para alertar sobre actualizaciones relevantes

## 5. Consideraciones éticas y legales
- Respeta los términos de uso y políticas de la plataforma SIMO
- Usa la información solo para fines de análisis y postulación personal

---