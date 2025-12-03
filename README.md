# 🚕 Proyecto Taxímetro (CLI)

> Sistema de gestión de tarifas de taxi en tiempo real basado en consola (Python).

Este proyecto simula el funcionamiento de un taxímetro digital, permitiendo iniciar trayectos, alternar entre estados (parado/movimiento) y generar facturas detalladas.

## 🚀 Funcionalidades (Nivel Esencial)

*   **Interfaz CLI Interactiva:** Menú dinámico que muestra solo las opciones lógicas según el estado actual.
*   **Cálculo en Tiempo Real:**
    *   🚖 **En Movimiento:** 0.05€ / segundo.
    *   🛑 **Parado:** 0.02€ / segundo.
*   **Reportes Intermedios:** Muestra el coste y duración de cada tramo al cambiar de estado.
*   **Factura Detallada:** Al finalizar, genera un desglose de tiempos y costes divididos por estado.
*   **Flujo Continuo:** Permite iniciar múltiples trayectos sin cerrar el programa.

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

3.  **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```

## 📂 Estructura del Proyecto

```text
.
├── main.py           # Punto de entrada y lógica de control de flujo
├── src/
│   ├── __init__.py
│   └── logica.py     # Motor de cálculo de tarifas (Puro)
└── README.md