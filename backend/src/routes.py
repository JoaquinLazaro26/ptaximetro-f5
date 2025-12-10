from fastapi import APIRouter, HTTPException, Depends
from src.schemas import EstadoCarrera, ConfigCarrera, TicketFinal
from src.core import get_taxi_core, TaximetroCore

router = APIRouter(prefix="/api/v1/taxi", tags=["Operaciones Taxímetro"])

@router.get("/status", response_model=EstadoCarrera)
def obtener_status(taxi: TaximetroCore = Depends(get_taxi_core)):
    """Devuelve el estado en tiempo real para el frontend."""
    info = taxi.obtener_estado_actual()
    return EstadoCarrera(
        estado=info["estado"],
        tiempo_transcurrido=info["tiempo"],
        importe_actual=info["importe"],
        moneda="€" # Esto vendría de config en el futuro
    )

@router.post("/start")
def iniciar_carrera(config: ConfigCarrera, taxi: TaximetroCore = Depends(get_taxi_core)):
    try:
        taxi.iniciar_carrera(config.tarifa_parado, config.tarifa_movimiento)
        return {"msg": "Carrera iniciada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/toggle")
def alternar_marcha(taxi: TaximetroCore = Depends(get_taxi_core)):
    """Cambia de Parado a Movimiento y viceversa."""
    taxi.alternar_marcha()
    return {"msg": "Cambio de estado registrado", "nuevo_estado": taxi.estado.name}

@router.post("/stop", response_model=TicketFinal)
def finalizar_carrera(taxi: TaximetroCore = Depends(get_taxi_core)):
    """Finaliza la carrera y devuelve el ticket."""
    try:
        ticket = taxi.finalizar_carrera()
        # TODO: AQUÍ LLAMAREMOS A FIREBASE EN LA SIGUIENTE SUB-ISSUE
        return ticket
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))