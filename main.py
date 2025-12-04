import sys
import logging
from src.gestor_historial import GestorHistorial
from src.configuracion import GestorConfiguracion
from src.modelo import Taximetro, Estado, Trayecto
from src.utils import leer_float_seguro

# --- CONFIGURACIÓN GLOBAL ---
logging.basicConfig(
    filename='taximetro.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Inyección de dependencias simple
gestor_conf = GestorConfiguracion()
gestor_hist = GestorHistorial() 
taxi = Taximetro(gestor_conf, gestor_hist)

def mostrar_encabezado() -> None:
    """Imprime la cabecera visual de la aplicación."""
    moneda = gestor_conf.moneda
    t_parado = gestor_conf.get_tarifa('parado')
    t_mov = gestor_conf.get_tarifa('movimiento')

    print("\n" + "┌" + "─"*42 + "┐")
    print("│ 🚕  SISTEMA DE TAXÍMETRO DIGITAL v2.1    │")
    print("└" + "─"*42 + "┘")
    print(f" • Tarifa Parado      : {t_parado:.2f}{moneda}/s")
    print(f" • Tarifa Movimiento  : {t_mov:.2f}{moneda}/s")
    print("-" * 44 + "\n")

def imprimir_resumen_final(resumen: Trayecto) -> None:
    """Muestra la factura final formateada."""
    moneda = gestor_conf.moneda
    print("\n" + "="*44)
    print("             📄 FACTURA FINAL             ")
    print("="*44)
    print(f" ⏱️  TIEMPO TOTAL       : {resumen.total_tiempo:.2f}s")
    print(f" 💰 COSTE TOTAL        : {resumen.total_coste:.2f}{moneda}")
    print("="*44)
    print(" DESGLOSE:")
    print(f"   - En Movimiento : {resumen.tiempo_movimiento:.2f}s ({resumen.coste_movimiento:.2f}{moneda})")
    print(f"   - Parado        : {resumen.tiempo_parado:.2f}s ({resumen.coste_parado:.2f}{moneda})")
    print("="*44 + "\n")

def gestionar_carrera() -> None:
    """Controla el flujo de un trayecto individual."""
    trayecto = taxi.iniciar_carrera()
    moneda = gestor_conf.moneda
    
    logging.info("Nuevo trayecto iniciado por el usuario")
    print(f"\n🏁 TRAYECTO INICIADO.")

    while trayecto.estado_actual != Estado.FINALIZADO:
        estado_str = trayecto.estado_actual.value
        print(f"\n📢 Estado actual: {estado_str.upper()}")
        
        opciones = "[p]arar, [f]inalizar" if trayecto.estado_actual == Estado.MOVIMIENTO else "[m]over, [f]inalizar"
        print(f"👉 Opciones: {opciones}")
            
        comando = input(" > ").strip().lower()

        try:
            coste_tramo, tiempo_tramo = 0.0, 0.0
            
            if comando == 'm':
                coste_tramo, tiempo_tramo = taxi.cambiar_estado("movimiento")
                print(f"🚗 ¡EN MARCHA!")
                logging.info("Usuario cambió estado a: MOVIMIENTO")
            
            elif comando == 'p':
                coste_tramo, tiempo_tramo = taxi.cambiar_estado("parado")
                print(f"🛑 ¡TAXI DETENIDO!")
                logging.info("Usuario cambió estado a: PARADO")
            
            elif comando == 'f':
                logging.info("Usuario solicitó finalizar trayecto")
                resumen = taxi.finalizar_carrera()
                imprimir_resumen_final(resumen) # type: ignore
                logging.info(f"Trayecto finalizado y facturado. Total: {resumen.total_coste:.2f}") # type: ignore
                return 
            
            else:
                print("❌ Comando no reconocido.")
                logging.warning(f"Comando desconocido en carrera: '{comando}'")
                continue

            # Log del tramo intermedio calculado
            if comando in ['m', 'p']:
                logging.info(f"Tramo calculado: {tiempo_tramo:.2f}s, Coste: {coste_tramo:.4f}")

        except ValueError as e:
            print(f"⚠️  Atención: {e}")
            logging.warning(f"Error lógico en carrera: {e}")

def menu_configuracion() -> None:
    """Sub-menú para actualizar tarifas con validación, confirmación y logs completos."""
    logging.info("Acceso al Menú de Configuración")
    
    moneda = gestor_conf.moneda
    p_actual = gestor_conf.get_tarifa("parado")
    m_actual = gestor_conf.get_tarifa("movimiento")

    print("\n⚙️  CONFIGURACIÓN DE PRECIOS")
    print(f"ℹ️  Escribe 'c' en cualquier momento para cancelar.")
    print("-" * 40)

    # 1. Inputs
    nuevo_p = leer_float_seguro(f" > Nuevo precio Parado (Actual: {p_actual}{moneda}/s): ")
    if nuevo_p is None:
        print("🔙 Operación cancelada.")
        logging.info("Configuración abortada por usuario en tarifa parado.")
        return

    nuevo_m = leer_float_seguro(f" > Nuevo precio Movimiento (Actual: {m_actual}{moneda}/s): ")
    if nuevo_m is None:
        print("🔙 Operación cancelada.")
        logging.info("Configuración abortada por usuario en tarifa movimiento.")
        return

    # 2. Resumen
    print("\n" + "🔍 RESUMEN DE CAMBIOS PROPUESTOS:")
    print(f"   Tarifa Parado     : {p_actual:.2f}  --->  {nuevo_p:.2f} {moneda}/s")
    print(f"   Tarifa Movimiento : {m_actual:.2f}  --->  {nuevo_m:.2f} {moneda}/s")
    
    # 3. Confirmación
    confirmacion = input("\n💾 ¿Confirmar y guardar estos cambios? (s/n): ").strip().lower()
    
    if confirmacion == 's':
        gestor_conf.set_tarifa("parado", nuevo_p)
        gestor_conf.set_tarifa("movimiento", nuevo_m)
        print("✅ ¡Configuración guardada correctamente!")
        logging.info(f"Configuración EXITOSA: P({p_actual}->{nuevo_p}), M({m_actual}->{nuevo_m})")
    else:
        print("🚫 Cambios descartados por el usuario.")
        logging.info(f"Configuración DESCARTADA por usuario en confirmación final.")

def main():
    logging.info("=== APLICACIÓN INICIADA (Sesión de Usuario) ===")
    mostrar_encabezado()
    
    while True:
        print("\n🔵 MENÚ PRINCIPAL")
        print("1. 🚕 Iniciar nuevo trayecto")
        print("2. ⚙️  Configurar tarifas")
        print("3. 👋 Salir")
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == '1':
            gestionar_carrera()
        elif opcion == '2':
            menu_configuracion()
        elif opcion == '3':
            print("👋 ¡Hasta pronto!")
            logging.info("Usuario cerró la aplicación voluntariamente (Opción 3)")
            sys.exit()
        else:
            print("❌ Opción no válida, intenta de nuevo.")
            logging.warning(f"Opción inválida en menú principal: '{opcion}'")

if __name__ == "__main__":
    main()