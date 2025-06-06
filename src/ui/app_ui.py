import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from models.orden_trabajo import OrdenTrabajo
from models.destino import Destino
from services.ruta_optima import calcular_ruta_optima
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim

class AppUI:
    """
    Clase principal de la interfaz gráfica de usuario.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestión de Órdenes de Trabajo - Logística")
        self.root.geometry("1200x700")
        self.orden = OrdenTrabajo()
        self.ruta_optima = []
        self.ruta_geometry = None
        self.geolocator = Nominatim(user_agent="logistica_app")
        self.marcadores = []
        self._setup_widgets()

    def _setup_widgets(self):
        # Frame superior para formulario de destino
        form_frame = ttk.LabelFrame(self.root, text="Agregar Destino")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry = ttk.Entry(form_frame, width=30)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Dirección:").grid(row=0, column=2, padx=5, pady=5)
        self.direccion_entry = ttk.Entry(form_frame, width=40)
        self.direccion_entry.grid(row=0, column=3, padx=5, pady=5)

        agregar_btn = ttk.Button(form_frame, text="Agregar Destino", command=self._agregar_destino)
        agregar_btn.grid(row=0, column=4, padx=10, pady=5)

        # Frame principal para lista y mapa
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para lista de destinos
        lista_frame = ttk.LabelFrame(main_frame, text="Destinos de la Orden de Trabajo")
        lista_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.destinos_listbox = tk.Listbox(lista_frame, height=20, font=("Arial", 11), width=40)
        self.destinos_listbox.pack(side="left", fill="y", expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.destinos_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.destinos_listbox.config(yscrollcommand=scrollbar.set)

        # Frame para el mapa
        mapa_frame = ttk.LabelFrame(main_frame, text="Mapa (OpenStreetMap)")
        mapa_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.mapa = TkinterMapView(mapa_frame, width=600, height=500, corner_radius=0)
        self.mapa.pack(fill="both", expand=True)
        self.mapa.set_position(-34.6037, -58.3816)  # Buenos Aires por defecto
        self.mapa.set_zoom(4)

        # Frame para controles inferiores
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill="x", padx=10, pady=5)

        calcular_btn = ttk.Button(bottom_frame, text="Calcular Ruta Óptima", command=self._calcular_ruta)
        calcular_btn.pack(side="left", padx=5)

        # Frame para mostrar la ruta óptima
        ruta_frame = ttk.LabelFrame(self.root, text="Ruta Óptima Generada")
        ruta_frame.pack(fill="x", padx=10, pady=5)
        self.ruta_label = ttk.Label(ruta_frame, text="(La ruta óptima aparecerá aquí)", font=("Arial", 11))
        self.ruta_label.pack(padx=5, pady=5)

        # Frame para visualización gráfica
        self.grafica_frame = ttk.LabelFrame(self.root, text="Visualización de la Ruta (Gráfico)")
        self.grafica_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas = None

    def _agregar_destino(self):
        nombre = self.nombre_entry.get().strip()
        direccion = self.direccion_entry.get().strip()
        if not nombre or not direccion:
            messagebox.showwarning("Campos incompletos", "Por favor, ingresa nombre y dirección.")
            return
        # Geocodificar dirección
        try:
            location = self.geolocator.geocode(direccion)
        except Exception as e:
            messagebox.showerror("Error de geocodificación", f"No se pudo conectar al servicio de geocodificación: {e}")
            return
        if not location:
            messagebox.showwarning("Dirección no encontrada", "No se pudo encontrar la dirección en el mapa.")
            return
        destino = Destino(nombre, direccion, lat=location.latitude, lon=location.longitude)
        self.orden.agregar_destino(destino)
        self._actualizar_lista_destinos()
        self.nombre_entry.delete(0, tk.END)
        self.direccion_entry.delete(0, tk.END)
        # Agregar marcador en el mapa
        marcador = self.mapa.set_marker(location.latitude, location.longitude, text=nombre)
        self.marcadores.append(marcador)
        self.mapa.set_position(location.latitude, location.longitude)
        self.mapa.set_zoom(12)

    def _actualizar_lista_destinos(self):
        self.destinos_listbox.delete(0, tk.END)
        for idx, destino in enumerate(self.orden.obtener_destinos(), 1):
            self.destinos_listbox.insert(tk.END, f"{idx}. {destino.nombre} - {destino.direccion}")

    def _calcular_ruta(self):
        destinos = self.orden.obtener_destinos()
        if len(destinos) < 2:
            messagebox.showinfo("Información insuficiente", "Agrega al menos dos destinos para calcular la ruta.")
            return
        try:
            resultado = calcular_ruta_optima(destinos)
        except Exception as e:
            messagebox.showerror("Error de ruteo", str(e))
            return
        orden_destinos = resultado["orden_destinos"]
        self.ruta_geometry = resultado["geometry"]
        self.ruta_optima = [destinos[i] for i in orden_destinos]
        ruta_str = " → ".join([d.nombre for d in self.ruta_optima])
        self.ruta_label.config(text=ruta_str)
        self._mostrar_grafica()
        self._dibujar_ruta_en_mapa()

    def _mostrar_grafica(self):
        # Elimina el gráfico anterior si existe
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        if not self.ruta_optima or len(self.ruta_optima) < 2:
            return
        # Generar coordenadas ficticias para visualización
        puntos = self._generar_coordenadas(len(self.ruta_optima))
        fig, ax = plt.subplots(figsize=(6, 4))
        x, y = zip(*puntos)
        ax.plot(x, y, marker='o', linestyle='-', color='blue')
        for i, destino in enumerate(self.ruta_optima):
            ax.text(x[i], y[i], destino.nombre, fontsize=9, ha='right')
        ax.set_title('Ruta Óptima (Visualización Simbólica)')
        ax.axis('off')
        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(fig, master=self.grafica_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def _generar_coordenadas(self, n):
        # Genera puntos en círculo para visualización simbólica
        import math
        radio = 3
        return [
            (radio * math.cos(2 * math.pi * i / n), radio * math.sin(2 * math.pi * i / n))
            for i in range(n)
        ]

    def _dibujar_ruta_en_mapa(self):
        self.mapa.delete_all_path()
        if self.ruta_geometry and self.ruta_geometry['coordinates']:
            # OpenRouteService devuelve (lon, lat), tkintermapview espera (lat, lon)
            coords = [(lat, lon) for lon, lat in self.ruta_geometry['coordinates']]
            self.mapa.set_path(coords)

    def run(self):
        self.root.mainloop() 