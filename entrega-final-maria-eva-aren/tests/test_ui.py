import pytest
from selenium.webdriver.common.by import By # Necesario si uso locators directos en tests
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.settings import VALID_USER, LOCKED_OUT_USER, PASSWORD
from utils.logger import get_logger

logger = get_logger()

# Aplicamos el marcador 'ui' a toda la clase para una fácil ejecución selectiva
@pytest.mark.ui 
class TestUISauceDemo:

    # ----------------------------------------------------
    # ESCENARIOS POSITIVOS (Flujos principales)
    # ----------------------------------------------------
    
    def test_01_successful_login(self, driver):
        """
        Prueba 1: Verifica que el usuario estándar pueda iniciar sesión correctamente 
        y la página de inventario cargue.
        """
        logger.info("Iniciando test_01_successful_login")
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        # 1. Acción: Navegar e iniciar sesión
        login_page.login_with_valid_credentials()

        # 2. Verificación: Asegurar que la página de Inventario ha cargado
        assert inventory_page.is_page_loaded(), "ERROR: La página de Inventario no cargó después del login."
        logger.info("Verificación de login exitoso completada.")


    def test_02_complete_purchase_flow(self, driver):
        """
        Prueba 2: Flujo completo de E2E: Login, Agregar productos, Checkout y Compra finalizada.
        """
        logger.info("Iniciando test_02_complete_purchase_flow")
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)

        # 1. Login
        login_page.login_with_valid_credentials()
        
        # 2. Agregar Productos y verificar el contador 
        inventory_page.add_backpack_to_cart()
        inventory_page.add_bike_light_to_cart()
        assert inventory_page.get_cart_count() == "2", "ERROR: El contador del carrito no es '2'."

        # 3. Ir al Carrito y verificar productos
        inventory_page.go_to_cart()
        assert cart_page.is_page_loaded(), "ERROR: No se cargó la página del Carrito."
        assert cart_page.is_product_in_cart("Sauce Labs Backpack"), "ERROR: Mochila no encontrada en el carrito."

        # 4. Checkout - Información
        cart_page.click_checkout_button()
        assert checkout_page.is_info_page_loaded(), "ERROR: No se cargó la página de información de Checkout."
        checkout_page.fill_information("Tester", "Automated", "12345")

        # 5. Checkout - Resumen y Finalización
        assert checkout_page.is_overview_page_loaded(), "ERROR: No se cargó la página de resumen de Checkout."
        checkout_page.finish_checkout()

        # 6. Verificación Final de Éxito
        assert checkout_page.is_complete_page_loaded(), "ERROR: No se cargó la página de confirmación de compra."
        success_message = checkout_page.get_complete_header()
        assert "Thank you for your order!" in success_message, "ERROR: Mensaje de confirmación incorrecto."
        logger.info("Flujo de compra completado y verificado exitosamente.")
        
    def test_03_add_and_remove_item(self, driver):
        """
        Prueba 3: Agrega un item y lo remueve desde la página de Inventario.
        """
        logger.info("Iniciando test_03_add_and_remove_item")
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        
        # El botón de remover para la mochila tiene el ID: remove-sauce-labs-backpack
        REMOVE_BUTTON = (By.ID, "remove-sauce-labs-backpack")

        # 1. Login y Añadir producto
        login_page.login_with_valid_credentials()
        inventory_page.add_backpack_to_cart()
        assert inventory_page.get_cart_count() == "1", "ERROR: Ítem no añadido al carrito."
        
        # 2. Remover el producto
        inventory_page.click_element(REMOVE_BUTTON)

        # 3. Verificación: El contador del carrito debe ser "0"
        assert inventory_page.get_cart_count() == "0", "ERROR: Ítem no removido del carrito, el contador no es 0."
        logger.info("Adición y remoción verificados.")


    # ----------------------------------------------------
    # ESCENARIOS NEGATIVOS (Requisito: por lo menos 1)
    # ----------------------------------------------------

    def test_04_login_locked_out_user(self, driver):
        """
        Prueba 4: Verifica el escenario negativo: usuario bloqueado.
        """
        logger.info("Iniciando test_04_login_locked_out_user (Negativo)")
        login_page = LoginPage(driver)

        # 1. Acción: Intentar iniciar sesión con credenciales bloqueadas
        login_page.go_to_page()
        login_page.perform_login(LOCKED_OUT_USER, PASSWORD)

        # 2. Verificación: Asegurar que el mensaje de error correcto es visible
        assert login_page.is_error_message_displayed(), "ERROR: El mensaje de error no apareció."
        error_message = login_page.get_login_error_message()
        assert "Epic sadface: Sorry, this user has been locked out." in error_message
        logger.info("Escenario Negativo de usuario bloqueado verificado.")


    def test_05_login_empty_password(self, driver):
        """
        Prueba 5: Verifica el escenario negativo: contraseña vacía.
        """
        logger.info("Iniciando test_05_login_empty_password (Negativo)")
        login_page = LoginPage(driver)

        # 1. Acción: Intentar iniciar sesión sin contraseña
        login_page.go_to_page()
        login_page.perform_login(VALID_USER, "")

        # 2. Verificación: Asegurar que el mensaje de error es visible
        assert login_page.is_error_message_displayed(), "ERROR: El mensaje de error no apareció."
        error_message = login_page.get_login_error_message()
        assert "Epic sadface: Password is required" in error_message
        logger.info("Escenario Negativo de contraseña vacía verificado.")


