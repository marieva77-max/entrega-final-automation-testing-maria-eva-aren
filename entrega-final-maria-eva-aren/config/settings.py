import os

# URLs Base
UI_BASE_URL = "https://www.saucedemo.com"
API_BASE_URL = "https://jsonplaceholder.typicode.com"

# Credenciales de SauceDemo
VALID_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PASSWORD = "secret_sauce"

# Tiempos de espera (en segundos)
IMPLICIT_WAIT = 5    # Espera implícita general
EXPLICIT_WAIT = 10   # Espera explícita para elementos específicos
PAGE_LOAD_TIMEOUT = 30

# Directorios (rutas absolutas para evitar problemas)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
