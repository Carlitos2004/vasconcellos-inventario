-- PARTE 1: Borrar tablas si existen
DROP TABLE IF EXISTS movimientos;
DROP TABLE IF EXISTS compras;
DROP TABLE IF EXISTS ventas;
DROP TABLE IF EXISTS lavados;
DROP TABLE IF EXISTS productos;

-- PARTE 2: Crear tablas en SQLite

CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre_producto TEXT NOT NULL,
    etiqueta TEXT,
    precio REAL,
    stock INTEGER
);

CREATE TABLE compras (
    id INTEGER PRIMARY KEY,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_compra REAL,
    total_compra REAL,
    fecha TEXT,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE ventas (
    id INTEGER PRIMARY KEY,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    total REAL NOT NULL,
    fecha TEXT,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE movimientos (
    id INTEGER PRIMARY KEY,
    producto_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha TEXT,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE lavados (
    id INTEGER PRIMARY KEY,
    tipo TEXT NOT NULL,
    precio REAL NOT NULL,
    fecha TEXT NOT NULL,
    detalles TEXT
);

-- PARTE 3: Insertar productos (sin duplicados)
INSERT INTO productos (id, nombre_producto, etiqueta, precio, stock) VALUES
    (1, 'HYUNDAI Teer G700 SP 10W-40', 'Aceite Motor', 2000.0, 9),
    (2, 'HYUNDAI Teer D700 C2/C3 5W-30', 'Aceite Motor', 0.0, 0),
    (3, 'LUBRAX Tecno Si 10W-40', 'Aceite Motor', 0.0, 0),
    (4, 'LUBRAX Tecno 15W-40', 'Aceite Motor', 0.0, 0),
    (5, 'LUBRAX Supera 15W-40', 'Aceite Motor', 0.0, 0),
    (6, 'LUBRAX Extreme Conditions 5W-40', 'Aceite Motor', 0.0, 0),
    (7, 'LUBRAX Top Turbo 15W-40', 'Aceite Motor', 0.0, 0),
    (8, 'QUARTZ Ineo MCS 5W-30', 'Aceite Motor', 0.0, 0),
    (9, 'Mobil Super 3000 X1 5W-40', 'Aceite Motor', 0.0, 0),
    (10, 'Mobil Super 2000 10W-40', 'Aceite Motor', 0.0, 0),
    (11, 'Coolant 715 Anticongelante', 'Líquidos / Refrigerantes / Líquido de frenos', 0.0, 0),
    (12, 'Coolant 715 Anticongelante 1L', 'Líquidos / Refrigerantes / Líquido de frenos', 0.0, 0),
    (13, 'Coolant 715 Anticongelante 5L', 'Líquidos / Refrigerantes / Líquido de frenos', 0.0, 0),
    (14, 'Kelvinator Refrigerante', 'Líquidos / Refrigerantes / Líquido de frenos', 0.0, 0),
    (15, 'Refrigerante 1L', 'Líquidos / Refrigerantes / Líquido de frenos', 0.0, 0),
    (16, 'Refrigerante 5L', 'Líquidos / Refrigerantes / Líquido de frenos', 0.0, 0),
    (17, 'DOT 3 Líquido de frenos', 'Líquidos / Refrigerantes / Líquido de frenos', 0.0, 0),
    (18, 'DOT 4 Líquido de frenos', 'Líquidos / Refrigerantes / Líquido de frenos', 0.0, 0),
    (19, 'Líquido de frenos genérico', 'Líquidos / Refrigerantes / Líquido de frenos', 0.0, 0),
    (20, 'SHAMPOO Meguiars', 'Limpieza Exterior', 0.0, 0),
    (21, 'Neutralizador de olores interior', 'Limpieza Interior', 0.0, 0),
    (22, 'Limpia tapiz spray', 'Limpieza Interior', 0.0, 0),
    (23, 'Limpia cuero', 'Limpieza Interior', 0.0, 0),
    (24, 'Desengrasante multiuso', 'Limpieza Interior', 0.0, 0),
    (25, 'Removedor de manchas textiles', 'Limpieza Interior', 0.0, 0),
    (26, 'Silicona interior mate', 'Limpieza Interior', 0.0, 0),
    (27, 'Silicona interior brillante', 'Limpieza Interior', 0.0, 0),
    (28, 'Limpia vidrios', 'Limpieza Interior', 0.0, 0),
    (29, 'Limpia vidrios exterior', 'Limpieza Exterior', 0.0, 0),
    (30, 'Descontaminante de llantas', 'Limpieza Exterior', 0.0, 0),
    (31, 'Desengrasante de motor', 'Motor / Desengrasantes', 0.0, 0),
    (32, 'Espuma activa para carrocería', 'Limpieza Exterior', 0.0, 0),
    (33, 'Espuma activa para llantas', 'Limpieza Exterior', 0.0, 0),
    (34, 'Descontaminante férrico', 'Limpieza Exterior', 0.0, 0),
    (35, 'Cera líquida rápida', 'Pintura / Ceras', 0.0, 0),
    (36, 'Sellador sintético', 'Pintura / Ceras', 0.0, 0),
    (37, 'Pasta de pulido corte 1', 'Pintura / Ceras', 0.0, 0),
    (38, 'Pasta de pulido corte 2', 'Pintura / Ceras', 0.0, 0),
    (39, 'Pasta de terminación', 'Pintura / Ceras', 0.0, 0),
    (40, 'Pad de lana corte pesado', 'Accesorio', 0.0, 0),
    (41, 'Pad de esponja corte medio', 'Accesorio', 0.0, 0),
    (42, 'Pad de esponja terminación', 'Accesorio', 0.0, 0),
    (43, 'Microfibra estándar', 'Accesorio', 0.0, 0),
    (44, 'Microfibra premium', 'Accesorio', 0.0, 0),
    (45, 'Toalla de secado grande', 'Accesorio', 0.0, 0),
    (46, 'Toalla waffle', 'Accesorio', 0.0, 0),
    (47, 'Cepillo para llantas', 'Accesorio', 0.0, 0),
    (48, 'Cepillo para tapiz', 'Accesorio', 0.0, 0),
    (49, 'Guante de lavado microfibra', 'Accesorio', 0.0, 0),
    (50, 'Guante de lana sintética', 'Accesorio', 0.0, 0),
    (51, 'Aplicador de espuma para cera', 'Accesorio', 0.0, 0),
    (52, 'Aplicador de microfibra', 'Accesorio', 0.0, 0),
    (53, 'Brocha detailing pequeña', 'Accesorio', 0.0, 0),
    (54, 'Brocha detailing grande', 'Accesorio', 0.0, 0),
    (55, 'Aspiradora industrial', 'Accesorio', 0.0, 0),
    (56, 'Pulidora roto-orbital', 'Accesorio', 0.0, 0),
    (57, 'Pulidora rotativa', 'Accesorio', 0.0, 0),
    (58, 'Extensión eléctrica', 'Accesorio', 0.0, 0),
    (59, 'Cinta de enmascarar 3M', 'Accesorio', 0.0, 0),
    (60, 'Pistola de aire comprimido', 'Accesorio', 0.0, 0),
    (61, 'Atomizador plástico 500 ml', 'Accesorio', 0.0, 0),
    (62, 'Atomizador plástico 1L', 'Accesorio', 0.0, 0),
    (63, 'Botella dispensadora 1L', 'Accesorio', 0.0, 0),
    (64, 'Embudo plástico', 'Accesorio', 0.0, 0),
    (65, 'Balde de lavado', 'Accesorio', 0.0, 0),
    (66, 'Balde con separador de suciedad', 'Accesorio', 0.0, 0),
    (67, 'Ambientador colgante', 'Accesorio', 0.0, 0),
    (68, 'Ambientador en spray', 'Accesorio', 0.0, 0),
    (69, 'Gata hidráulica Universal', 'Accesorio', 0.0, 0),
    (70, 'Pinturas colores', 'Pintura', 0.0, 0)
;

-- PARTE 4: Insertar compras
INSERT INTO compras (id, producto_id, cantidad, precio_compra, total_compra, fecha) VALUES
    (52, 1, 21, 400.0, 8400.0, '2025-11-28 01:43:49')
;

-- PARTE 5: Insertar ventas
INSERT INTO ventas (id, producto_id, cantidad, precio_unitario, total, fecha) VALUES
    (31, 1, 12, 2000.0, 24000.0, '2025-11-28 01:44:02')
;

-- PARTE 6: Insertar movimientos
INSERT INTO movimientos (id, producto_id, tipo, cantidad, fecha) VALUES
    (48, 1, 'COMPRA', 5, '2025-11-14 12:09:08'),
    (49, 1, 'VENTA', 2, '2025-11-14 12:09:49')
;

-- PARTE 7: Insertar lavados
INSERT INTO lavados (id, tipo, precio, fecha, detalles) VALUES
    (12, 'lavado full', 434000, '2025-11-28 01:44:24', 'don juan')
;
