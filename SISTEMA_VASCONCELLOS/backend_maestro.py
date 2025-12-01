# ==============================================================================
#  BACKEND MAESTRO - VASCONCELLOS AUTOMOTRIZ
#  Versión Final: Fusión de Inventario (sistema.py) + Agenda Premium (app.py)
# ==============================================================================

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import sqlite3
import os
import glob
import locale

# --- CONFIGURACIÓN INICIAL ---
app = Flask(__name__)
app.secret_key = 'vasconcellos_secret_key_pro'
CORS(app) # Vital para que index.html funcione con este backend

# Configuración de idioma español para fechas
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    except:
        print("⚠️ Advertencia: No se pudo configurar idioma local.")

# --- 1. GESTIÓN INTELIGENTE DE BASE DE DATOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Prioridad: inventario_automotriz.db (la que tiene tus datos reales)
POSIBLES_NOMBRES = ["inventario_automotriz.db", "inventario.db"]
DB_PATH = None

for nombre in POSIBLES_NOMBRES:
    ruta_temp = os.path.join(BASE_DIR, nombre)
    if os.path.exists(ruta_temp):
        DB_PATH = ruta_temp
        print(f"✅ Base de datos cargada: {nombre}")
        break

# Si no encuentra ninguna, crea una nueva por defecto
if not DB_PATH:
    DB_PATH = os.path.join(BASE_DIR, "inventario_automotriz.db")
    print(f"⚠️ No se encontró base de datos. Se creará: {DB_PATH}")

