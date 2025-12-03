from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    
    # ----------------------------------------------------
    # 1. LOCALIZADORES 
    # ----------------------------------------------------
    
    # Verificación de Página
    PAGE_TITLE = (By.CLASS_NAME, "title") # Título cambia en cada paso
    
    # Campos de información 
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    
    # Botones de navegación
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    
    # Mensaje de éxito 
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    
    # ----------------------------------------------------
    # 2. MÉTODOS DE ACCIÓN 
    # ----------------------------------------------------
    
    
    def is_info_page_loaded(self) -> bool:
        """Verifica si la página de información de envío está cargada."""
        return self.get_element_text(self.PAGE_TITLE) == "Checkout: Your Information"

    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        """Rellena el formulario de información de envío y continúa."""
        self.type_text(self.FIRST_NAME_FIELD, first_name)
        self.type_text(self.LAST_NAME_FIELD, last_name)
        self.type_text(self.POSTAL_CODE_FIELD, postal_code)
        self.logger.info(f"Información de envío rellenada: {first_name}, {last_name}, {postal_code}")
        self.click_element(self.CONTINUE_BUTTON)
        
    

    def is_overview_page_loaded(self) -> bool:
        """Verifica si la página de resumen de compra está cargada."""
        return self.get_element_text(self.PAGE_TITLE) == "Checkout: Overview"

    def finish_checkout(self):
        """Finaliza el proceso de compra haciendo clic en el botón 'Finish'."""
        self.click_element(self.FINISH_BUTTON)
        self.logger.info("Compra finalizada.")

    
        
    def is_complete_page_loaded(self) -> bool:
        """Verifica si la página de confirmación de compra está cargada."""
        return self.get_element_text(self.PAGE_TITLE) == "Checkout: Complete!"
            
    def get_complete_header(self) -> str:
        """Retorna el mensaje de éxito de la compra (ej: 'Thank you for your order!')."""
        return self.get_element_text(self.COMPLETE_HEADER)


