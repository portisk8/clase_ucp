import json
from typing import List
from models.orden_trabajo import OrdenTrabajo
from models.destino import Destino

# Nota: Se asume que OrdenTrabajo y Destino tienen métodos para serializar/deserializar

def guardar_ordenes_json(ordenes: List[OrdenTrabajo], archivo: str):
    """
    Guarda una lista de órdenes de trabajo en un archivo JSON.
    """
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump([orden.to_dict() for orden in ordenes], f, ensure_ascii=False, indent=2)

def cargar_ordenes_json(archivo: str) -> List[OrdenTrabajo]:
    """
    Carga una lista de órdenes de trabajo desde un archivo JSON.
    """
    with open(archivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [OrdenTrabajo.from_dict(od) for od in data] 