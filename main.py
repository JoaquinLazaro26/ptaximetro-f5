import time
import sys
import logging
from src.logica import calcular_coste_tramo
from src.configuracion import cargar_configuracion

# Carga inicial de datos
CONFIG = cargar_configuracion()
T_PARADO = CONFIG['tarifa_parado']
T_MOVIMIENTO = CONFIG['tarifa_movimiento']
MONEDA = CONFIG['moneda']

## Configuración de los LOGS 
logging.basicConfig(
    filename='taximetro.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def mostrar_bienvenida():
    print("\n" + "┌" + "─"*40 + "┐")
    print("│ 🚕  SISTEMA DE TAXÍMETRO DIGITAL v1.0   │")
    print("└" + "─"*40 + "┘")
    print("Instrucciones:")
    print(f" • Tarifa Parado      : {T_PARADO:.2f}€/s")
    print(f" • Tarifa Movimiento  : {T_MOVIMIENTO:.2f}€/s")
    print("-" * 42 + "\n")

def imprimir_estado_intermedio(coste_tramo, tiempo_tramo, estado_anterior, total_acumulado):
    """Imprime el resumen al cambiar de estado."""
    print(f"\n   ⏱️  Fin de tramo ({estado_anterior.upper()})")
    print(f"   ├─ Tiempo tramo: {tiempo_tramo:.2f}s")
    print(f"   ├─ Coste tramo : {coste_tramo:.2f}€")
    print(f"   └─ 💰 ACUMULADO ACTUAL: {total_acumulado:.2f}€")

def imprimir_factura_final(t_parado, t_mov, c_parado, c_mov):
    """Imprime la factura bonita al finalizar."""
    t_total = t_parado + t_mov
    c_total = c_parado + c_mov
    
    print("\n" + "="*42)
    print("             📄 FACTURA FINAL             ")
    print("="*42)
    print(f" ⏱️  TIEMPO TOTAL       : {t_total:.2f}s")
    print(f" 💰 COSTE TOTAL        : {c_total:.2f}€")
    print("-" * 42)
    print(" DESGLOSE:")
    print(f" • En Movimiento : {t_mov:.2f}s  -> {c_mov:.2f}€")
    print(f" • Parado        : {t_parado:.2f}s  -> {c_parado:.2f}€")
    print("="*42 + "\n")

def iniciar_trayecto():
    logging.info("Iniciando nuevo trayecto")
    # Acumuladores
    t_parado_total = 0.0
    t_mov_total = 0.0
    c_parado_total = 0.0
    c_mov_total = 0.0
    
    en_trayecto = True
    estado_actual = "parado" # Estado inicial
    tiempo_ultimo_cambio = time.time()
    
    print(f"🏁 TRAYECTO INICIADO.")

    while en_trayecto:
        # Lógica de Menú Dinámico
        print(f"\n📢 Estado actual: {estado_actual.upper()}")
        
        if estado_actual == "parado":
            print("👉 Opciones disponibles: [m]over, [f]inalizar")
        else:
            print("👉 Opciones disponibles: [p]arar, [f]inalizar")
            
        comando = input(" > ").strip().lower()

        # Lógica de transición de estados
        if comando == 'm':
            if estado_actual == "movimiento":
                print("❌ Opción inválida. El taxi ya se mueve.")
            else:
                # Calcular tramo PARADO
                coste, tiempo, ahora = calcular_coste_tramo(tiempo_ultimo_cambio, estado_actual, T_PARADO, T_MOVIMIENTO)
                
                # Actualizar acumuladores
                c_parado_total += coste
                t_parado_total += tiempo
                total_actual = c_parado_total + c_mov_total
                
                imprimir_estado_intermedio(coste, tiempo, estado_actual, total_actual)
                
                # Cambio
                tiempo_ultimo_cambio = ahora
                estado_actual = "movimiento"
                print(f"🚗 ¡EN MARCHA!")

        elif comando == 'p':
            if estado_actual == "parado":
                 print("❌ Opción inválida. El taxi ya está parado.")
            else:
                # Calcular tramo MOVIMIENTO
                coste, tiempo, ahora = calcular_coste_tramo(tiempo_ultimo_cambio, estado_actual, T_PARADO, T_MOVIMIENTO)
                
                # Actualizar acumuladores
                c_mov_total += coste
                t_mov_total += tiempo
                total_actual = c_parado_total + c_mov_total

                imprimir_estado_intermedio(coste, tiempo, estado_actual, total_actual)
                
                # Cambio
                tiempo_ultimo_cambio = ahora
                estado_actual = "parado"
                print(f"🛑 ¡TAXI DETENIDO!")

        elif comando == 'f':
            # Calcular último tramo pendiente
            coste, tiempo, ahora = calcular_coste_tramo(tiempo_ultimo_cambio, estado_actual, T_PARADO, T_MOVIMIENTO)
            
            if estado_actual == "movimiento":
                c_mov_total += coste
                t_mov_total += tiempo
            else:
                c_parado_total += coste
                t_parado_total += tiempo
            
            en_trayecto = False
            imprimir_factura_final(t_parado_total, t_mov_total, c_parado_total, c_mov_total)
        
        else:
            print("❌ Comando no reconocido.")

def main():
    mostrar_bienvenida()
    
    while True:
        respuesta = input("¿Iniciar nuevo trayecto? (s/n): ").strip().lower()
        
        if respuesta == 's':
            iniciar_trayecto()
        elif respuesta == 'n':
            print("👋 ¡Gracias por usar el servicio!")
            sys.exit()
        else:
            print("Por favor, usa 's' o 'n'.")

if __name__ == "__main__":
    main()