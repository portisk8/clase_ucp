import sqlite3
from typing import List
from models.orden_trabajo import OrdenTrabajo
from models.destino import Destino

DB_NAME = "ordenes.db"

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orden_trabajo (
        id INTEGER PRIMARY KEY AUTOINCREMENT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS destino (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orden_id INTEGER,
        nombre TEXT,
        direccion TEXT,
        FOREIGN KEY (orden_id) REFERENCES orden_trabajo(id)
    )''')
    conn.commit()
    conn.close()

def guardar_orden(orden: OrdenTrabajo):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO orden_trabajo DEFAULT VALUES')
    orden_id = c.lastrowid
    for destino in orden.obtener_destinos():
        c.execute('INSERT INTO destino (orden_id, nombre, direccion) VALUES (?, ?, ?)',
                  (orden_id, destino.nombre, destino.direccion))
    conn.commit()
    conn.close()

def cargar_ordenes() -> List[OrdenTrabajo]:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id FROM orden_trabajo')
    ordenes = []
    for (orden_id,) in c.fetchall():
        c.execute('SELECT nombre, direccion FROM destino WHERE orden_id=?', (orden_id,))
        destinos = [Destino(nombre, direccion) for nombre, direccion in c.fetchall()]
        orden = OrdenTrabajo()
        for d in destinos:
            orden.agregar_destino(d)
        ordenes.append(orden)
    conn.close()
    return ordenes 