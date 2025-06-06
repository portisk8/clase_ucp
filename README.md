# Aplicación de Logística - Orden de Trabajo

Esta es una aplicación de escritorio para una empresa de logística, desarrollada en Python 3.12 usando Tkinter. Permite ingresar órdenes de trabajo con múltiples destinos, calcular la ruta óptima entre ellos (algoritmo del viajante o heurística), visualizar la ruta y guardar/cargar datos en JSON o SQLite.

## Estructura del proyecto

- `main.py`: Punto de entrada de la aplicación.
- `ui/`: Interfaz gráfica (Tkinter).
- `models/`: Clases de dominio (`OrdenTrabajo`, `Destino`).
- `services/`: Lógica de optimización de rutas.
- `storage/`: Guardado y carga de datos (JSON/SQLite).

## Instalación

1. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

```bash
python main.py
```

No se requieren servicios externos. Compatible con Python 3.12. 