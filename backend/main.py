# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.logs import configurar_logging
from src.routes import router as taxi_router
from src.config import get_firestore_db
from src.core import get_taxi_core
from src.services import obtener_configuracion

# 1. Configurar Logging antes de nada
configurar_logging()

app = FastAPI(title="Proyecto-Taximetro API", version="3.1.0")

# CORS
origins = ["*"] # Permitir todo por ahora para facilitar desarrollo frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router
app.include_router(taxi_router)

@app.on_event("startup")
async def startup_event():
    """Inicialización de Singletons y Cachés."""
    try:
        # 1. Verificar conexión DB
        from src.config import get_firestore_db
        get_firestore_db()
        
        # 2. Cargar caché de configuración en el Core
        taxi = get_taxi_core()
        config_db = obtener_configuracion() # Lee de Firestore
        taxi.actualizar_configuracion_interna(config_db.moneda)
        
        print(f"✅ Sistema iniciado. Moneda configurada: {taxi.moneda}")
        
    except Exception as e:
        print(f"❌ Error en inicio: {e}")

@app.get("/")
def read_root():
    return {"status": "online"}