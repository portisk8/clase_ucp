from typing import List
from .destino import Destino

class OrdenTrabajo:
    """
    Representa una orden de trabajo con múltiples destinos.
    """
    def __init__(self):
        self.destinos: List[Destino] = []

    def agregar_destino(self, destino: Destino):
        self.destinos.append(destino)

    def quitar_destino(self, destino: Destino):
        self.destinos.remove(destino)

    def obtener_destinos(self) -> List[Destino]:
        return self.destinos

    def to_dict(self):
        return {
            'destinos': [d.to_dict() for d in self.destinos]
        }

    @classmethod
    def from_dict(cls, data):
        orden = cls()
        for d in data.get('destinos', []):
            orden.agregar_destino(Destino.from_dict(d))
        return orden 