from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.schemas import EstadoCarrera, ConfiguracionTarifas, TicketFinal, DashboardKPIs
from src.core import get_taxi_core, TaximetroCore, Estado
from src.auth import verificar_token
import src.services as services

# Todas las rutas requieren autenticación (Token de Google)
router = APIRouter(
    prefix="/api/v1/taxi", 
    tags=["Taximetro Expert"],
    dependencies=[Depends(verificar_token)] 
)

# --- OPERATIVAS (CONTROL) ---

@router.get("/status", response_model=EstadoCarrera)
def obtener_status(taxi: TaximetroCore = Depends(get_taxi_core)):
    """Polling: Estado en tiempo real usando caché RAM."""
    info = taxi.obtener_estado_actual()
    
    return EstadoCarrera(
        estado=info["estado"],
        tiempo_transcurrido=info["tiempo"],
        importe_actual=info["importe"],
        moneda=taxi.moneda
    )

@router.post("/start")
def iniciar_carrera(
    taxi: TaximetroCore = Depends(get_taxi_core),
    user: dict = Depends(verificar_token) # Obtenemos info del usuario
):
    """Inicia carrera usando la configuración guardada en BD."""
    # 1. Obtener tarifas de Firestore
    config = services.obtener_configuracion()
    
    try:
        taxi.iniciar_carrera(config.tarifa_parado, config.tarifa_movimiento)
        return {"msg": "Carrera iniciada", "tarifas": config}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/toggle")
def alternar_marcha(taxi: TaximetroCore = Depends(get_taxi_core)):
    """Pausar/Reanudar movimiento. Solo si hay carrera activa."""
    if taxi.estado == Estado.LIBRE:
        raise HTTPException(status_code=400, detail="No hay carrera activa para alternar.")
    
    taxi.alternar_marcha()
    return {"msg": "Estado cambiado", "nuevo_estado": taxi.estado.name}

@router.post("/stop", response_model=TicketFinal)
def finalizar_carrera(
    taxi: TaximetroCore = Depends(get_taxi_core),
    user: dict = Depends(verificar_token)
):
    """Finaliza, cobra y guarda en historial."""
    try:
        ticket = taxi.finalizar_carrera()
        # Guardamos vinculando al UID de Firebase del usuario logueado
        services.guardar_trayecto(ticket, user_id=user["uid"])
        return ticket
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- GESTIÓN (DASHBOARD & CONFIG) ---

@router.get("/config", response_model=ConfiguracionTarifas)
def leer_configuracion():
    """Devuelve las tarifas actuales."""
    return services.obtener_configuracion()

@router.put("/config")
def actualizar_configuracion(
    nuevas_tarifas: ConfiguracionTarifas,
    taxi: TaximetroCore = Depends(get_taxi_core)
):
    if taxi.estado != Estado.LIBRE:
        raise HTTPException(status_code=409, detail="No se puede cambiar config en carrera.")
    # Guardar en Firestore
    services.guardar_configuracion(nuevas_tarifas)
    # Actualizar caché en el Core
    taxi.actualizar_configuracion_interna(nuevas_tarifas.moneda)
    
    return {"msg": "Configuración actualizada", "data": nuevas_tarifas}

@router.get("/history", response_model=List[TicketFinal])
def ver_historial():
    """Devuelve los últimos 10 trayectos."""
    return services.obtener_historial(limit=10)

@router.get("/dashboard", response_model=DashboardKPIs)
def ver_dashboard():
    """Calcula totales y estadísticas."""
    return services.calcular_kpis()