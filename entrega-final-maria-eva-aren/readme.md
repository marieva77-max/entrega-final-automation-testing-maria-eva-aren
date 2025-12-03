# Proyecto Final QA Automation con Python

Este proyecto está construido desde cero, utilizando Python, Pytest, Selenium WebDriver y Requests, siguiendo el patrón de diseño **Page Object Model (POM)**.

El objetivo es demostrar la capacidad de crear una solución de automatización robusta, con separación de lógica, gestión avanzada de fixtures, logging y reportes automáticos.

---

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Framework de Testing:** Pytest
* **Web Automation:** Selenium WebDriver
* **API Testing:** Requests
* **Reportes:** Pytest-HTML
* **Patrón de Diseño:** Page Object Model (POM)
* **Control de Versiones:** Git / GitHub

---

## Estructura del Proyecto

El proyecto sigue una estructura modular y organizada para desacoplar la configuración, la lógica de la página, las utilidades y los tests.

```text
proyecto-final/
├─ config/         # Archivos de configuración global (URLs, credenciales).
├─ pages/          # Clases Page Object Model (POM).
├─ tests/          # Contiene los tests (separados por UI y API).
├─ utils/          # Clases de soporte (Logger, Driver Factory, API Client).
├─ screenshots/    # Capturas de pantalla automáticas en caso de fallo UI.
├─ reports/        # Reportes HTML generados.
├─ conftest.py     # Fixtures y hooks principales de Pytest.
├─ pytest.ini      # Configuración de marcadores y reportes.
└─ requirements.txt# Dependencias.

