from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    
    # ----------------------------------------------------
    # 1. LOCALIZADORES 
    # ----------------------------------------------------
    
    # Verificación de Página
    PAGE_TITLE = (By.CLASS_NAME, "title") # Debe contener el texto "Products"
    
    # Carrito y navegación
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    
    # Botones de productos (Uso un par para los tests)
    BACKPACK_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    BIKE_LIGHT_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-bike-light")
    
    # ----------------------------------------------------
    # 2. MÉTODOS DE ACCIÓN 
    # ----------------------------------------------------

    def is_page_loaded(self) -> bool:
        """
        Verifica si la página ha cargado correctamente 
        revisando el texto del título principal.
        """
        self.logger.info("Verificando que la página de Inventario esté cargada.")
        try:
            title_text = self.get_element_text(self.PAGE_TITLE)
            return title_text == "Products"
        except Exception:
            return False

    def add_backpack_to_cart(self):
        """Añade la mochila (Sauce Labs Backpack) al carrito de compras."""
        self.click_element(self.BACKPACK_ADD_BUTTON)
        self.logger.info("Producto: Mochila añadida al carrito.")

    def add_bike_light_to_cart(self):
        """Añade la luz de bicicleta (Sauce Labs Bike Light) al carrito de compras."""
        self.click_element(self.BIKE_LIGHT_ADD_BUTTON)
        self.logger.info("Producto: Luz de bicicleta añadida al carrito.")

    def get_cart_count(self) -> str:
        """
        Retorna la cantidad de ítems mostrada en el badge del carrito.
        Retorna "0" si el badge no es visible (carrito vacío).
        """
        if self.is_element_displayed(self.SHOPPING_CART_BADGE):
            return self.get_element_text(self.SHOPPING_CART_BADGE)
        return "0"

    def go_to_cart(self):
        """Navega a la página del carrito haciendo clic en el icono."""
        self.click_element(self.SHOPPING_CART_LINK)
        self.logger.info("Navegando al Carrito de Compras.")


