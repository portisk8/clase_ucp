class Destino:
    """
    Representa un destino con nombre, dirección y coordenadas.
    """
    def __init__(self, nombre: str, direccion: str, lat: float = None, lon: float = None):
        self.nombre = nombre
        self.direccion = direccion
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return f"Destino(nombre={self.nombre}, direccion={self.direccion}, lat={self.lat}, lon={self.lon})"

    def to_dict(self):
        return {'nombre': self.nombre, 'direccion': self.direccion, 'lat': self.lat, 'lon': self.lon}

    @classmethod
    def from_dict(cls, data):
        return cls(data['nombre'], data['direccion'], data.get('lat'), data.get('lon')) 