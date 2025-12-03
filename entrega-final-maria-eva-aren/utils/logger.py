import logging
import inspect

def get_logger(log_level=logging.INFO):
    """
    Configura y devuelve una instancia de logger.
    El nombre del logger será el nombre de la función o clase que lo llame.
    """
    # Obtiene el nombre de la función/método que llamó a get_logger
    logger_name = inspect.stack()[1][3]
    
    # Crea el logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    
    # Evita duplicar handlers si ya existen
    if not logger.handlers:
        # Crea un manejador para consola
        console_handler = logging.StreamHandler()
        
        # Define el formato del log: Hora - Nivel - Mensaje
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
        
        # Añade el manejador al logger
        logger.addHandler(console_handler)
        
    return logger

