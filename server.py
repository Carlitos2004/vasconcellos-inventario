# ============================================================
#  server.py — API Flask Final para Vasconcellos Automotriz
#  (Productos, Ventas, Compras, Lavados + ELIMINAR movimientos)
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============================================================
# CONEXIÓN A MYSQL
# ============================================================

def get_db():
    """
    Abre una conexión nueva a la base de datos.
    Cambia la password si tu root tiene otra clave.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2004",   # 🔴 CAMBIA ESTO A TU CLAVE
        database="inventario_automotriz"
    )

# ============================================================
# PRODUCTOS
# ============================================================

@app.get("/productos")
def productos_get():
    """
    Lista todos los productos para el inventario.
    """
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, nombre_producto, etiqueta, stock, precio
        FROM productos
        ORDER BY id ASC
    """)
    filas = cur.fetchall()

    res = [
        {
            "id": f[0],
            "nombre_producto": f[1],
            "etiqueta": f[2],
            "stock": f[3],
            "precio": f[4],
        }
        for f in filas
    ]

    db.close()
    return jsonify(res)


@app.post("/productos")
def productos_post():
    """
    Crea un nuevo producto.
    """
    data = request.json
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO productos (nombre_producto, etiqueta, stock, precio)
        VALUES (%s, %s, %s, %s)
    """, (data["nombre_producto"], data["etiqueta"], data["stock"], data["precio"]))

    db.commit()
    db.close()
    return jsonify({"msg": "ok"})


@app.put("/productos/<int:id>")
def productos_put(id):
    """
    Edita nombre, etiqueta, stock y precio de un producto.
    """
    data = request.json
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        UPDATE productos
        SET nombre_producto=%s, etiqueta=%s, stock=%s, precio=%s
        WHERE id=%s
    """, (data["nombre_producto"], data["etiqueta"], data["stock"], data["precio"], id))

    db.commit()
    db.close()
    return jsonify({"msg": "ok"})


@app.delete("/productos/<int:id>")
def productos_del(id):
    """
    Elimina un producto.
    (OJO: si tiene ventas/compras asociadas, MySQL puede dar error
    por las llaves foráneas.)
    """
    db = get_db()
    cur = db.cursor()

    cur.execute("DELETE FROM productos WHERE id=%s", (id,))
    db.commit()
    db.close()
    return jsonify({"msg": "ok"})

# ============================================================
# CATEGORÍAS
# ============================================================

@app.get("/categorias")
def categorias_get():
    """
    Devuelve la lista de etiquetas únicas para armar
    los select de categorías.
    """
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
    """
    Registra una venta:
    - Calcula total (precio producto * cantidad)
    - Descuenta stock
    """
    data = request.json
    producto_id = data["producto_id"]
    cantidad = data["cantidad"]

    db = get_db()
    cur = db.cursor()

    # Ver stock actual y precio del producto
    cur.execute("SELECT stock, precio, nombre_producto FROM productos WHERE id=%s",
                (producto_id,))
    fila = cur.fetchone()

    if not fila:
        db.close()
        return jsonify({"error": "Producto no existe"})

    stock_actual, precio_unitario, nombre_producto = fila

    if stock_actual < cantidad:
        db.close()
        return jsonify({"error": "Stock insuficiente"})

    total = precio_unitario * cantidad

    # Registrar venta
    cur.execute("""
        INSERT INTO ventas (producto_id, cantidad, precio_unitario, total, fecha)
        VALUES (%s, %s, %s, %s, NOW())
    """, (producto_id, cantidad, precio_unitario, total))

    # Descontar stock
    cur.execute("UPDATE productos SET stock = stock - %s WHERE id=%s",
                (cantidad, producto_id))

    db.commit()
    db.close()

    return jsonify({"msg": "ok"})


