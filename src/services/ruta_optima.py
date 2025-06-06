import openrouteservice
from openrouteservice import convert
from typing import List

import openrouteservice.optimization
from models.destino import Destino
import os
from dotenv import load_dotenv

load_dotenv()
ORS_API_KEY = os.getenv("ORS_API_KEY")

class DemasiadosDestinosError(Exception):
    pass

def calcular_ruta_optima(destinos: List[Destino]) -> dict:
    """
    Calcula la ruta óptima real usando OpenRouteService.
    Devuelve un dict con 'orden_destinos' (índices en el orden óptimo) y 'geometry' (polilínea).
    """
    if not ORS_API_KEY:
        raise Exception("No se encontró la API key de OpenRouteService.")
    if len(destinos) < 2:
        return {"orden_destinos": list(range(len(destinos))), "geometry": None}
    if len(destinos) > 10:
        raise DemasiadosDestinosError("La API gratuita de OpenRouteService solo permite hasta 10 destinos por ruta.")

    client = openrouteservice.Client(key=ORS_API_KEY)
    coords = []
    for d in destinos:
        if d.lat is not None and d.lon is not None:
            coords.append([d.lon, d.lat])
        else:
            raise Exception("Faltan coordenadas en uno o más destinos.")

    # Si solo hay 2 destinos, usar directions directamente
    if len(coords) == 2:
        route = client.directions(coords, profile='driving-car', format='geojson')
        geometry = route['features'][0]['geometry']
        return {"orden_destinos": [0, 1], "geometry": geometry}

    # El primer destino es solo start/end, los jobs son los destinos 1...N
    try:
        jobs = [{"id": i+1, "location": coord} for i, coord in enumerate(coords[1:])]
        vehicles = [{"id": 1, "start": coords[0], "end": coords[0]}]
        result = client.optimization(jobs=jobs, vehicles=vehicles)
    except openrouteservice.exceptions.ApiError as e:
        print("Payload enviado:", {"jobs": jobs, "vehicles": vehicles})
        raise Exception(f"Error de OpenRouteService: {e}")
    # El orden óptimo es [0] + [job['job'] + 1] (ya que jobs empieza en 1 y corresponde a coords[1:])
    orden_destinos = [0] + [step['job'] for step in result['routes'][0]['steps']]
    waypoints = [coords[i] for i in orden_destinos]
    route = client.directions(waypoints, profile='driving-car', format='geojson')
    geometry = route['features'][0]['geometry']
    return {"orden_destinos": orden_destinos, "geometry": geometry} 