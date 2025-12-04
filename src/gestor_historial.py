import datetime
from typing import Any

class GestorHistorial:
    ARCHIVO_HISTORIAL = 'history.txt'

    def guardar(self, trayecto: Any, moneda: str) -> bool:
        """
        Orquesta el guardado del trayecto en el archivo de registro.
        """
        linea = self._formatear_linea(trayecto, moneda)
        return self._escribir_linea(linea)

    def _formatear_linea(self, trayecto: Any, moneda: str) -> str:
        """
        Construye la cadena de texto con el formato legible.
        Incluye fecha, duración, tarifas aplicadas y coste total.
        """
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extracción de datos (Clean Code: nombres claros)
        duracion = trayecto.total_tiempo
        coste = trayecto.total_coste
        t_parado = trayecto.tarifa_parado
        t_mov = trayecto.tarifa_movimiento

        # Formato: FECHA | DURACION | TARIFAS(P/M) | TOTAL
        return (
            f"{fecha_hora} | "
            f"Tiempo: {duracion:.2f}s | "
            f"Tarifas: {t_parado:.2f}/{t_mov:.2f} ({moneda}/s) | "
            f"Total: {coste:.2f}{moneda}\n"
        )

    def _escribir_linea(self, linea: str) -> bool:
        """Maneja exclusivamente la operación de I/O (Input/Output)."""
        try:
            with open(self.ARCHIVO_HISTORIAL, 'a', encoding='utf-8') as f:
                f.write(linea)
            return True
        except IOError as e:
            # Aquí podríamos integrar un logger si fuera necesario
            print(f"❌ Error crítico escribiendo historial: {e}")
            return False