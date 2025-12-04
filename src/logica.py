import time

# Calcular el coste del tramo según parámetros
# Se le agrega un parámetro opcional para los test unitarios
def calcular_coste_tramo(tiempo_inicio, estado, tarifa_parado, tarifa_movimiento, tiempo_fin=None):
    """
    Calcula el coste. 
    Parámetro 'tiempo_fin' es opcional. Si se pasa, se usa para el cálculo (útil para tests).
    Si no se pasa, usa time.time() (comportamiento normal).
    """
    # Si tiempo_fin tiene valor, úsalo. Si es None, usa time.time()
    tiempo_actual = tiempo_fin if tiempo_fin is not None else time.time()
    
    segundos_transcurridos = tiempo_actual - tiempo_inicio
    
    precio_actual = tarifa_movimiento if estado == "movimiento" else tarifa_parado
    coste_tramo = segundos_transcurridos * precio_actual
    
    return coste_tramo, segundos_transcurridos, tiempo_actual