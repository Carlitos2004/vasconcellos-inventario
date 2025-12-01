from backend_maestro import db, app, Client

with app.app_context():
    clientes = Client.query.all()
    for c in clientes:
        print(f"ID: {c.id} | Nombre: {c.name} | Email: {c.email}")
