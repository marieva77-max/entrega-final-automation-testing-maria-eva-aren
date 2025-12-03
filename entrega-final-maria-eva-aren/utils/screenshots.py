import os
from datetime import datetime
from config.settings import SCREENSHOTS_DIR
from utils.logger import get_logger

logger = get_logger()

def take_screenshot(driver, test_name):
    """
    Toma una captura de pantalla y la guarda con un timestamp único.
    :param driver: La instancia del WebDriver.
    :param test_name: Nombre del test que falló.
    """
    if not os.path.exists(SCREENSHOTS_DIR):
        os.makedirs(SCREENSHOTS_DIR)

    # Genera un nombre de archivo único con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{test_name.replace('/', '_').replace(':', '_')}_{timestamp}.png"
    file_path = os.path.join(SCREENSHOTS_DIR, file_name)

    try:
        driver.save_screenshot(file_path)
        logger.error(f"Captura guardada en: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error al intentar tomar la captura de pantalla: {e}")
        return None



