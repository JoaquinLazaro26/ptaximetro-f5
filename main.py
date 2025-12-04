import time
import sys
import logging
from src.gestor_historial import guardar_trayecto
from src.logica import calcular_coste_tramo
from src.configuracion import cargar_configuracion, guardar_configuracion

# Configuración del Log
logging.basicConfig(
    filename='taximetro.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Carga inicial de config
CONFIG = cargar_configuracion()
T_PARADO = CONFIG['tarifa_parado']
T_MOVIMIENTO = CONFIG['tarifa_movimiento']
MONEDA = str(CONFIG['moneda'])

def mostrar_bienvenida():
    print("\n" + "┌" + "─"*40 + "┐")
    print("│ 🚕  SISTEMA DE TAXÍMETRO DIGITAL v1.1   │")
    print("└" + "─"*40 + "┘")
    print(f" • Tarifa Parado      : {T_PARADO:.2f}{MONEDA}/s")
    print(f" • Tarifa Movimiento  : {T_MOVIMIENTO:.2f}{MONEDA}/s")
    print("-" * 42 + "\n")

def imprimir_estado_intermedio(coste_tramo, tiempo_tramo, estado_anterior, total_acumulado):
    print(f"\n   ⏱️  Fin de tramo ({estado_anterior.upper()})")
    print(f"   ├─ Tiempo tramo: {tiempo_tramo:.2f}s")
    print(f"   ├─ Coste tramo : {coste_tramo:.2f}{MONEDA}")
    print(f"   └─ 💰 ACUMULADO ACTUAL: {total_acumulado:.2f}{MONEDA}")

def imprimir_factura_final(t_parado, t_mov, c_parado, c_mov):
    t_total = t_parado + t_mov
    c_total = c_parado + c_mov
    print("\n" + "="*42)
    print("             📄 FACTURA FINAL             ")
    print("="*42)
    print(f" ⏱️  TIEMPO TOTAL       : {t_total:.2f}s")
    print(f" 💰 COSTE TOTAL        : {c_total:.2f}{MONEDA}")
    print("="*42 + "\n")
    print(" DESGLOSE:")
    print(f" • En Movimiento : {t_mov:.2f}s  -> {c_mov:.2f}{MONEDA}")
    print(f" • Parado        : {t_parado:.2f}s  -> {c_parado:.2f}{MONEDA}")
    print("="*42 + "\n")

def iniciar_trayecto():
    # Log de inicio
    logging.info(f"TRAYECTO INICIADO. Tarifas vigentes: P={T_PARADO}, M={T_MOVIMIENTO}")
    
    t_parado_total = 0.0
    t_mov_total = 0.0
    c_parado_total = 0.0
    c_mov_total = 0.0
    
    en_trayecto = True
    estado_actual = "parado"
    tiempo_ultimo_cambio = time.time()
    
    print(f"\n🏁 TRAYECTO INICIADO.")
    print(f" • Tarifa Parado      : {T_PARADO:.2f}{MONEDA}/s")
    print(f" • Tarifa Movimiento  : {T_MOVIMIENTO:.2f}{MONEDA}/s")

    while en_trayecto:
        print(f"\n📢 Estado actual: {estado_actual.upper()}")
        
        if estado_actual == "parado":
            print("👉 Opciones disponibles: [m]over, [f]inalizar")
        else:
            print("👉 Opciones disponibles: [p]arar, [f]inalizar")
            
        comando = input(" > ").strip().lower()

        if comando == 'm':
            if estado_actual == "movimiento":
                msg = "Intento de mover cuando ya estaba en movimiento"
                print(f"❌ {msg}")
                logging.warning(msg)
            else:
                coste, tiempo, ahora = calcular_coste_tramo(tiempo_ultimo_cambio, estado_actual, T_PARADO, T_MOVIMIENTO)
                c_parado_total += coste
                t_parado_total += tiempo
                total_actual = c_parado_total + c_mov_total
                
                # Log del cambio
                logging.info(f"Cambio estado: MOVIMIENTO. Tramo Parado: {tiempo:.2f}s, Coste: {coste:.2f}{MONEDA}")
                
                imprimir_estado_intermedio(coste, tiempo, estado_actual, total_actual)
                tiempo_ultimo_cambio = ahora
                estado_actual = "movimiento"
                print(f"🚗 ¡EN MARCHA!")

        elif comando == 'p':
            if estado_actual == "parado":
                 msg = "Intento de parar cuando ya estaba parado"
                 print(f"❌ {msg}")
                 logging.warning(msg)
            else:
                coste, tiempo, ahora = calcular_coste_tramo(tiempo_ultimo_cambio, estado_actual, T_PARADO, T_MOVIMIENTO)
                c_mov_total += coste
                t_mov_total += tiempo
                total_actual = c_parado_total + c_mov_total

                # Log del cambio
                logging.info(f"Cambio estado: PARADO. Tramo Movimiento: {tiempo:.2f}s, Coste: {coste:.2f}{MONEDA}")

                imprimir_estado_intermedio(coste, tiempo, estado_actual, total_actual)
                tiempo_ultimo_cambio = ahora
                estado_actual = "parado"
                print(f"🛑 ¡TAXI DETENIDO!")

        elif comando == 'f':
            coste, tiempo, ahora = calcular_coste_tramo(tiempo_ultimo_cambio, estado_actual, T_PARADO, T_MOVIMIENTO)
            
            if estado_actual == "movimiento":
                c_mov_total += coste
                t_mov_total += tiempo
            else:
                c_parado_total += coste
                t_parado_total += tiempo
            
            total_final = c_parado_total + c_mov_total
            tiempo_total = t_parado_total + t_mov_total

            if guardar_trayecto(tiempo_total, total_final, MONEDA):
                logging.info("Historial guardado correctamente en history.txt")
            else:
                logging.error("No se pudo guardar el historial")
            # Log de Fin exitoso
            logging.info(f"TRAYECTO FINALIZADO. Total: {total_final:.2f}{MONEDA}. Duración: {(t_parado_total + t_mov_total):.2f}s")
            
            en_trayecto = False
            imprimir_factura_final(t_parado_total, t_mov_total, c_parado_total, c_mov_total)
        
        else:
            print("❌ Comando no reconocido.")
            logging.warning(f"Comando desconocido introducido: {comando}")

def menu_configuracion():
    """Sub-menú para cambiar precios."""
    global T_PARADO, T_MOVIMIENTO
    
    print("\n⚙️  CONFIGURACIÓN DE PRECIOS")
    print(f"   Actual Parado: {T_PARADO}")
    print(f"   Actual Movimiento: {T_MOVIMIENTO}")
    
    try:
        nuevo_p = float(input("Nuevo precio Parado (€/s): "))
        nuevo_m = float(input("Nuevo precio Movimiento (€/s): "))
        
        # Validaciones básicas
        if nuevo_p < 0 or nuevo_m < 0:
            print("❌ Los precios no pueden ser negativos.")
            return

        nueva_conf = {
            "tarifa_parado": nuevo_p,
            "tarifa_movimiento": nuevo_m,
            "moneda": MONEDA
        }
        
        if guardar_configuracion(nueva_conf):
            # Actualizamos las variables globales con los nuevos valores
            T_PARADO = nuevo_p
            T_MOVIMIENTO = nuevo_m
            logging.info(f"Configuración actualizada: P={nuevo_p}, M={nuevo_m}")

    except ValueError:
        print("❌ Error: Debes introducir números válidos.")

def main():
    logging.info("App iniciada")
    mostrar_bienvenida()
    
    while True:
        print("\n🔵 MENÚ PRINCIPAL")
        print("1. 🚕 Iniciar nuevo trayecto")
        print("2. ⚙️  Configurar tarifas")
        print("3. 👋 Salir")
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == '1':
            iniciar_trayecto()
        elif opcion == '2':
            menu_configuracion()
        elif opcion == '3':
            print("👋 ¡Hasta pronto!")
            logging.info("Salida del usuario")
            sys.exit()
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()