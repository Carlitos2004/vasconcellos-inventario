import sqlite3
import os

# --- CONFIGURACIÓN ---
DB_NAME = "inventario_automotriz.db"

# Banco de Imágenes Ampliado (Para que le achunte a todo)
IMAGENES = {
    # ACEITES Y LUBRICANTES
    "aceite": "https://images.unsplash.com/photo-1517057011470-8f36d636e6ca?auto=format&fit=crop&w=800&q=80",
    "lubricante": "https://images.unsplash.com/photo-1615900119312-2acd3a71f3aa?auto=format&fit=crop&w=800&q=80",
    "motor": "https://images.unsplash.com/photo-1517057011470-8f36d636e6ca?auto=format&fit=crop&w=800&q=80",
    "10w": "https://images.unsplash.com/photo-1517057011470-8f36d636e6ca?auto=format&fit=crop&w=800&q=80",
    "5w": "https://images.unsplash.com/photo-1517057011470-8f36d636e6ca?auto=format&fit=crop&w=800&q=80",
    "valvoline": "https://images.unsplash.com/photo-1517057011470-8f36d636e6ca?auto=format&fit=crop&w=800&q=80",
    "mobil": "https://images.unsplash.com/photo-1517057011470-8f36d636e6ca?auto=format&fit=crop&w=800&q=80",
    "shell": "https://images.unsplash.com/photo-1517057011470-8f36d636e6ca?auto=format&fit=crop&w=800&q=80",
    "total": "https://images.unsplash.com/photo-1517057011470-8f36d636e6ca?auto=format&fit=crop&w=800&q=80",
    "castrol": "https://images.unsplash.com/photo-1517057011470-8f36d636e6ca?auto=format&fit=crop&w=800&q=80",
    "liqui": "https://images.unsplash.com/photo-1615900119312-2acd3a71f3aa?auto=format&fit=crop&w=800&q=80",
    
    # LIMPIEZA EXTERIOR
    "shampoo": "https://images.unsplash.com/photo-1601362840469-51e4d8d58785?auto=format&fit=crop&w=800&q=80",
    "lavado": "https://images.unsplash.com/photo-1601362840469-51e4d8d58785?auto=format&fit=crop&w=800&q=80",
    "cera": "https://images.unsplash.com/photo-1625043484555-47841a7543c5?auto=format&fit=crop&w=800&q=80",
    "wax": "https://images.unsplash.com/photo-1625043484555-47841a7543c5?auto=format&fit=crop&w=800&q=80",
    "pulidor": "https://images.unsplash.com/photo-1625043484555-47841a7543c5?auto=format&fit=crop&w=800&q=80",
    "esponja": "https://images.unsplash.com/photo-1601362840469-51e4d8d58785?auto=format&fit=crop&w=800&q=80",
    "guante": "https://images.unsplash.com/photo-1601362840469-51e4d8d58785?auto=format&fit=crop&w=800&q=80",
    "hidrolavadora": "https://images.unsplash.com/photo-1601362840469-51e4d8d58785?auto=format&fit=crop&w=800&q=80",
    
    # ACCESORIOS DE LIMPIEZA
    "microfibra": "https://images.unsplash.com/photo-1507136566006-cfc505b114fc?auto=format&fit=crop&w=800&q=80",
    "paño": "https://images.unsplash.com/photo-1507136566006-cfc505b114fc?auto=format&fit=crop&w=800&q=80",
    "toalla": "https://images.unsplash.com/photo-1507136566006-cfc505b114fc?auto=format&fit=crop&w=800&q=80",
    "cepillo": "https://images.unsplash.com/photo-1507136566006-cfc505b114fc?auto=format&fit=crop&w=800&q=80",
    
    # INTERIOR
    "interior": "https://images.unsplash.com/photo-1589561723449-37a420b3b37e?auto=format&fit=crop&w=800&q=80",
    "tapiz": "https://images.unsplash.com/photo-1589561723449-37a420b3b37e?auto=format&fit=crop&w=800&q=80",
    "silicona": "https://images.unsplash.com/photo-1589561723449-37a420b3b37e?auto=format&fit=crop&w=800&q=80",
    "cockpit": "https://images.unsplash.com/photo-1589561723449-37a420b3b37e?auto=format&fit=crop&w=800&q=80",
    "aroma": "https://images.unsplash.com/photo-1616400619175-5beda3a17896?auto=format&fit=crop&w=800&q=80",
    "olor": "https://images.unsplash.com/photo-1616400619175-5beda3a17896?auto=format&fit=crop&w=800&q=80",
    "ambientador": "https://images.unsplash.com/photo-1616400619175-5beda3a17896?auto=format&fit=crop&w=800&q=80",
    "pino": "https://images.unsplash.com/photo-1616400619175-5beda3a17896?auto=format&fit=crop&w=800&q=80",
    
    # RUEDAS
    "renovador": "https://images.unsplash.com/photo-1578844251758-2f71da645217?auto=format&fit=crop&w=800&q=80",
    "neumatico": "https://images.unsplash.com/photo-1578844251758-2f71da645217?auto=format&fit=crop&w=800&q=80",
    "llanta": "https://images.unsplash.com/photo-1578844251758-2f71da645217?auto=format&fit=crop&w=800&q=80",
    "goma": "https://images.unsplash.com/photo-1578844251758-2f71da645217?auto=format&fit=crop&w=800&q=80",
    
    # MANTENIMIENTO
    "refrigerante": "https://images.unsplash.com/photo-1626245342324-b8c6e0904026?auto=format&fit=crop&w=800&q=80",
    "coolant": "https://images.unsplash.com/photo-1626245342324-b8c6e0904026?auto=format&fit=crop&w=800&q=80",
    "agua": "https://images.unsplash.com/photo-1626245342324-b8c6e0904026?auto=format&fit=crop&w=800&q=80",
    "destilada": "https://images.unsplash.com/photo-1626245342324-b8c6e0904026?auto=format&fit=crop&w=800&q=80",
    "aditivo": "https://images.unsplash.com/photo-1615900119312-2acd3a71f3aa?auto=format&fit=crop&w=800&q=80",
    "limpia": "https://images.unsplash.com/photo-1626245342324-b8c6e0904026?auto=format&fit=crop&w=800&q=80", # Catch-all para limpiadores
    "filtro": "https://images.unsplash.com/photo-1486262715619-01b8c2297602?auto=format&fit=crop&w=800&q=80",
    
    # REPUESTOS Y OTROS
    "bateria": "https://images.unsplash.com/photo-1624526260584-20925623705d?auto=format&fit=crop&w=800&q=80",
    "foco": "https://images.unsplash.com/photo-1490902931801-d6f80ca94fe4?auto=format&fit=crop&w=800&q=80",
    "led": "https://images.unsplash.com/photo-1490902931801-d6f80ca94fe4?auto=format&fit=crop&w=800&q=80",
    "luz": "https://images.unsplash.com/photo-1490902931801-d6f80ca94fe4?auto=format&fit=crop&w=800&q=80",
    "ampolleta": "https://images.unsplash.com/photo-1490902931801-d6f80ca94fe4?auto=format&fit=crop&w=800&q=80",
    "herramienta": "https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?auto=format&fit=crop&w=800&q=80",
    "llave": "https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?auto=format&fit=crop&w=800&q=80",
    
    # DEFAULT (El auto deportivo)
    "default": "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=800&q=80" 
}

