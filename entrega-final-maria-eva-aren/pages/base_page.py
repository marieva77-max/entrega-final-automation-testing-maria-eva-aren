from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import EXPLICIT_WAIT
from utils.logger import get_logger

class BasePage:
    
    logger = get_logger()

    def __init__(self, driver: WebDriver):
        """
        Constructor de la Base Page. 
        Recibe la instancia del driver inyectada por Pytest.
        """
        self.driver = driver

    #--------------------------------------------------
    # MÉTODOS DE ESPERA
    #--------------------------------------------------

    def _wait_for_element_visible(self, locator: tuple, timeout=EXPLICIT_WAIT):
        """Espera de forma explícita a que un elemento sea visible en la página."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except Exception as e:
            self.logger.error(f"TIEMPO AGOTADO: El elemento con locator {locator} no fue visible en {timeout}s.")
            raise # Relanzar la excepción para que el test falle

    def _wait_for_url_to_be(self, url: str, timeout=EXPLICIT_WAIT) -> bool:
        """Espera a que la URL actual coincida con la esperada."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.url_to_be(url)
            )
        except Exception:
            self.logger.warning(f"La URL '{url}' no se cargó o no coincide dentro del timeout de {timeout}s.")
            return False

    # ----------------------------------------------------
    # MÉTODOS DE INTERACCIÓN
    # ----------------------------------------------------

    def click_element(self, locator: tuple):
        """Espera a que el elemento sea clickeable y luego hace click."""
        try:
            element = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            self.logger.info(f"Clic exitoso en el elemento con locator: {locator}")
        except Exception as e:
            self.logger.error(f"Fallo al intentar hacer click en {locator}: {e}")
            raise

    def type_text(self, locator: tuple, text: str):
        """Espera a que el elemento sea visible, lo limpia y luego escribe el texto."""
        try:
            element = self._wait_for_element_visible(locator)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Texto '{text}' tipeado en el elemento con locator: {locator}")
        except Exception as e:
            self.logger.error(f"Fallo al intentar tipear texto en {locator}: {e}")
            raise
            
    def get_element_text(self, locator: tuple) -> str:
        """Espera a que el elemento sea visible y retorna su texto."""
        try:
            element = self._wait_for_element_visible(locator)
            text = element.text
            self.logger.debug(f"Texto obtenido del elemento {locator}: '{text}'")
            return text
        except Exception as e:
            self.logger.error(f"Fallo al intentar obtener texto de {locator}: {e}")
            raise

    def is_element_displayed(self, locator: tuple) -> bool:
        """Verifica si un elemento es visible sin lanzar excepción si no lo encuentra."""
        try:
            self._wait_for_element_visible(locator, timeout=3) # Usamos un timeout corto
            return True
        except Exception:
            return False


