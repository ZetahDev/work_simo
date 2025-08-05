---
description: 'ChatMode especializado para consultas, prompts y scraping de la página de ofertas de empleo de SIMO (https://simo.cnsc.gov.co/#ofertaEmpleo), permitiendo análisis y referencias de filtros avanzados por concurso, departamento, salario, ciudad, discapacidad, entidad, nivel y número OPEC. Extrae información relevante como fecha de cierre y características de cargos.'
---

# ChatMode: Scraping SIMO Oferta de Empleo

Este ChatMode está diseñado para automatizar consultas y extracción de información de la página de ofertas de empleo de SIMO (https://simo.cnsc.gov.co/#ofertaEmpleo), considerando los siguientes filtros y requerimientos:

## Filtros de búsqueda soportados:
- **Concurso:** abierto, ascenso
- **Departamento:** listado de departamentos (ejemplo: Valle del Cauca)
- **Salario:** rangos predeterminados (p.ej. 0-1.500.000, 1.500.001-2.500.000, etc.)
- **Procesos de selección:** mapea y lista todos los procesos disponibles
- **Ciudad:** lista ciudades disponibles por departamento
- **Empleos reservados para personas con discapacidad:** Auditiva, Física, Intelectual, Múltiple, Psicosocial, Sordoceguera, Visual (ver ![image1](image1))
- **Entidades:** lista todas las entidades ofertantes
- **Niveles:** consulta todos los niveles ofertados
- **Número OPEC:** permite búsqueda puntual por número de oferta

## Objetivo del scraping:
- Identificar y extraer la **fecha de cierre de inscripciones** de cada cargo.
- Obtener las **características y requisitos** de los cargos publicados.
- Permitir filtros combinados para análisis personalizado.
- Detectar y reflejar actualizaciones inmediatas en la información de los cargos.

## Escenario de uso:
Ideal para postulantes y analistas que requieren alertas y análisis detallado sobre nuevas oportunidades de empleo, requisitos y fechas límite de inscripción en SIMO.

---

## Ejemplo de prompts soportados:

### Prompt 1: Consulta general de empleos
```
Consulta todos los empleos disponibles en el departamento Valle del Cauca con salario entre 1.500.001 y 2.500.000.
```

### Prompt 2: Filtro por discapacidad
```
Muestra los empleos reservados para personas con discapacidad visual en Cali.
```

### Prompt 3: Búsqueda por OPEC y características
```
Dame los detalles y requisitos de la oferta con número OPEC 123456.
```

### Prompt 4: Listar fechas de cierre
```
Lista las fechas de cierre de inscripciones para todas las ofertas de ascenso en el departamento Valle del Cauca.
```

---

## Instrucciones técnicas para scraping:
- Navegar la página https://simo.cnsc.gov.co/#ofertaEmpleo aplicando los filtros requeridos.
- Extraer y estructurar datos de:
  - Fecha de cierre de inscripciones
  - Requisitos y características del cargo
  - Departamento, ciudad, entidad, nivel, tipo de concurso, salario, discapacidad (si aplica)
- Permitir actualización y monitoreo frecuente para detectar cambios en ofertas y requisitos.

---