# 🚕 Proyecto Taxímetro (CLI)

> Sistema de gestión de tarifas de taxi en tiempo real desarrollado en Python.

Este proyecto simula el funcionamiento profesional de un taxímetro digital. Permite iniciar trayectos, calcular costes en tiempo real según el estado (parado/movimiento), gestionar configuraciones y mantener un registro histórico y de auditoría.

## 🚀 Funcionalidades

### 🟢 Nivel Esencial (Core)
*   **Interfaz CLI Interactiva:** Menú dinámico y fácil de usar.
*   **Cálculo en Tiempo Real:** Algoritmo preciso para calcular tarifas según el tiempo transcurrido.
*   **Facturación:** Generación de factura detallada al finalizar el trayecto.

### 🟡 Nivel Medio (Robustez & Configuración)
*   **⚙️ Sistema de Configuración:** Precios y moneda configurables desde el propio programa (persistencia en `config.json`).
*   **📝 Logging de Auditoría:** Registro automático de eventos, errores y cambios de estado en `taximetro.log`.
*   **💾 Historial de Viajes:** Almacenamiento permanente de los trayectos finalizados en `history.txt`.
*   **🧪 Test Unitarios:** Batería de pruebas automatizadas con `pytest` para asegurar la precisión matemática y manejo de errores.

## 🛠️ Requisitos e Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/TU_USUARIO/Proyecto-Taximetro.git
    cd Proyecto-Taximetro
    ```

2.  **Configurar entorno virtual (Recomendado):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    Ahora es necesario instalar las librerías de testing.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```

## 🧪 Cómo ejecutar los Tests

El proyecto incluye tests unitarios para validar la lógica de negocio y casos borde (edge cases).

```bash
python -m pytest
```
*Deberías ver una salida en verde confirmando que todos los tests han pasado.*

## 📂 Estructura del Proyecto

```text
.
├── config.json         # Archivo de configuración persistente
├── history.txt         # Registro histórico de viajes (se genera al usar)
├── taximetro.log       # Log de eventos del sistema (se genera al usar)
├── main.py             # Punto de entrada principal
├── requirements.txt    # Dependencias del proyecto
├── src/
│   ├── __init__.py
│   ├── logica.py       # Motor de cálculo (Puro)
│   ├── configuracion.py# Gestor de lectura/escritura de config JSON
│   └── gestor_historial.py # Módulo de persistencia en texto
└── tests/
    ├── __init__.py
    └── test_logica.py  # Tests unitarios con Pytest
```

## 🔮 Roadmap

*   ✅ **Nivel Esencial:** CLI Básica y Lógica de Negocio.
*   ✅ **Nivel Medio:** Persistencia, Logs, Configuración y Tests.
*   🟠 **Nivel Avanzado:** Refactor a OOP (Clases), Autenticación y GUI.
*   🔴 **Nivel Experto:** Docker, Base de Datos y Web API.

---
*Desarrollado con ❤️ y Python.*
