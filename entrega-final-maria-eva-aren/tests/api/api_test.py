import pytest
from utils.logger import get_logger

logger = get_logger()

# Aplico el marcador 'api' a toda la clase
@pytest.mark.api 
class TestApiJsonPlaceholder:

    # ----------------------------------------------------
    # PRUEBA 1: GET (Lectura y validación de estructura)
    # ----------------------------------------------------
    
    def test_get_single_post_status_and_content(self, api_client):
        """
        Verifica la solicitud GET para un post específico.
        Valida el status code (200) y la presencia de claves en el JSON.
        """
        logger.info("Iniciando test_get_single_post_status_and_content")
        endpoint = "/posts/1"
        
        # 1. Acción: Ejecutar la petición GET
        response = api_client.get(endpoint)
        
        # 2. Verificación de Status Code
        assert response.status_code == 200, f"FAIL: Status code no es 200. Recibido: {response.status_code}"
        
        # 3. Verificación de Contenido y Estructura JSON
        data = response.json()
        assert isinstance(data, dict), "FAIL: La respuesta no es un objeto JSON."
        assert data.get('id') == 1, "FAIL: El ID del post no coincide."
        assert 'userId' in data and 'title' in data and 'body' in data, "FAIL: Faltan claves esenciales en el JSON."
        
        logger.info("Prueba GET exitosa. Status y estructura JSON validados.")


    # ----------------------------------------------------
    # PRUEBA 2: POST (Creación de recurso)
    # ----------------------------------------------------
    
    def test_create_new_post(self, api_client):
        """
        Verifica la solicitud POST para crear un nuevo recurso.
        Valida el status code (201) y que el body retornado contenga los datos enviados.
        """
        logger.info("Iniciando test_create_new_post")
        endpoint = "/posts"
        new_post_data = {
            'title': 'Test Post Automation',
            'body': 'Contenido creado por QA Mentor.',
            'userId': 1
        }
        
        # 1. Acción: Ejecutar la petición POST con los datos JSON
        response = api_client.post(endpoint, json=new_post_data)
        
        # 2. Verificación de Status Code (201 Created)
        assert response.status_code == 201, f"FAIL: Status code no es 201. Recibido: {response.status_code}"
        
        # 3. Verificación de Contenido JSON
        response_data = response.json()
        assert response_data.get('id') is not None, "FAIL: El ID retornado es nulo."
        # Se espera que el servicio devuelva un "echo" de los datos enviados
        assert response_data.get('title') == new_post_data['title'], "FAIL: El título retornado no coincide con el enviado."
        
        logger.info(f"Prueba POST exitosa. Nuevo recurso creado con ID: {response_data.get('id')}")


    # ----------------------------------------------------
    # PRUEBA 3: DELETE (Eliminación de recurso)
    # ----------------------------------------------------

    def test_delete_post(self, api_client):
        """
        Verifica la solicitud DELETE para eliminar un recurso.
        Valida el status code (200 o 204).
        """
        logger.info("Iniciando test_delete_post")
        post_id_to_delete = 1 
        endpoint = f"/posts/{post_id_to_delete}"
        
        # 1. Acción: Ejecutar la petición DELETE
        response = api_client.delete(endpoint)
        
        # 2. Verificación de Status Code
        # DELETE puede retornar 200 (OK) o 204 (No Content). JSONPlaceholder retorna 200.
        assert response.status_code in [200, 204], f"FAIL: Status code no es 200/204. Recibido: {response.status_code}"
        
        # 3. Verificación de Body (Debe estar vacío o ser un JSON vacío)
        try:
            # Si el texto de respuesta está vacío, la eliminación fue efectiva según JSONPlaceholder
            assert not response.text or response.json() == {}, "FAIL: El cuerpo de la respuesta no está vacío después de DELETE."
        except requests.JSONDecodeError:
             # Maneja el caso de que response.text no sea JSON (body vacío)
            assert not response.text, "FAIL: La respuesta no está vacía y no es JSON válido."

        logger.info(f"Prueba DELETE exitosa para el post ID: {post_id_to_delete}. Status: {response.status_code}")

