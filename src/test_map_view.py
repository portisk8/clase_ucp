import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim

root = tk.Tk()
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)
#  # Frame para el mapa
mapa_frame = ttk.LabelFrame(main_frame, text="Mapa (OpenStreetMap)")
mapa_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
#Agregar Mapa
mapa = TkinterMapView(mapa_frame, width=800, height=800, corner_radius=0)
mapa.pack(fill="both", expand=True)
mapa.set_position(-34.6037, -58.3816)  # Buenos Aires por defecto
mapa.set_zoom(4)
# Agregar Marcador
marcadores = []
# mapa.set_marker(-34.6037, -58.3816, text="Buenos Aires")

#Location
direction = "lavalle 50, Corrientes, Argentina"
nombre = "Cuenca"
geolocator = Nominatim(user_agent="logistica_app")
location = geolocator.geocode(direction)
mapa.set_marker(location.latitude, location.longitude, text=nombre)
marcador = mapa.set_marker(location.latitude, location.longitude, text=nombre)
marcadores.append(marcador)
mapa.set_position(location.latitude, location.longitude)
mapa.set_zoom(4)

root.mainloop() 