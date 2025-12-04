import time
from enum import Enum

class Estado(Enum):
    PARADO = "parado"
    MOVIMIENTO = "movimiento"
    FINALIZADO = "finalizado"

class Trayecto:
    """Representa un viaje individual y calcula sus costos."""
    
    def __init__(self, tarifa_parado, tarifa_movimiento):
        self.tarifa_parado = tarifa_parado
        self.tarifa_movimiento = tarifa_movimiento
        
        self.inicio = time.time()
        self.ultimo_cambio = self.inicio
        self.estado_actual = Estado.PARADO
        
        # Acumuladores
        self.tiempo_parado = 0.0
        self.tiempo_movimiento = 0.0
        self.coste_parado = 0.0
        self.coste_movimiento = 0.0

    def cambiar_estado(self, nuevo_estado: Estado) -> tuple[float, float]:
        """Calcula el tramo actual y cambia al nuevo estado."""
        if nuevo_estado == self.estado_actual:
            raise ValueError(f"Ya estás en estado {nuevo_estado.value}")
            
        # Calcular lo que ha pasado desde el último cambio hasta AHORA
        ahora = time.time()
        tiempo_tramo = ahora - self.ultimo_cambio
        coste_tramo = 0.0

        if self.estado_actual == Estado.PARADO:
            coste_tramo = tiempo_tramo * self.tarifa_parado
            self.tiempo_parado += tiempo_tramo
            self.coste_parado += coste_tramo
        elif self.estado_actual == Estado.MOVIMIENTO:
            coste_tramo = tiempo_tramo * self.tarifa_movimiento
            self.tiempo_movimiento += tiempo_tramo
            self.coste_movimiento += coste_tramo

        # Actualizar timestamps y estado
        self.ultimo_cambio = ahora
        self.estado_actual = nuevo_estado
        
        return coste_tramo, tiempo_tramo

    def finalizar(self):
        """Cierra el trayecto calculando el último tramo pendiente."""
        coste_final, tiempo_final = self.cambiar_estado(Estado.FINALIZADO)
        return coste_final, tiempo_final

    @property
    def total_tiempo(self):
        return self.tiempo_parado + self.tiempo_movimiento

    @property
    def total_coste(self):
        return self.coste_parado + self.coste_movimiento


class Taximetro:
    """Controlador principal de la aplicación (Fachada)."""
    
    def __init__(self, gestor_config, gestor_historial):
        """
        Args:
            gestor_config: Instancia de GestorConfiguracion.
            gestor_historial: Instancia de GestorHistorial.
        """
        self.config = gestor_config
        self.historial = gestor_historial  # Inyección de dependencia
        self.trayecto_actual = None

    def iniciar_carrera(self):
        t_parado = self.config.get_tarifa("parado")
        t_mov = self.config.get_tarifa("movimiento")
        self.trayecto_actual = Trayecto(t_parado, t_mov)
        return self.trayecto_actual

    def cambiar_estado(self, nuevo_estado_str):
        if not self.trayecto_actual:
            raise RuntimeError("No hay carrera en curso")
            
        estado_enum = Estado(nuevo_estado_str)
        return self.trayecto_actual.cambiar_estado(estado_enum)

    def finalizar_carrera(self):
        if not self.trayecto_actual:
            return None
        
        # 1. Finalizar lógica de tiempo/coste
        self.trayecto_actual.finalizar()
        
        # 2. Guardar usando el gestor inyectado, pasando el OBJETO completo
        self.historial.guardar(
            self.trayecto_actual, 
            self.config.moneda
        )
        
        resumen = self.trayecto_actual
        self.trayecto_actual = None
        return resumen