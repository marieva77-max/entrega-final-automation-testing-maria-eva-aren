import pytest
from utils.driver_factory import DriverFactory
from utils.screenshots import take_screenshot
from utils.logger import get_logger

# Inicializa el logger para conftest
logger = get_logger()

@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture que inicializa el WebDriver y maneja el teardown (cierre).
    Se usa el scope 'function' para asegurar un navegador limpio por cada test.
    """
    logger.info("Inicializando WebDriver...")
    # 1. SETUP: Inicializa el driver
    web_driver = DriverFactory.get_driver(browser="chrome")
    
    # 2. PROVISIÓN: Cede el control del driver al test
    yield web_driver
    
    # 3. TEARDOWN: Se ejecuta después de que el test termina
    logger.info("Cerrando WebDriver...")
    web_driver.quit()

# ----------------------------------------------------
# HOOKS DE PYTEST - Captura Automática en Fallo
# ----------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest Hook que se ejecuta después de la fase de 'call' de un test.
    Permite actuar cuando un test falla.
    """
    # 1. Ejecuta el hook estándar y obtiene el resultado del reporte
    outcome = yield
    report = outcome.get_result()

    # 2. Verifica si el test falló y estamos en la fase de ejecución ('call')
    if report.when == 'call' and report.failed:
        logger.error(f"El test {report.nodeid} ha fallado. Intentando tomar captura...")
        
        # Intenta acceder al objeto driver si fue solicitado por el test
        try:
            # item.funcargs contiene los fixtures usados por el test
            driver = item.funcargs['driver'] 
            test_name = report.nodeid.replace("::", "_") # Nombre para la captura
            
            # Llama a la utilidad de captura
            take_screenshot(driver, test_name)
            
        except KeyError:
            # Esto pasa si el test fallido no usó el fixture 'driver' (ej: tests API)
            logger.warning("El test fallido no usó el fixture 'driver'. No se tomó captura.")
        except Exception as e:
            logger.error(f"Error inesperado al intentar manejar el fallo y la captura: {e}")



# from utils.driver_factory import DriverFactory
# from utils.screenshots import take_screenshot
# from utils.logger import get_logger
# import pytest
# ...
# ----------------------------------------------------------------------------------

# Importación específica para las pruebas de API
from utils.api_client import ApiClient

@pytest.fixture(scope="session")
def api_client():
    """
    Fixture que inicializa el ApiClient (Requests) y maneja el teardown (cierre de sesión).
    El scope 'session' asegura que una sola instancia del cliente se use para todas las pruebas de API.
    """
    logger.info("Inicializando ApiClient para pruebas de API...")
    # 1. SETUP: Inicializa el cliente
    client = ApiClient()
    
    # 2. PROVISIÓN: Le da el control del cliente al test
    yield client
    
    # 3. TEARDOWN: Se ejecuta después de que todos los tests de la sesión han terminado
    logger.info("Cerrando sesión del ApiClient...")
    client.close_session()

# Los hooks de screenshot/reporte ya se definieron antes (pytest_runtest_makereport)
# seguirán funcionando para las pruebas de UI sin interferir con las pruebas de API.

