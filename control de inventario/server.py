# ============================================================
#  server.py — Vasconcellos Automotriz (VERSIÓN SQLITE)
#  Funciona SIN MySQL, SIN Workbench, SIN instalar nada extra.
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# ============================================================
# CONEXIÓN A SQLITE
# ============================================================

def get_db():
    return sqlite3.connect("inventario.db", check_same_thread=False)

# Crear tablas
def init_db():
    db = get_db()
    cur = db.cursor()

    # Tabla productos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_producto TEXT NOT NULL,
            etiqueta TEXT,
            stock INTEGER,
            precio REAL
        )
    """)

    # Tabla ventas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER,
            precio_unitario REAL,
            total REAL,
            fecha TEXT,
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    """)

    # Tabla compras
    cur.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER,
            precio_compra REAL,
            total_compra REAL,
            fecha TEXT,
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    """)

    # Tabla lavados
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lavados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            detalles TEXT,
            precio REAL,
            fecha TEXT
        )
    """)

    db.commit()
    db.close()

init_db()

# ============================================================
# PRODUCTOS
# ============================================================

@app.get("/productos")
def productos_get():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT id, nombre_producto, etiqueta, stock, precio FROM productos ORDER BY id ASC")
    filas = cur.fetchall()

    res = [{"id": f[0], "nombre_producto": f[1], "etiqueta": f[2], "stock": f[3], "precio": f[4]} for f in filas]

    db.close()
    return jsonify(res)


@app.post("/productos")
def productos_post():
    data = request.json
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO productos (nombre_producto, etiqueta, stock, precio)
        VALUES (?, ?, ?, ?)
    """, (data["nombre_producto"], data["etiqueta"], data["stock"], data["precio"]))

    db.commit()
    db.close()
    return jsonify({"msg": "ok"})


@app.put("/productos/<int:id>")
def productos_put(id):
    data = request.json
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        UPDATE productos
        SET nombre_producto=?, etiqueta=?, stock=?, precio=?
        WHERE id=?
    """, (data["nombre_producto"], data["etiqueta"], data["stock"], data["precio"], id))

    db.commit()
    db.close()
    return jsonify({"msg": "ok"})


@app.delete("/productos/<int:id>")
def productos_del(id):
    db = get_db()
    cur = db.cursor()

    cur.execute("DELETE FROM productos WHERE id=?", (id,))
    db.commit()
    db.close()
    return jsonify({"msg": "ok"})

# ============================================================
# CATEGORÍAS
# ============================================================

@app.get("/categorias")
def categorias_get():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT DISTINCT etiqueta FROM productos ORDER BY etiqueta ASC")
    categorias = [c[0] for c in cur.fetchall() if c[0]]

    db.close()
    return jsonify(categorias)

# ============================================================
# VENTAS
# ============================================================

@app.post("/ventas")
def ventas_post():
    data = request.json
    producto_id = data["producto_id"]
    cantidad = data["cantidad"]

    db = get_db()
    cur = db.cursor()

    # Obtener stock y precio
    cur.execute("SELECT stock, precio FROM productos WHERE id=?", (producto_id,))
    fila = cur.fetchone()

    if not fila:
        return jsonify({"error": "Producto no existe"})

    stock_actual, precio_unitario = fila

    if stock_actual < cantidad:
        return jsonify({"error": "Stock insuficiente"})

    total = precio_unitario * cantidad

    # Registrar venta
    cur.execute("""
        INSERT INTO ventas (producto_id, cantidad, precio_unitario, total, fecha)
        VALUES (?, ?, ?, ?, DATETIME('now'))
    """, (producto_id, cantidad, precio_unitario, total))

    # Descontar stock
    cur.execute("UPDATE productos SET stock = stock - ? WHERE id=?", (cantidad, producto_id))

    db.commit()
    db.close()
    return jsonify({"msg": "ok"})


