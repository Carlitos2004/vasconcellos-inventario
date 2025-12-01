from backend_maestro import db, app, Client

with app.app_context():
    db.create_all()
    print("✅ Tabla 'client' verificada o creada correctamente.")