def actualizar_imagenes():
    if not os.path.exists(DB_NAME):
        print(f"❌ Error: No encuentro {DB_NAME}")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Detectar tabla de productos
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'users' AND name NOT LIKE 'appointments'")
    tablas = cursor.fetchall()
    
    if not tablas:
        print("❌ No hay tablas de productos.")
        return
        
    # Elegir la tabla con más columnas "tipo texto" (probablemente tiene el nombre)
    tabla = tablas[0][0]
    cursor.execute(f"PRAGMA table_info(\"{tabla}\")")
    cols = cursor.fetchall() # id, name, type, notnull, dflt, pk
    
    # Buscar cuál es la columna del NOMBRE
    col_nombre = None
    col_id = 'rowid'
    
    col_nombres = [c[1] for c in cols]
    
    # Lógica para encontrar la columna que tiene el TEXTO del producto
    # Prioridad: nombre, descripcion, producto, item...
    for c in col_nombres:
        if any(x in c.lower() for x in ['nomb', 'desc', 'prod', 'item']):
            col_nombre = c
            break
            
    # Si no encuentra por nombre, usa la segunda columna (la primera suele ser ID)
    if not col_nombre and len(col_nombres) > 1:
        col_nombre = col_nombres[1]
        
    # Buscar columna ID explícito si existe
    for c in col_nombres:
        if c.lower() in ['id', 'codigo', 'sku']:
            col_id = c
            break

    print(f"--- DIAGNÓSTICO ---")
    print(f"Tabla detectada: {tabla}")
    print(f"Usando columna ID: {col_id}")
    print(f"Usando columna NOMBRE: {col_nombre}")
    print("-------------------")

    # Asegurar columna imagen
    try:
        cursor.execute(f"ALTER TABLE \"{tabla}\" ADD COLUMN image_url TEXT")
    except: pass

    # Leer productos
    sql = f"SELECT {col_id}, \"{col_nombre}\" FROM \"{tabla}\""
    productos = cursor.execute(sql).fetchall()
    
    print(f"Procesando {len(productos)} productos...")
    print("Muestra de detección:")
    
    cambios = 0
    for i, prod in enumerate(productos):
        pid = prod[0]
        nombre_raw = prod[1]
        
        if not nombre_raw: continue # Saltar vacíos
        
        nombre = str(nombre_raw).lower()
        
        # Asignación
        url_asignada = IMAGENES["default"]
        tipo_detectado = "default"
        
        for clave, url in IMAGENES.items():
            if clave == "default": continue
            # Buscar palabra completa o parcial significativa
            if clave in nombre:
                url_asignada = url
                tipo_detectado = clave
                break
        
        # Solo imprimir los primeros 5 para verificar
        if i < 5:
            print(f"  [{nombre_raw[:20]}...] -> Detectado: {tipo_detectado}")

        cursor.execute(f"UPDATE \"{tabla}\" SET image_url = ? WHERE {col_id} = ?", (url_asignada, pid))
        cambios += 1
        
    conn.commit()
    conn.close()
    print("-------------------")
    print(f"✅ ¡LISTO! Imágenes actualizadas en {cambios} productos.")
    print("👉 REINICIA 'app.py' Y RECARGA LA PÁGINA.")

if __name__ == "__main__":
    actualizar_imagenes()