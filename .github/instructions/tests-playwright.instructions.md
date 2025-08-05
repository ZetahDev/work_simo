---
title: 'Tests con Playwright'
description: 'Guía para realizar pruebas automáticas de la página SIMO utilizando Playwright.'
applyTo: tests/
---

# Tests con Playwright

## Objetivo
Automatizar pruebas de la página SIMO para identificar elementos clave y validar funcionalidad antes de realizar el scraping.

---

## Pasos para los tests

### 1. Instalación de Playwright
```bash
pip install pytest-playwright
playwright install
```

### 2. Creación de test básico
```python
import pytest
from playwright.sync_api import sync_playwright

def test_simo_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://simo.cnsc.gov.co/#ofertaEmpleo")
        assert page.title() == "SIMO - Oferta de Empleo"
        browser.close()
```

### 3. Identificación de elementos
Usa `page.locator` para interactuar con filtros y resultados.

---

## Consideraciones
- **Rendimiento:** Ejecuta tests en modo headless para mayor velocidad.
- **Cobertura:** Valida todos los filtros y elementos relevantes.
- **Integración:** Usa CI/CD para ejecutar tests automáticamente.

---