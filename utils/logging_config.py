import logging
import os
from pathlib import Path

def setup_logging(log_file=None):
    """Configura el sistema de logging para la aplicación."""
    
    # Formato de los logs
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_format, date_format)

    # Logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Limpiar handlers existentes si los hay
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Handler para archivo si se proporciona
    if log_file:
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            print(f"No se pudo configurar el logging en archivo: {e}")

    # Evitar ruidos de librerías externas
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("groq").setLevel(logging.INFO)

def get_logger(name):
    """Devuelve un logger con el nombre especificado."""
    return logging.getLogger(name)
