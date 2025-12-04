import datetime
import os

ARCHIVO_HISTORIAL = 'history.txt'

def guardar_trayecto(duracion_total, costo_total, moneda):
    """
    Guarda una línea en el historial con fecha, duración y costo.
    Ejemplo: 2023-10-27 10:30:00 | Duración: 120.0s | Total: 5.50€
    """
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{fecha_hora} | Duración: {duracion_total:.2f}s | Total: {costo_total:.2f}{moneda}\n"
    
    try:
        with open(ARCHIVO_HISTORIAL, 'a', encoding='utf-8') as f:
            f.write(linea)
        return True
    except IOError as e:
        print(f"⚠️ Error al escribir en historial: {e}")
        return False