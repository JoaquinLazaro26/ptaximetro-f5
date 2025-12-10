from google.cloud import firestore
from src.config import get_firestore_db
from src.schemas import TicketFinal, ConfiguracionTarifas, DashboardKPIs
import logging

logger = logging.getLogger("DB_Service")

# --- GESTIÓN DE TRAYECTOS ---

def guardar_trayecto(ticket: TicketFinal, user_id: str):
    try:
        db = get_firestore_db()
        datos = ticket.model_dump(exclude={"id"}) # Excluimos ID porque lo genera Firestore
        datos["created_at"] = firestore.SERVER_TIMESTAMP
        datos["user_id"] = user_id # Vinculamos el trayecto al usuario (Admin)
        
        _, ref = db.collection("trayectos").add(datos)
        logger.info(f"💾 Trayecto guardado: {ref.id}")
        return ref.id
    except Exception as e:
        logger.error(f"❌ Error guardando trayecto: {e}")
        return None

def obtener_historial(limit: int = 10) -> list[TicketFinal]:
    """Recupera los últimos N trayectos ordenados por fecha."""
    try:
        db = get_firestore_db()
        # Query ordenada por fecha descendente
        docs = db.collection("trayectos")\
                 .order_by("created_at", direction=firestore.Query.DESCENDING)\
                 .limit(limit)\
                 .stream()
        
        historial = []
        for doc in docs:
            data = doc.to_dict()
            # Convertir timestamp de firestore a datetime de python si es necesario
            if "created_at" in data:
                data["timestamp"] = data["created_at"]
            
            # Inyectar el ID del documento
            data["id"] = doc.id
            historial.append(TicketFinal(**data))
            
        return historial
    except Exception as e:
        logger.error(f"Error recuperando historial: {e}")
        return []

def calcular_kpis() -> DashboardKPIs:
    """Calcula totales agregados (versión simple para Firestore)."""
    try:
        db = get_firestore_db()
        docs = db.collection("trayectos").stream()
        
        total_ganado = 0.0
        total_carreras = 0
        tiempo_total = 0
        
        for doc in docs:
            d = doc.to_dict()
            total_ganado += d.get("total_coste", 0)
            tiempo_total += d.get("total_tiempo", 0)
            total_carreras += 1
            
        promedio = (total_ganado / total_carreras) if total_carreras > 0 else 0.0
        
        return DashboardKPIs(
            total_ganado=round(total_ganado, 2),
            total_carreras=total_carreras,
            tiempo_total_servicio=tiempo_total,
            promedio_carrera=round(promedio, 2)
        )
    except Exception as e:
        logger.error(f"Error calculando KPIs: {e}")
        return DashboardKPIs(total_ganado=0, total_carreras=0, tiempo_total_servicio=0, promedio_carrera=0)

# --- GESTIÓN DE CONFIGURACIÓN ---

def obtener_configuracion() -> ConfiguracionTarifas:
    """Lee la configuración de Firestore o devuelve defaults."""
    try:
        db = get_firestore_db()
        doc = db.collection("settings").document("global").get()
        
        if doc.exists:
            return ConfiguracionTarifas(**doc.to_dict())
        else:
            # Defaults si no existe
            return ConfiguracionTarifas(tarifa_parado=0.05, tarifa_movimiento=0.10, moneda="€")
    except Exception as e:
        logger.error(f"Error leyendo config: {e}")
        # Fail-safe defaults
        return ConfiguracionTarifas(tarifa_parado=0.05, tarifa_movimiento=0.10)

def guardar_configuracion(conf: ConfiguracionTarifas):
    """Actualiza la configuración global."""
    try:
        db = get_firestore_db()
        db.collection("settings").document("global").set(conf.model_dump())
        logger.info("⚙️ Configuración actualizada en Firestore")
        return True
    except Exception as e:
        logger.error(f"Error guardando config: {e}")
        raise e