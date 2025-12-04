import pytest
from src.logica import calcular_coste_tramo

# Constantes para los tests
PRECIO_PARADO = 0.02
PRECIO_MOVIMIENTO = 0.05

# --- TESTS BÁSICOS (HAPPY PATH) ---

def test_calculo_parado_exacto():
    """Verifica que 10 segundos parado cobren exactamente 0.20€."""
    inicio = 1000
    fin = 1010
    coste, tiempo, _ = calcular_coste_tramo(inicio, "parado", PRECIO_PARADO, PRECIO_MOVIMIENTO, tiempo_fin=fin)
    
    assert tiempo == 10
    assert coste == 0.20

def test_calculo_movimiento_exacto():
    """Verifica que 5 segundos en movimiento cobren exactamente 0.25€."""
    inicio = 1000
    fin = 1005
    coste, tiempo, _ = calcular_coste_tramo(inicio, "movimiento", PRECIO_PARADO, PRECIO_MOVIMIENTO, tiempo_fin=fin)
    
    assert tiempo == 5
    assert coste == 0.25

def test_tiempo_cero():
    """No debe cobrar nada si el tiempo transcurrido es 0."""
    inicio = 1000
    coste, tiempo, _ = calcular_coste_tramo(inicio, "parado", PRECIO_PARADO, PRECIO_MOVIMIENTO, tiempo_fin=inicio)
    
    assert tiempo == 0
    assert coste == 0

# --- TESTS DE BORDES Y ROBUSTEZ (EDGE CASES) ---

def test_precision_decimal():
    """
    Verifica problemas de punto flotante.
    Si estamos 0.1s a 0.05€/s -> El coste debería ser 0.005€.
    Usamos pytest.approx para evitar errores por decimales ínfimos (ej: 0.00500000001).
    """
    inicio = 1000
    fin = 1000.1 # Solo una décima de segundo
    
    coste, tiempo, _ = calcular_coste_tramo(inicio, "movimiento", PRECIO_PARADO, PRECIO_MOVIMIENTO, tiempo_fin=fin)
    
    # 0.1 * 0.05 = 0.005
    assert coste == pytest.approx(0.005)

def test_estado_desconocido_usa_tarifa_parado():
    """
    Según nuestra lógica actual: 'precio = mov if estado == "movimiento" else parado'.
    Si pasamos un estado basura ("volando"), debería cobrar como parado (default).
    Esto es importante saberlo para evitar crashes.
    """
    inicio = 1000
    fin = 1010
    
    coste, _, _ = calcular_coste_tramo(inicio, "volando", PRECIO_PARADO, PRECIO_MOVIMIENTO, tiempo_fin=fin)
    
    # Debería usar la tarifa de parado (0.02 * 10 = 0.20)
    assert coste == 0.20

def test_tarifas_gratis():
    """El sistema debe soportar tarifas a 0 euros (promociones, etc)."""
    inicio = 1000
    fin = 1100 # 100 segundos
    
    coste, _, _ = calcular_coste_tramo(inicio, "movimiento", 0.00, 0.00, tiempo_fin=fin)
    
    assert coste == 0.0

def test_tarifas_cambiantes():
    """
    Asegura que la función obedece los argumentos y no usa constantes globales.
    Si le paso tarifa 100€/s, debe cobrar eso.
    """
    inicio = 1000
    fin = 1001 # 1 segundo
    tarifa_cara = 100.0
    
    coste, _, _ = calcular_coste_tramo(inicio, "movimiento", PRECIO_PARADO, tarifa_cara, tiempo_fin=fin)
    
    assert coste == 100.0

def test_tiempo_negativo():
    """
    ¿Qué pasa si el tiempo fin es menor al inicio?
    Matemáticamente debería dar coste negativo. 
    Es bueno testearlo para confirmar que la lógica matemática es consistente.
    """
    inicio = 1010
    fin = 1000 # El reloj fue hacia atrás 10 segundos
    
    coste, tiempo, _ = calcular_coste_tramo(inicio, "parado", PRECIO_PARADO, PRECIO_MOVIMIENTO, tiempo_fin=fin)
    
    assert tiempo == -10
    assert coste == -0.20