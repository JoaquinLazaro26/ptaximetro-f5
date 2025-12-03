import time

# Constantes
TARIFA_PARADO = 0.02
TARIFA_MOVIMIENTO = 0.05

# Funcion para calcular el costo según tiempo de inicio y el estado
def calcular_coste_tramo(tiempo_inicio, estado):
    """
    Calcula los datos de un tramo específico.
    Retorna: (coste_tramo, tiempo_transcurrido, tiempo_actual)
    """
    tiempo_actual = time.time()
    segundos_transcurridos = tiempo_actual - tiempo_inicio
    
    precio_actual = TARIFA_MOVIMIENTO if estado == "movimiento" else TARIFA_PARADO
    coste_tramo = segundos_transcurridos * precio_actual
    
    return coste_tramo, segundos_transcurridos, tiempo_actual