# Conexión SQLAlchemy (Para la Agenda)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Conexión SQLite Cruda (Para el Inventario Legacy)
def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# --- 2. MODELOS SQLALCHEMY (AGENDA) ---
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Pendiente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- 3. INICIALIZACIÓN DE TABLAS (HÍBRIDO) ---
def init_all_tables():
    # 1. Tablas de Agenda (SQLAlchemy)
    with app.app_context():
        db.create_all()

    # 2. Tablas de Inventario (SQLite Raw - Lógica de sistema.py)
    conn = get_db()
    cur = conn.cursor()
    
    # Productos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_producto TEXT NOT NULL,
            etiqueta TEXT,
            stock INTEGER,
            precio REAL,
            image_url TEXT
        )
    """)
    # Ventas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER,
            total REAL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Compras, Lavados, Movimientos (Vitales para sistema.py)
    cur.execute("CREATE TABLE IF NOT EXISTS compras (id INTEGER PRIMARY KEY AUTOINCREMENT, producto_id INTEGER, cantidad INTEGER, costo REAL, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS lavados (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT, detalles TEXT, precio REAL, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS movimientos (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT, descripcion TEXT, monto REAL, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    
    conn.commit()
    conn.close()

# Ejecutamos la creación al inicio
init_all_tables()

# --- 4. FILTROS VISUALES ---
@app.template_filter('fecha_bonita')
def fecha_bonita_filter(fecha_str):
    if not fecha_str: return {'dia': '--', 'mes': '---'}
    try:
        dt = datetime.strptime(fecha_str, '%Y-%m-%d')
        return {'dia': dt.strftime('%d'), 'mes': dt.strftime('%b').upper().replace('.', '')}
    except: return {'dia': '??', 'mes': '???'}


# ==============================================================================
#  SECCIÓN A: API INVENTARIO (Lógica exacta de sistema.py)
# ==============================================================================

@app.route("/productos", methods=["GET"])
def productos_get():
    db_conn = get_db()
    cur = db_conn.cursor()
    # Intentamos leer image_url
    try:
        cur.execute("SELECT id, nombre_producto, etiqueta, stock, precio, image_url FROM productos")
    except:
        cur.execute("SELECT id, nombre_producto, etiqueta, stock, precio FROM productos")
    
    filas = cur.fetchall()
    res = []
    for f in filas:
        item = { "id": f[0], "nombre_producto": f[1], "etiqueta": f[2], "stock": f[3], "precio": f[4] }
        if len(f) > 5: item["image_url"] = f[5]
        res.append(item)
    
    db_conn.close()
    return jsonify(res)

@app.route("/productos", methods=["POST"])
def productos_post():
    data = request.json
    db_conn = get_db()
    cur = db_conn.cursor()
    cur.execute("INSERT INTO productos (nombre_producto, etiqueta, stock, precio) VALUES (?, ?, ?, ?)", 
                (data["nombre_producto"], data["etiqueta"], data["stock"], data["precio"]))
    db_conn.commit()
    db_conn.close()
    return jsonify({"msg": "Producto creado"})

@app.route("/productos/<int:id>", methods=["PUT"])
def productos_put(id):
    data = request.json
    db_conn = get_db()
    cur = db_conn.cursor()
    cur.execute("UPDATE productos SET nombre_producto=?, etiqueta=?, stock=?, precio=? WHERE id=?", 
                (data["nombre_producto"], data["etiqueta"], data["stock"], data["precio"], id))
    db_conn.commit()
    db_conn.close()
    return jsonify({"msg": "Producto actualizado"})

@app.route("/productos/<int:id>", methods=["DELETE"])
def productos_delete(id):
    db_conn = get_db()
    cur = db_conn.cursor()
    cur.execute("DELETE FROM productos WHERE id=?", (id,))
    db_conn.commit()
    db_conn.close()
    return jsonify({"msg": "Producto eliminado"})

@app.route("/ventas", methods=["GET", "POST"])
def ventas_route():
    db_conn = get_db()
    cur = db_conn.cursor()
    if request.method == "POST":
        data = request.json
        cur.execute("INSERT INTO ventas (producto_id, cantidad, total) VALUES (?, ?, ?)", (data["producto_id"], data["cantidad"], data["total"]))
        cur.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (data["cantidad"], data["producto_id"]))
        cur.execute("INSERT INTO movimientos (tipo, descripcion, monto) VALUES (?, ?, ?)", ("INGRESO", f"Venta ID: {data['producto_id']}", data['total']))
        db_conn.commit()
        db_conn.close()
        return jsonify({"msg": "Venta ok"})
    else:
        cur.execute("SELECT v.id, p.nombre_producto, v.cantidad, v.total, v.fecha FROM ventas v JOIN productos p ON v.producto_id = p.id ORDER BY v.fecha DESC")
        res = [{"id":f[0], "producto":f[1], "cantidad":f[2], "total":f[3], "fecha":f[4]} for f in cur.fetchall()]
        db_conn.close()
        return jsonify(res)

@app.route("/lavados", methods=["GET", "POST"])
def lavados_route():
    db_conn = get_db()
    cur = db_conn.cursor()
    if request.method == "POST":
        data = request.json
        cur.execute("INSERT INTO lavados (tipo, detalles, precio, fecha) VALUES (?, ?, ?, DATETIME('now'))", (data["tipo"], data["detalles"], data["precio"]))
        cur.execute("INSERT INTO movimientos (tipo, descripcion, monto) VALUES (?, ?, ?)", ("INGRESO", f"Servicio: {data['tipo']}", data['precio']))
        db_conn.commit()
        db_conn.close()
        return jsonify({"msg": "ok"})
    else:
        cur.execute("SELECT id, tipo, detalles, precio, fecha FROM lavados ORDER BY fecha ASC")
        res = [{"id":f[0], "tipo":f[1], "detalles":f[2], "precio":f[3], "fecha":f[4]} for f in cur.fetchall()]
        db_conn.close()
        return jsonify(res)

@app.route("/lavados/<int:id>", methods=["DELETE"])
def lavados_delete(id):
    db_conn = get_db()
    cur = db_conn.cursor()
    cur.execute("DELETE FROM lavados WHERE id=?", (id,))
    db_conn.commit()
    db_conn.close()
    return jsonify({"msg": "Lavado eliminado"})

@app.route("/movimientos", methods=["GET"])
def movimientos_get():
    db_conn = get_db()
    cur = db_conn.cursor()
    cur.execute("SELECT id, tipo, descripcion, monto, fecha FROM movimientos ORDER BY fecha DESC")
    res = [{"id":f[0], "tipo":f[1], "descripcion":f[2], "monto":f[3], "fecha":f[4]} for f in cur.fetchall()]
    db_conn.close()
    return jsonify(res)


# ==============================================================================
#  SECCIÓN B: WEB AGENDA & TIENDA (Lógica de app.py)
# ==============================================================================

@app.route('/')
def home():
    return redirect(url_for('store'))

@app.route('/store')
def store():
    # Renderizamos la tienda usando los datos reales
    db_conn = get_db()
    cur = db_conn.cursor()
    products = []
    try:
        cur.execute("SELECT id, nombre_producto, precio, image_url FROM productos")
        for f in cur.fetchall():
            img = f[3] if len(f) > 3 and f[3] else 'https://via.placeholder.com/300?text=Sin+Imagen'
            products.append({'id': f[0], 'name': f[1], 'price': f[2], 'image_url': img})
    except: pass
    db_conn.close()
    cart = session.get('cart', {})
    return render_template('store.html', products=products, cart_count=sum(cart.values()))

@app.route('/agenda', methods=['GET', 'POST'])
def agenda():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            service = request.form.get('service')
            date = request.form.get('date')
            
            if name and date:
                new_appt = Appointment(name=name, email=email, service=service, date=date)
                db.session.add(new_appt)
                db.session.commit()
                flash('¡Reserva enviada!', 'success')
            return redirect(url_for('agenda'))
        except:
            db.session.rollback()
            flash('Error al reservar.', 'error')
    return render_template('agenda.html')

@app.route('/admin')
def admin():
    appointments = Appointment.query.order_by(Appointment.status == 'Pendiente', Appointment.date.asc()).all()
    appointments.reverse()
    return render_template('vascon.html', appointments=appointments)

@app.route('/admin/update_status/<int:id>/<string:new_status>')
def update_status(id, new_status):
    appt = Appointment.query.get_or_404(id)
    appt.status = new_status
    db.session.commit()
    return redirect(url_for('admin'))

# Auth y Rutas Extra
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == "admin" and request.form.get('password') == "vascon123":
            session['logged_in'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('store'))

@app.route('/client_login') 
def client_login(): return render_template('client_login.html')
@app.route('/client_register') 
def client_register(): return render_template('client_register.html')

@app.route('/api/cart/add/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    cart = session.get('cart', {})
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    session['cart'] = cart
    return jsonify({'status': 'ok', 'total_count': sum(cart.values())})


# ==============================================================================
#  ARRANQUE
# ==============================================================================
if __name__ == '__main__':
    print("🚀 SISTEMA UNIFICADO VASCONCELLOS - ACTIVO")
    print(f"📂 Base de datos: {os.path.basename(DB_PATH)}")
    print("👉 Accede a: http://127.0.0.1:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')