# 🚖 Taxímetro Expert v4.0

> Plataforma de gestión inteligente de tarifas de taxi basada en **Microservicios**, **Docker** y **Firebase**.

![Status](https://img.shields.io/badge/Status-Stable-success)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)
![Frontend](https://img.shields.io/badge/Frontend-Bootstrap%205-purple)

## 📖 ¿De qué trata el proyecto?

**Taxímetro Expert** es una solución digital completa que simula y gestiona el funcionamiento de un taxímetro real, pero con capacidades en la nube. Permite a los conductores calcular el coste de un trayecto basándose en tarifas por tiempo (parado vs movimiento), registrando cada viaje en una base de datos segura.

### 🌟 Funcionalidades Principales
*   **Cálculo en Tiempo Real:** Algoritmo preciso que diferencia tarifas cuando el coche está en marcha o detenido.
*   **Arquitectura Dockerizada:** Backend y Frontend corren en contenedores aislados.
*   **Login Seguro:** Autenticación mediante **Google & Firebase Auth**.
*   **Persistencia en la Nube:** Historial de viajes y configuración de tarifas guardados en **Google Firestore**.
*   **Dashboard Interactivo:** Visualización de ganancias, KPIs y tickets detallados.
*   **Hot-Reload:** Entorno de desarrollo preparado para reflejar cambios de código al instante.

---

## 🚀 Instalación y Despliegue (Docker)

Sigue estos pasos para levantar el proyecto en tu máquina local.

### Prerrequisitos
*   Tener instalado **Docker Desktop** y **Git**.
*   Tener las credenciales de tu proyecto de Firebase (`firebase_credentials.json`).

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Bootcamp-IA-P6/Proyecto1_Joaquin_Lazaro.git
cd Proyecto1_Joaquin_Lazaro
```

### 2. Configurar Secretos (¡Importante!)
Por seguridad, las claves no se suben al repositorio. Debes colocarlas manualmente:

1.  Crea un archivo `.env` dentro de la carpeta `/backend` con el siguiente contenido:
    ```ini
    FIREBASE_CRED_PATH=firebase_credentials.json
    FIREBASE_DB_NAME=(default)
    ```
2.  Coloca tu archivo `firebase_credentials.json` (descargado de Firebase Console) dentro de la carpeta `/backend`.

### 3. Arrancar el Sistema
Ejecuta el siguiente comando en la raíz del proyecto:

```bash
docker-compose up --build
```

Esperar hasta ver el mensaje `✅ Sistema iniciado` en la consola.

---

## 🕹️ Guía de Uso

Una vez arrancado Docker, el sistema expone dos puertos:

*   **Frontend (Web):** [http://localhost:8080](http://localhost:8080) 👈 **Entra aquí**
*   **Backend (API):** [http://localhost:8000/docs](http://localhost:8000/docs) (Documentación automática)

### Flujo de Trabajo

1.  **Iniciar Sesión:** Entra a la web y pulsa "Iniciar sesión con Google". Si es la primera vez, se creará tu perfil.
2.  **Configurar Tarifas:**
    *   Ve al menú lateral -> **Configuración**.
    *   Define el precio por segundo en parado (ej. 0.05€) y en movimiento (ej. 0.10€).
3.  **Iniciar Carrera:**
    *   Pulsa **INICIAR VIAJE**. El estado cambiará a "LIBRE" -> "PARADO".
    *   El taxímetro empieza a contar usando la tarifa de "Espera".
4.  **Alternar Marcha:**
    *   Pulsa **MARCHA** cuando el coche se mueva. El estado pasa a "MOVIMIENTO" (tarifa más cara).
    *   Pulsa **DETENERSE** en semáforos (tarifa más barata).
5.  **Finalizar:**
    *   Pulsa **FINALIZAR**. Se generará un **Ticket Digital** con el desglose exacto.
    *   El viaje se guarda automáticamente en el **Historial**.

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una arquitectura de microservicios orquestada con Docker Compose:

```
graph TD
    User[Usuario (Navegador)] -->|Puerto 8080| Frontend[Nginx (Frontend HTML/JS)]
    Frontend -->|API Fetch| Backend[FastAPI (Backend Python)]
    Backend -->|Auth| Firebase[Firebase Auth]
    Backend -->|Data| Firestore[Google Cloud Firestore]
    
    subgraph Docker Host
    Frontend
    Backend
    end
```

*   **Frontend:** Servidor Nginx ligero (`alpine`). Sirve archivos estáticos y gestiona la lógica visual con JavaScript Vanilla y Bootstrap.
*   **Backend:** Python 3.14 con FastAPI. Gestiona la lógica de negocio (`core.py`), autenticación (`auth.py`) y conexión a base de datos.
*   **Volúmenes:** Utilizamos volúmenes de Docker para inyectar las credenciales de forma segura sin quemarlas en la imagen.

---

## 🛠️ Tecnologías

*   **Lenguaje:** Python 3.14 & JavaScript (ES6)
*   **Frameworks:** FastAPI, Bootstrap 5.3
*   **Base de Datos:** Google Firestore (NoSQL)
*   **Contenedores:** Docker & Docker Compose
*   **Servidor Web:** Uvicorn (App) & Nginx (Web)