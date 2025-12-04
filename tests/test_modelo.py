import pytest
import time
from unittest.mock import MagicMock, patch
from src.modelo import Taximetro, Trayecto, Estado
from src.configuracion import GestorConfiguracion
from src.gestor_historial import GestorHistorial

# --- FIXTURES ---

@pytest.fixture
def mock_config():
    """Mock del Gestor de Configuración."""
    config = MagicMock(spec=GestorConfiguracion)
    config.get_tarifa.side_effect = lambda tipo: 2.0 if tipo == "parado" else 5.0
    config.moneda = "€"
    return config

@pytest.fixture
def mock_historial():
    """Mock del Gestor de Historial."""
    historial = MagicMock(spec=GestorHistorial)
    historial.guardar.return_value = True
    return historial

@pytest.fixture
def taximetro(mock_config, mock_historial):
    """
    Instancia un taxímetro inyectándole los Mocks.
    Ahora cumplimos con la nueva firma __init__(config, historial).
    """
    return Taximetro(mock_config, mock_historial)

# --- TESTS TRAYECTO (Lógica pura, sin cambios) ---

def test_calculo_trayecto_parado():
    trayecto = Trayecto(tarifa_parado=2.0, tarifa_movimiento=5.0)
    
    # Setup determinista
    trayecto.inicio = 1000
    trayecto.ultimo_cambio = 1000
    
    # Avanzamos 10s
    with patch('time.time', return_value=1010):
        coste, tiempo = trayecto.cambiar_estado(Estado.MOVIMIENTO)
    
    assert tiempo == 10
    assert coste == 20.0
    assert trayecto.estado_actual == Estado.MOVIMIENTO

def test_calculo_trayecto_movimiento():
    trayecto = Trayecto(2.0, 5.0)
    trayecto.estado_actual = Estado.MOVIMIENTO
    trayecto.ultimo_cambio = 1000
    
    with patch('time.time', return_value=1005):
        coste, tiempo = trayecto.cambiar_estado(Estado.PARADO)
        
    assert tiempo == 5
    assert coste == 25.0

# --- TESTS TAXIMETRO (Integración con Mocks) ---

def test_flujo_completo_taximetro(taximetro, mock_historial):
    """Prueba que el Taxímetro orqueste todo y LLAME al historial al final."""
    
    # 1. Iniciar
    trayecto = taximetro.iniciar_carrera()
    trayecto.ultimo_cambio = 1000 # T=0
    
    # 2. Moverse (10s Parado)
    with patch('time.time', return_value=1010):
        taximetro.cambiar_estado("movimiento")
    
    # 3. Finalizar (10s Movimiento)
    with patch('time.time', return_value=1020):
        resumen = taximetro.finalizar_carrera()
    
    # Validaciones de negocio
    assert resumen.total_coste == 70.0 # (10*2) + (10*5)
    
    # VALIDACIÓN CLAVE DE INTERACCIÓN:
    # Verificamos que el método .guardar() del mock fue llamado exactamente una vez
    mock_historial.guardar.assert_called_once()
    
    # Verificamos que se llamó con los argumentos correctos
    args, _ = mock_historial.guardar.call_args
    assert args[0] == resumen  # El primer argumento fue el objeto trayecto
    assert args[1] == "€"      # El segundo fue la moneda

def test_error_cambio_sin_carrera(taximetro):
    with pytest.raises(RuntimeError):
        taximetro.cambiar_estado("movimiento")