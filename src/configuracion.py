import json
import os
import sys

ARCHIVO_CONFIG = 'config.json'

def cargar_configuracion():
    """Carga la configuración desde el archivo JSON."""
    if not os.path.exists(ARCHIVO_CONFIG):
        return {"tarifa_parado": 0.02, "tarifa_movimiento": 0.05, "moneda": "€"}
        
    try:
        with open(ARCHIVO_CONFIG, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    except Exception:
        return {"tarifa_parado": 0.02, "tarifa_movimiento": 0.05, "moneda": "€"}
    
    except json.JSONDecodeError:
        print(f"❌ Error: {ARCHIVO_CONFIG} tiene un formato inválido.")
        sys.exit(1)

def guardar_configuracion(nueva_config):
    """Guarda el diccionario de configuración en el archivo JSON."""
    try:
        with open(ARCHIVO_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(nueva_config, f, indent=4, ensure_ascii=False)
        print("✅ Configuración guardada correctamente.")
        return True
    except IOError as e:
        print(f"❌ Error al guardar configuración: {e}")
        return False