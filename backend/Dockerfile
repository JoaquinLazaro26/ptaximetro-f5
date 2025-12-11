# Usamos Python 3.14-slim
FROM python:3.14-slim

# Evita que Python genere archivos .pyc y bufferea la salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos dependencias del sistema necesarias para compilar librerías
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos requirements primero para aprovechar la caché de Docker
COPY requirements.txt .

# Actualizamos pip e instalamos dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente
COPY . .

# Exponemos el puerto
EXPOSE 8000

# Comando de inicio con Hot-Reload activado para desarrollo
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]