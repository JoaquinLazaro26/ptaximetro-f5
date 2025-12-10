from pydantic import BaseModel
from typing import Optional

# Lo que devolvemos al frontend periódicamente
class EstadoCarrera(BaseModel):
    estado: str          # "LIBRE", "PARADO", "MOVIMIENTO"
    tiempo_transcurrido: int
    importe_actual: float
    moneda: str

# Configuración para iniciar carrera
class ConfigCarrera(BaseModel):
    tarifa_parado: float = 0.05
    tarifa_movimiento: float = 0.10
    moneda: str = "€"

# Recibo final
class TicketFinal(BaseModel):
    total_tiempo: int
    total_coste: float
    tiempo_movimiento: int
    tiempo_parado: int
    coste_movimiento: float
    coste_parado: float
    timestamp: str