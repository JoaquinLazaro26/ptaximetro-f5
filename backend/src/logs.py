import logging
from logging.handlers import RotatingFileHandler
import sys

# Configuración constante
LOG_FILENAME = "taximetro.log"

def configurar_logging():
    """Configura el logging para escribir en archivo y consola."""
    
    # 1. Definir el formato profesional
    log_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s'
    )

    # 2. Crear el Handler de Archivo (Rotativo)
    file_handler = RotatingFileHandler(
        LOG_FILENAME, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    # 3. Crear Handler de Consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    # 4. Obtener el Logger Raíz (Root)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # --- FIX CRÍTICO PARA UVICORN ---
    # Uvicorn ya añade handlers al iniciar.
    # En lugar de comprobar "if not handlers", limpiamos los antiguos 
    # o simplemente añadimos el nuestro asegurándonos de no duplicar el de archivo.
    
    # Verificamos si ya existe un FileHandler para no añadirlo doble al recargar
    file_handlers_existentes = [h for h in root_logger.handlers if isinstance(h, RotatingFileHandler)]
    
    if not file_handlers_existentes:
        root_logger.addHandler(file_handler)
        # Opcional: Añadimos consola también para ver nuestro formato, 
        # aunque Uvicorn ya tiene el suyo. Esto fuerza nuestro formato bonito.
        root_logger.addHandler(console_handler)
        
    logging.info("✅ Sistema de Logging (re)inicializado correctamente.")