@app.get("/ventas")
def ventas_get():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT v.id, p.nombre_producto, v.cantidad, v.precio_unitario, v.total, v.fecha
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        ORDER BY v.fecha ASC
    """)

    filas = cur.fetchall()

    res = [{
        "id": f[0],
        "nombre_producto": f[1],
        "cantidad": f[2],
        "precio_unitario": f[3],
        "total": f[4],
        "fecha": f[5],
    } for f in filas]

    db.close()
    return jsonify(res)


@app.delete("/ventas/<int:id>")
def ventas_delete(id):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT producto_id, cantidad FROM ventas WHERE id=?", (id,))
    fila = cur.fetchone()

    if not fila:
        return jsonify({"error": "Venta no encontrada"}), 404

    producto_id, cantidad = fila

    # Devolver stock
    cur.execute("UPDATE productos SET stock = stock + ? WHERE id=?", (cantidad, producto_id))

    # Borrar venta
    cur.execute("DELETE FROM ventas WHERE id=?", (id,))

    db.commit()
    db.close()
    return jsonify({"msg": "ok"})

# ============================================================
# COMPRAS
# ============================================================

@app.post("/compras")
def compras_post():
    data = request.json
    producto_id = data["producto_id"]
    cantidad = data["cantidad"]
    precio_compra = data["precio_compra"]

    total = cantidad * precio_compra

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO compras (producto_id, cantidad, precio_compra, total_compra, fecha)
        VALUES (?, ?, ?, ?, DATETIME('now'))
    """, (producto_id, cantidad, precio_compra, total))

    # Subir stock
    cur.execute("UPDATE productos SET stock = stock + ? WHERE id=?", (cantidad, producto_id))

    db.commit()
    db.close()
    return jsonify({"msg": "ok"})


@app.get("/compras")
def compras_get():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT c.id, p.nombre_producto, c.cantidad, c.precio_compra, 
               c.total_compra, c.fecha
        FROM compras c
        JOIN productos p ON c.producto_id = p.id
        ORDER BY c.fecha ASC
    """)

    filas = cur.fetchall()

    res = [{
        "id": f[0],
        "nombre_producto": f[1],
        "cantidad": f[2],
        "precio_compra": f[3],
        "total_compra": f[4],
        "fecha": f[5],
    } for f in filas]

    db.close()
    return jsonify(res)


@app.delete("/compras/<int:id>")
def compras_delete(id):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT producto_id, cantidad FROM compras WHERE id=?", (id,))
    fila = cur.fetchone()

    if not fila:
        return jsonify({"error": "Compra no encontrada"}), 404

    producto_id, cantidad = fila

    # Obtener stock actual
    cur.execute("SELECT stock FROM productos WHERE id=?", (producto_id,))
    stock_actual = cur.fetchone()[0]

    # Evitar dejar stock negativo
    if stock_actual < cantidad:
        return jsonify({"error": "No se puede eliminar: dejaría el stock negativo."}), 400

    # Ajustar stock
    cur.execute("UPDATE productos SET stock = stock - ? WHERE id=?", (cantidad, producto_id))

    # Borrar compra
    cur.execute("DELETE FROM compras WHERE id=?", (id,))

    db.commit()
    db.close()
    return jsonify({"msg": "ok"})

# ============================================================
# LAVADOS
# ============================================================

@app.post("/lavados")
def lavados_post():
    data = request.json

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO lavados (tipo, detalles, precio, fecha)
        VALUES (?, ?, ?, DATETIME('now'))
    """, (data["tipo"], data["detalles"], data["precio"]))

    db.commit()
    db.close()
    return jsonify({"msg": "ok"})


@app.get("/lavados")
def lavados_get():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT id, tipo, detalles, precio, fecha FROM lavados ORDER BY fecha ASC")
    filas = cur.fetchall()

    res = [{
        "id": f[0],
        "tipo": f[1],
        "detalles": f[2],
        "precio": f[3],
        "fecha": f[4],
    } for f in filas]

    db.close()
    return jsonify(res)


@app.delete("/lavados/<int:id>")
def lavados_delete(id):
    db = get_db()
    cur = db.cursor()

    cur.execute("DELETE FROM lavados WHERE id=?", (id,))
    db.commit()
    db.close()

    return jsonify({"msg": "ok"})

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    print("🚀 Servidor Flask (SQLite) iniciando en http://127.0.0.1:5000")
    app.run(debug=True)
