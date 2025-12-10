# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.logs import configurar_logging
from src.routes import router as taxi_router
from src.config import get_firestore_db

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
    # Solo verificamos que DB inicie, aunque no la usemos en esta sub-issue
    try:
        get_firestore_db()
    except:
        pass # El log ya se maneja dentro de config.py

@app.get("/")
def read_root():
    return {"status": "online"}