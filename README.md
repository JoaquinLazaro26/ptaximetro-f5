# 🚖 Proyecto Taxímetro

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-yellow)
![Status](https://img.shields.io/badge/Status-Completed-success)

Aplicación de escritorio desarrollada en Python que simula el funcionamiento lógico y contable de un taxímetro digital incremental. Evolucionado desde un script básico hasta una aplicación completa con Arquitectura MVC, Persistencia y GUI profesional.

## ✨ Características Principales

- **Arquitectura MVC:** Separación estricta entre Lógica (`modelo`), Interfaz (`gui`) y Control.
- **Interfaz Gráfica (GUI):** Desarrollada con `tkinter`, incluye:
  - Diseño moderno y responsivo.
  - Actualización en tiempo real sin bloqueo (Event Loop).
  - Panel de Login con autenticación segura (Hash + Salt).
- **Lógica de Negocio Incremental:**
  - Tarifas dinámicas: "Parado" vs "En Movimiento".
  - Cálculo preciso de costes y tiempos.
- **Persistencia de Datos:**
  - `users.json`: Base de datos de usuarios encriptada.
  - `config.json`: Configuración persistente de tarifas.
  - `history.txt`: Registro de auditoría inmutable de carreras.
- **Logging Profesional:** Trazabilidad completa de acciones de usuario y errores del sistema.

## 📂 Estructura del Proyecto

```text
ptaximetro/
├── main.py                 # Punto de entrada (Orquestador & DI)
├── config.json             # Configuración (Autogenerado)
├── users.json              # Usuarios (Autogenerado)
├── history.txt             # Historial de carreras
├── taximetro.log           # Logs técnicos
└── src/
    ├── modelo.py           # Lógica de Negocio (Core)
    ├── gui.py              # Interfaz Gráfica (Vista)
    ├── autenticacion.py    # Gestión de Seguridad
    ├── configuracion.py    # Gestión de Configuración
    ├── gestor_historial.py # Gestión de Logs de Negocio
    ├── estilos.py          # Definición de Tema/UI
    └── constantes.py       # Constantes Globales
```

## 🚀 Instalación y Uso

1. **Requisitos:** Python 3.x instalado. No requiere librerías externas (solo librería estándar).

2. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/proyecto-taximetro.git
   cd proyecto-taximetro
   ```

3. **Ejecutar la aplicación:**
   *Es importante ejecutar desde la raíz del proyecto:*
   ```bash
   python main.py
   ```

4. **Credenciales por defecto:**
   Al iniciar, si no existe base de datos, puedes editar `users.json` o usar el usuario semilla si se configuró.

## ⚙️ Configuración

Las tarifas se pueden modificar desde la propia interfaz gráfica (botón ⚙️ en el Dashboard) o editando manualmente el archivo `config.json` (respetando el formato JSON).

> **Nota:** La configuración está bloqueada mientras haya una carrera en curso por seguridad.

## 👨‍💻 Autor

Joaquin Alonso Lazaro Marquez
