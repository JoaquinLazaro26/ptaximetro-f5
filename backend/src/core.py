import time
import logging
from enum import Enum
from typing import Optional, Tuple
from src.schemas import TicketFinal

logger = logging.getLogger("CoreNegocio")

class Estado(Enum):
    LIBRE = "libre"
    PARADO = "parado"
    MOVIMIENTO = "movimiento"

class TaximetroCore:
    def __init__(self):
        self.estado = Estado.LIBRE
        self.inicio_trayecto = 0.0
        self.ultimo_cambio = 0.0
        
        # Acumuladores
        self.tiempo_parado = 0.0
        self.tiempo_movimiento = 0.0
        self.coste_parado = 0.0
        self.coste_movimiento = 0.0
        
        # Tarifas actuales
        self.tarifa_parado = 0.0
        self.tarifa_movimiento = 0.0

    def iniciar_carrera(self, t_parado: float, t_mov: float):
        if self.estado != Estado.LIBRE:
            raise ValueError("Carrera ya en curso")
            
        self.tarifa_parado = t_parado
        self.tarifa_movimiento = t_mov
        
        self.inicio_trayecto = time.time()
        self.ultimo_cambio = self.inicio_trayecto
        
        # Empezamos parados por defecto
        self.estado = Estado.PARADO
        
        # Reseteo contadores
        self.tiempo_parado = 0.0
        self.tiempo_movimiento = 0.0
        self.coste_parado = 0.0
        self.coste_movimiento = 0.0
        
        logger.info(f"▶ Carrera INICIADA. Tarifas: P={t_parado}, M={t_mov}")

    def _calcular_tramo_pendiente(self) -> Tuple[float, float, float]:
        """Calcula tiempo y coste desde el último cambio de estado hasta AHORA."""
        if self.estado == Estado.LIBRE:
            return 0.0, 0.0, time.time()

        ahora = time.time()
        delta_tiempo = ahora - self.ultimo_cambio
        delta_coste = 0.0

        if self.estado == Estado.PARADO:
            delta_coste = delta_tiempo * self.tarifa_parado
        elif self.estado == Estado.MOVIMIENTO:
            delta_coste = delta_tiempo * self.tarifa_movimiento
            
        return delta_coste, delta_tiempo, ahora

    def alternar_marcha(self):
        if self.estado == Estado.LIBRE:
            return # No hace nada si no hay carrera

        coste, tiempo, ahora = self._calcular_tramo_pendiente()

        # Consolidar lo acumulado antes de cambiar
        if self.estado == Estado.PARADO:
            self.tiempo_parado += tiempo
            self.coste_parado += coste
            self.estado = Estado.MOVIMIENTO
            logger.info("🚕 Coche en MOVIMIENTO")
        else:
            self.tiempo_movimiento += tiempo
            self.coste_movimiento += coste
            self.estado = Estado.PARADO
            logger.info("🛑 Coche PARADO")

        self.ultimo_cambio = ahora

    def finalizar_carrera(self) -> TicketFinal:
        if self.estado == Estado.LIBRE:
            raise ValueError("No hay carrera activa")

        # Sumar el último tramo
        coste, tiempo, _ = self._calcular_tramo_pendiente()
        
        if self.estado == Estado.PARADO:
            self.tiempo_parado += tiempo
            self.coste_parado += coste
        elif self.estado == Estado.MOVIMIENTO:
            self.tiempo_movimiento += tiempo
            self.coste_movimiento += coste

        ticket = TicketFinal(
            total_tiempo=int(self.tiempo_parado + self.tiempo_movimiento),
            total_coste=round(self.coste_parado + self.coste_movimiento, 2),
            tiempo_movimiento=int(self.tiempo_movimiento),
            tiempo_parado=int(self.tiempo_parado),
            coste_movimiento=round(self.coste_movimiento, 2),
            coste_parado=round(self.coste_parado, 2),
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )

        self.estado = Estado.LIBRE
        logger.info(f"🏁 Carrera FINALIZADA. Total: {ticket.total_coste}")
        return ticket

    def obtener_estado_actual(self) -> dict:
        coste_p, tiempo_p, _ = self._calcular_tramo_pendiente()
        
        t_total = self.tiempo_parado + self.tiempo_movimiento + tiempo_p
        c_total = self.coste_parado + self.coste_movimiento + coste_p
        
        return {
            "estado": self.estado.name,
            "tiempo": int(t_total),
            "importe": round(c_total, 2)
        }

# Instancia Global (Singleton)
taxi_instance = TaximetroCore()

def get_taxi_core():
    return taxi_instance