# ==============================================================================
#  BACKEND MAESTRO - VASCONCELLOS AUTOMOTRIZ
#  Versión mejorada con sistema de clientes y portal
# ==============================================================================

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import locale

# --- CONFIGURACIÓN INICIAL ---
app = Flask(__name__)
app.secret_key = 'vasconcellos_secret_key_pro'
CORS(app)

# Idioma español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    except:
        print("⚠️ No se pudo configurar idioma local.")

# --- 1. BASE DE DATOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "inventario_automotriz.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# --- 2. MODELOS SQLALCHEMY ---
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Pendiente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# --- 3. INICIALIZACIÓN DE TABLAS ---
def init_all_tables():
    with app.app_context():
        db.create_all()

    conn = get_db()
    cur = conn.cursor()
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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER,
            total REAL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lavados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            detalles TEXT,
            precio REAL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            descripcion TEXT,
            monto REAL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_all_tables()

# --- 4. FILTROS VISUALES ---
@app.template_filter('fecha_bonita')
def fecha_bonita_filter(fecha_str):
    if not fecha_str: return {'dia': '--', 'mes': '---'}
    try:
        dt = datetime.strptime(fecha_str, '%Y-%m-%d')
        return {'dia': dt.strftime('%d'), 'mes': dt.strftime('%b').upper().replace('.', '')}
    except:
        return {'dia': '??', 'mes': '???'}

# ==============================================================================
#  SECCIÓN A: API INVENTARIO
# ==============================================================================

@app.route("/productos", methods=["GET"])
def productos_get():
    db_conn = get_db()
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT id, nombre_producto, etiqueta, stock, precio, image_url FROM productos")
    except:
        cur.execute("SELECT id, nombre_producto, etiqueta, stock, precio FROM productos")
    filas = cur.fetchall()
    res = []
    for f in filas:
        item = {"id": f[0], "nombre_producto": f[1], "etiqueta": f[2], "stock": f[3], "precio": f[4]}
        if len(f) > 5: item["image_url"] = f[5]
        res.append(item)
    db_conn.close()
    return jsonify(res)

# ==============================================================================
#  SECCIÓN B: WEB AGENDA, TIENDA Y CLIENTES
# ==============================================================================

@app.route('/')
def home():
    return redirect(url_for('store'))

@app.route('/store')
def store():
    db_conn = get_db()
    cur = db_conn.cursor()
    products = []
    try:
        cur.execute("SELECT id, nombre_producto, precio, image_url FROM productos")
        for f in cur.fetchall():
            img = f[3] if len(f) > 3 and f[3] else 'https://via.placeholder.com/300?text=Sin+Imagen'
            products.append({'id': f[0], 'name': f[1], 'price': f[2], 'image_url': img})
    except:
        pass
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

# ==============================================================================
#  SECCIÓN C: CLIENTES - REGISTRO / LOGIN / PORTAL
# ==============================================================================

@app.route('/client_register', methods=['GET', 'POST'])
def client_register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        existing = Client.query.filter_by(email=email).first()
        if existing:
            flash('Ese correo ya está registrado. Intenta iniciar sesión.', 'error')
            return redirect(url_for('client_login'))

        new_client = Client(name=name, email=email)
        new_client.set_password(password)
        db.session.add(new_client)
        db.session.commit()

        flash('Cuenta creada correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('client_login'))

    return render_template('client_register.html')





@app.route('/client_login', methods=['GET','POST'])
def client_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        client = Client.query.filter_by(email=email).first()
        if client and client.check_password(password):
            session['client_id'] = client.id
            session['client_name'] = client.name
            session['client_email'] = client.email
            flash(f'Bienvenido, {client.name}', 'success')
            return redirect(url_for('client_portal'))
        flash('Correo o contraseña incorrectos.', 'error')

    return render_template('client_login.html')



@app.route('/client_portal')
def client_portal():
    if 'client_id' not in session:
        return redirect(url_for('client_login'))

    appointments = Appointment.query.filter_by(
        email=session.get('client_email')
    ).order_by(Appointment.date.asc()).all()

    return render_template('client_portal.html', appointments=appointments)


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('store'))

# ==============================================================================
#  ARRANQUE
# ==============================================================================

if __name__ == '__main__':
    print("🚀 SISTEMA UNIFICADO VASCONCELLOS - ACTIVO")
    print(f"📂 Base de datos: {os.path.basename(DB_PATH)}")
    print("👉 Accede a: http://127.0.0.1:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')
