from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import UI_BASE_URL
from config.settings import VALID_USER, PASSWORD 

class LoginPage(BasePage):
    
    # ----------------------------------------------------
    # 1. LOCALIZADORES 
    # ----------------------------------------------------
    
    # Campos de formulario
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    
    # Botones
    LOGIN_BUTTON = (By.ID, "login-button")
    
    # Mensajes de estado
    ERROR_MESSAGE = (By.XPATH, "//h3[@data-test='error']")
    
    # ----------------------------------------------------
    # 2. MÉTODOS DE ACCIÓN 
    # ----------------------------------------------------

    def go_to_page(self):
        """Navega directamente a la URL base de la aplicación."""
        self.driver.get(UI_BASE_URL)
        self.logger.info(f"Navegando a la página de login: {UI_BASE_URL}")

    def perform_login(self, username: str, password: str):
        """
        Encapsula el proceso de login. 
        Utiliza los métodos robustos de la BasePage.
        """
        self.type_text(self.USERNAME_FIELD, username)
        self.type_text(self.PASSWORD_FIELD, password)
        self.click_element(self.LOGIN_BUTTON)
        self.logger.info(f"Intento de login con usuario: {username}")
        # No hay 'return' acá. El test se va a encargar de verificar el resultado.
        
    def login_with_valid_credentials(self):
        """Helper para realizar un login exitoso usando credenciales válidas."""
        self.go_to_page()
        self.perform_login(VALID_USER, PASSWORD)
        
    def get_login_error_message(self) -> str:
        """Retorna el texto del mensaje de error."""
        return self.get_element_text(self.ERROR_MESSAGE)

    def is_error_message_displayed(self) -> bool:
        """Verifica si el mensaje de error es visible en la página."""
        return self.is_element_displayed(self.ERROR_MESSAGE)