@app.get("/ventas")
def ventas_get():
    """
    Lista todas las ventas con nombre de producto.
    """
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT v.id, p.nombre_producto, v.cantidad, v.precio_unitario, v.total, v.fecha
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        ORDER BY v.fecha ASC
    """)

    filas = cur.fetchall()
    res = [
        {
            "id": f[0],
            "nombre_producto": f[1],
            "cantidad": f[2],
            "precio_unitario": f[3],
            "total": f[4],
            "fecha": f[5],
        }
        for f in filas
    ]

    db.close()
    return jsonify(res)


@app.delete("/ventas/<int:id>")
def ventas_delete(id):
    """
    Elimina una venta:
    - Devuelve el stock al producto (stock + cantidad).
    """
    db = get_db()
    cur = db.cursor()

    # Buscar la venta
    cur.execute("SELECT producto_id, cantidad FROM ventas WHERE id=%s", (id,))
    fila = cur.fetchone()

    if not fila:
        db.close()
        return jsonify({"error": "Venta no encontrada"}), 404

    producto_id, cantidad = fila

    # Devolver stock
    cur.execute(
        "UPDATE productos SET stock = stock + %s WHERE id=%s",
        (cantidad, producto_id)
    )

    # Eliminar la venta
    cur.execute("DELETE FROM ventas WHERE id=%s", (id,))

    db.commit()
    db.close()
    return jsonify({"msg": "ok"})

# ============================================================
# COMPRAS
# ============================================================

@app.post("/compras")
def compras_post():
    """
    Registra una compra:
    - Calcula total (precio_compra * cantidad)
    - Suma stock al producto
    """
    data = request.json
    producto_id = data["producto_id"]
    cantidad = data["cantidad"]
    precio_compra = data["precio_compra"]

    total = cantidad * precio_compra

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO compras (producto_id, cantidad, precio_compra, total_compra, fecha)
        VALUES (%s, %s, %s, %s, NOW())
    """, (producto_id, cantidad, precio_compra, total))

    # Sumar stock
    cur.execute(
        "UPDATE productos SET stock = stock + %s WHERE id=%s",
        (cantidad, producto_id)
    )

    db.commit()
    db.close()

    return jsonify({"msg": "ok"})


@app.get("/compras")
def compras_get():
    """
    Lista todas las compras con nombre de producto.
    """
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
    res = [
        {
            "id": f[0],
            "nombre_producto": f[1],
            "cantidad": f[2],
            "precio_compra": f[3],
            "total_compra": f[4],
            "fecha": f[5],
        }
        for f in filas
    ]

    db.close()
    return jsonify(res)


@app.delete("/compras/<int:id>")
def compras_delete(id):
    """
    Elimina una compra:
    - Resta del stock la cantidad que había entrado.
    - Si dejaría el stock negativo, no deja borrar.
    """
    db = get_db()
    cur = db.cursor()

    # Buscar la compra
    cur.execute("SELECT producto_id, cantidad FROM compras WHERE id=%s", (id,))
    fila = cur.fetchone()

    if not fila:
        db.close()
        return jsonify({"error": "Compra no encontrada"}), 404

    producto_id, cantidad = fila

    # Ver stock actual
    cur.execute("SELECT stock FROM productos WHERE id=%s", (producto_id,))
    fila_stock = cur.fetchone()

    if not fila_stock:
        db.close()
        return jsonify({"error": "Producto no encontrado para la compra"}), 404

    stock_actual = fila_stock[0]

    if stock_actual < cantidad:
        db.close()
        return jsonify({
            "error": "No se puede eliminar la compra porque dejaría el stock negativo."
        }), 400

    # Ajustar stock y borrar compra
    cur.execute(
        "UPDATE productos SET stock = stock - %s WHERE id=%s",
        (cantidad, producto_id)
    )
    cur.execute("DELETE FROM compras WHERE id=%s", (id,))

    db.commit()
    db.close()
    return jsonify({"msg": "ok"})

# ============================================================
# LAVADOS / SERVICIOS
# ============================================================

@app.post("/lavados")
def lavados_post():
    """
    Registra un lavado/servicio con tipo, detalles, precio y fecha NOW().
    """
    data = request.json
    tipo = data["tipo"]
    detalles = data["detalles"]
    precio = data["precio"]

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO lavados (tipo, detalles, precio, fecha)
        VALUES (%s, %s, %s, NOW())
    """, (tipo, detalles, precio))

    db.commit()
    db.close()

    return jsonify({"msg": "ok"})


@app.get("/lavados")
def lavados_get():
    """
    Lista todos los lavados/servicios.
    """
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, tipo, detalles, precio, fecha
        FROM lavados
        ORDER BY fecha ASC
    """)

    filas = cur.fetchall()
    res = [
        {
            "id": f[0],
            "tipo": f[1],
            "detalles": f[2],
            "precio": f[3],
            "fecha": f[4],
        }
        for f in filas
    ]

    db.close()
    return jsonify(res)
@app.delete("/lavados/<int:id>")
def lavados_delete(id):
    """
    Elimina un lavado/servicio por ID.
    """
    db = get_db()
    cur = db.cursor()

    cur.execute("DELETE FROM lavados WHERE id=%s", (id,))
    db.commit()

    db.close()
    return jsonify({"msg": "ok"})


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    print("🚀 Servidor Flask iniciando. (http://127.0.0.1:5000)")
    app.run(debug=True)
