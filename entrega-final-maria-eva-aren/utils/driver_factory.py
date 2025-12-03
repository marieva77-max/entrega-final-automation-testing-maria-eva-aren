from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class DriverFactory:
    @staticmethod
    def get_driver(browser="chrome"):
        """
        Inicializa y retorna una instancia de WebDriver.
        Por defecto usa Chrome, pero se prepara para escalabilidad.
        """
        driver = None
        
        if browser.lower() == "chrome":
            # Opciones de configuración para Chrome
            options = Options()
            options.add_argument("--start-maximized") # Iniciar maximizado
            options.add_argument("--ignore-certificate-errors") # Ignorar errores SSL
            
            # options.add_argument("--headless") 
            # options.add_argument("--no-sandbox")
            # options.add_argument("--disable-dev-shm-usage")

            # Inicialización del driver
            driver = webdriver.Chrome(options=options)
        
        elif browser.lower() == "firefox":
            # Esto sería la lógica para Firefox de ser necesario
            driver = webdriver.Firefox()
            
        else:
            raise ValueError(f"Navegador no soportado: {browser}")
            
        # Configuración global de esperas implícitas (backup safety net)
        # Es preferible usar esperas explícitas en los Page Objects, 
        # pero esto ayuda con cargas lentas inesperadas.
        driver.implicitly_wait(5)
        
        return driver

