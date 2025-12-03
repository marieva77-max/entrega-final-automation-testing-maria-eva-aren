import requests
from config.settings import API_BASE_URL
from utils.logger import get_logger

class ApiClient:
    """
    Cliente genérico para interactuar con la API REST.
    Encapsula la librería requests y añade logging.
    """
    
    logger = get_logger()

    def __init__(self, base_url=API_BASE_URL):
        """Inicializa el cliente con la URL base de la API."""
        self.base_url = base_url
        self.session = requests.Session()
        # Se puede añadir una cabecera global de ser necesario (x ej: Authorization)
        # self.session.headers.update({'Accept': 'application/json'})

    def _request(self, method: str, endpoint: str, **kwargs):
        """
        Método privado genérico para ejecutar peticiones HTTP.
        :param method: Método HTTP (GET, POST, DELETE, etc.)
        :param endpoint: Ruta específica de la API (ej: /posts)
        :param kwargs: Argumentos adicionales pasados a requests (data, json, params, headers)
        :return: Objeto Response de requests.
        """
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"-> API Request: {method} {url}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            self.logger.info(f"<- API Response: {response.status_code} - Tiempo: {response.elapsed.total_seconds():.3f}s")
            response.raise_for_status() # Tira una excepción si el status code indica error (4xx o 5xx)
            return response
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"Error HTTP en {method} {url}: {e}")
            return e.response # Retorna la respuesta de error para que el test la valide
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"Error de conexión en {url}: {e}")
            raise # Tira la excepción para que Pytest marque el test como error


    def get(self, endpoint: str, params=None):
        """Implementa la petición GET."""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data=None, json=None):
        """Implementa la petición POST."""
        # JSONPlaceholder requiere la cabecera Content-Type para POST/PUT/PATCH
        headers = {'Content-type': 'application/json; charset=UTF-8'}
        return self._request("POST", endpoint, data=data, json=json, headers=headers)

    def delete(self, endpoint: str):
        """Implementa la petición DELETE."""
        return self._request("DELETE", endpoint)
    
    def close_session(self):
        """Cierra la sesión de requests (buena práctica)."""
        self.session.close()

