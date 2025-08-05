---
title: 'Prompts de Scraping para SIMO'
description: 'Colección de prompts para interactuar y extraer información de la página de ofertas de empleo de SIMO, con filtros avanzados y ejemplos de uso para cada caso.'
applyTo: prompts/
---

# Prompts de ejemplo para scraping en SIMO

Utiliza estos prompts para automatizar consultas y extracción de información relevante de los empleos ofertados en SIMO:

## Filtros disponibles:
- Concurso: abierto, ascenso
- Departamento: cualquier departamento disponible
- Ciudad: ciudades filtradas por departamento
- Salario: selecciona uno o varios rangos (ver lista)
- Procesos de selección: mapea todos los procesos activos
- Entidades: consulta entidades ofertantes
- Niveles: todos los niveles ofertados
- Empleos reservados para discapacidad: Auditiva, Física, Intelectual, Múltiple, Psicosocial, Sordoceguera, Visual
- Número OPEC: búsqueda puntual

---

## Ejemplos de prompts:

1. **Consulta por concurso y salario:**
   ```
   Filtra todos los empleos de concurso abierto en el Valle del Cauca con salario superior a 3.500.000.
   ```
2. **Consulta por discapacidad:**
   ```
   ¿Qué empleos hay reservados para personas con discapacidad intelectual en Palmira?
   ```
3. **Consulta por entidad y nivel:**
   ```
   Muéstrame las ofertas de la entidad "Gobernación del Valle del Cauca" para nivel profesional.
   ```
4. **Consulta por fecha de cierre:**
   ```
   Lista las ofertas cuyo cierre de inscripciones sea esta semana en el Valle del Cauca.
   ```
5. **Consulta por número OPEC:**
   ```
   ¿Cuáles son los requisitos del empleo con número OPEC 7891011?
   ```

---

## Observaciones:

- Puedes combinar varios filtros en una sola consulta.
- Siempre extrae la fecha de cierre y características del cargo en los resultados.
- Usa los nombres de discapacidad según la lista proporcionada en ![image1](image1).

---