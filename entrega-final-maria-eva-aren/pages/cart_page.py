from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    
    # ----------------------------------------------------
    # 1. LOCALIZADORES 
    # ----------------------------------------------------
    
    # Verificación de Página
    PAGE_TITLE = (By.CLASS_NAME, "title") # Debe contener el texto "Your Cart"
    
    # Lista de productos en el carrito
    CART_ITEMS_LIST = (By.CLASS_NAME, "cart_item")
    
    # Botones de navegación
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    
    # Localizador genérico para el nombre de un producto (usado para validar)
    ITEM_NAME_GENERIC = (By.CLASS_NAME, "inventory_item_name")
    
    # ----------------------------------------------------
    # 2. MÉTODOS DE ACCIÓN 
    # ----------------------------------------------------

    def is_page_loaded(self) -> bool:
        """
        Verifica si la página ha cargado correctamente 
        revisando el texto del título principal.
        """
        self.logger.info("Verificando que la página del Carrito esté cargada.")
        try:
            title_text = self.get_element_text(self.PAGE_TITLE)
            return title_text == "Your Cart"
        except Exception:
            return False

    def get_number_of_items_in_cart(self) -> int:
        """
        Cuenta la cantidad de elementos de producto listados en el carrito.
        """
        # Intentamos esperar a que la lista de ítems sea visible
        try:
            items = self.driver.find_elements(*self.CART_ITEMS_LIST)
            return len(items)
        except Exception as e:
            self.logger.warning(f"No se encontraron ítems en el carrito. Error: {e}")
            return 0

    def is_product_in_cart(self, product_name: str) -> bool:
        """
        Verifica si un producto específico está presente en el carrito.
        Busca el nombre del producto en todos los nombres listados.
        """
        # Se buscan todos los elementos que contengan el nombre del producto
        # Esto busca por texto usando XPATH,
        # es útil para verificar contenido dinámico.
        xpath_locator = (By.XPATH, f"//div[@class='inventory_item_name' and text()='{product_name}']")
        
        if self.is_element_displayed(xpath_locator):
            self.logger.info(f"El producto '{product_name}' ha sido encontrado en el carrito.")
            return True
        else:
            self.logger.warning(f"El producto '{product_name}' NO se encuentra en el carrito.")
            return False

    def click_checkout_button(self):
        """Hace clic en el botón de Checkout para ir al formulario de información."""
        self.click_element(self.CHECKOUT_BUTTON)
        self.logger.info("Navegando al formulario de Checkout.")


