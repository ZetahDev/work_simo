---
title: 'Implementación en Python con BeautifulSoup'
description: 'Guía para realizar el scraping de SIMO utilizando Python y la librería BeautifulSoup.'
applyTo: scraping/
---

# Implementación en Python con BeautifulSoup

## Objetivo
Extraer datos relevantes de la página SIMO utilizando Python y BeautifulSoup, aplicando filtros avanzados y estructurando la información.

---

## Pasos para el scraping

### 1. Instalación de dependencias
```bash
pip install requests beautifulsoup4
```

### 2. Acceso a la página
Utiliza `requests` para realizar peticiones HTTP y obtener el HTML de la página.
```python
import requests
from bs4 import BeautifulSoup

url = "https://simo.cnsc.gov.co/#ofertaEmpleo"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
```

### 3. Identificación de elementos
Usa `soup.find` y `soup.find_all` para localizar los datos de interés (fecha de cierre, requisitos, etc.).

### 4. Filtrado de datos
Implementa funciones para aplicar filtros como concurso, departamento, salario, etc.

---

## Consideraciones
- **Autenticación:** Si la página requiere login, utiliza `requests.Session`.
- **Paginación:** Maneja múltiples páginas si los resultados están distribuidos.
- **Actualización:** Monitorea cambios en la estructura del HTML.

---