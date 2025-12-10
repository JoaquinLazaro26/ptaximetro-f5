from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

# --- CONFIGURACIÓN ---
class ConfiguracionTarifas(BaseModel):
    tarifa_parado: float = Field(..., gt=0, description="Precio por segundo parado")
    tarifa_movimiento: float = Field(..., gt=0, description="Precio por segundo en movimiento")
    moneda: str = "€"

    @field_validator('tarifa_parado', 'tarifa_movimiento')
    def validar_positivos(cls, v):
        if v <= 0:
            raise ValueError('Las tarifas deben ser mayores a 0')
        return v

# --- RESPUESTA DE ESTADO (POLLING) ---
class EstadoCarrera(BaseModel):
    estado: str
    tiempo_transcurrido: int
    importe_actual: float
    moneda: str
    
# --- TICKET FINAL (HISTORIAL) ---
class TicketFinal(BaseModel):
    id: Optional[str] = None
    total_tiempo: int
    total_coste: float
    tiempo_movimiento: int
    tiempo_parado: int
    coste_movimiento: float
    coste_parado: float
    # Nuevos campos solicitados:
    tarifa_parado_aplicada: float
    tarifa_movimiento_aplicada: float
    timestamp: datetime # Usamos datetime real para serialización correcta

# --- DASHBOARD / KPIS ---
class DashboardKPIs(BaseModel):
    total_ganado: float
    total_carreras: int
    tiempo_total_servicio: int # Segundos
    promedio_carrera: float