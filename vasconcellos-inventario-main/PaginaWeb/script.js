/* ============================================================
   script.js — Vasconcellos Automotriz (Versión mejorada)
   CON ELIMINAR EN VENTAS / COMPRAS / LAVADOS / MOVIMIENTOS
============================================================ */

const API = "http://127.0.0.1:5000";
let productosCache = [];

/* ============================================================
   FORMATOS
============================================================ */

function formatearPrecio(n) {
  return Number(n).toLocaleString("es-CL", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  });
}

function fechaDiaHoraCorta(f) {
  const d = new Date(f);
  // Meses con primera letra mayúscula: Ene, Feb, Mar, Abr, May, Jun, Jul, Ago, Sep, Oct, Nov, Dic
  const meses = [
    "Ene",
    "Feb",
    "Mar",
    "Abr",
    "May",
    "Jun",
    "Jul",
    "Ago",
    "Sep",
    "Oct",
    "Nov",
    "Dic",
  ];
  const dia = String(d.getDate()).padStart(2, "0");
  const mes = meses[d.getMonth()];
  const hora = String(d.getHours()).padStart(2, "0");
  const min = String(d.getMinutes()).padStart(2, "0");
  return `${dia} ${mes} ${hora}:${min}`;
}

/**
 * Devuelve clave y etiqueta bonita de mes
 * Ej: { clave: "2025-11", label: "Noviembre 2025" }
 */
function etiquetaMesClave(f) {
  const d = new Date(f);
  const meses = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
  ];

  const mesNumero = d.getMonth() + 1;
  return {
    clave: `${d.getFullYear()}-${mesNumero}`,
    label: `${meses[d.getMonth()]} ${d.getFullYear()}`,
  };
}

function toggleMes(headerDiv) {
  const card = headerDiv.parentElement;
  const contenido = card.querySelector(".mes-contenido");

  if (!contenido) return;

  const activo = contenido.classList.contains("activo");
  if (activo) {
    contenido.classList.remove("activo");
    headerDiv.classList.remove("activo");
  } else {
    contenido.classList.add("activo");
    headerDiv.classList.add("activo");
  }
}

/* ============================================================
   SIDEBAR / INVENTARIO
============================================================ */

function toggleInventario() {
  const sub = document.getElementById("submenu-inventario");
  const arrow = document.getElementById("arrow-inv");

  if (sub.style.display === "block") {
    sub.style.display = "none";
    arrow.textContent = "▸";
  } else {
    sub.style.display = "block";
    arrow.textContent = "▾";
  }
}

/**
 * Al hacer clic en "Inventario" en el menú:
 * - Siempre muestra el inventario completo
 * - Abre/cierra el submenú
 */
function clickInventario() {
  mostrarInventarioCompleto();
  toggleInventario();
}

/**
 * Botón "Inventario completo 📦" del submenú:
 * - Muestra la sección dashboard
 * - Limpia el buscador
 * - Renderiza TODOS los productos
 */
function mostrarInventarioCompleto() {
  ocultarTodo();
  document.getElementById("dashboard").style.display = "block";

  const buscador = document.getElementById("buscador");
  if (buscador) buscador.value = "";

  // Mostrar todo el inventario desde la caché
  renderProductos(productosCache);
}

async function cargarCategorias() {
  const resp = await fetch(`${API}/categorias`);
  const categorias = await resp.json();

  const sub = document.getElementById("submenu-inventario");
  sub.innerHTML = "";

  // Botón Inventario completo
  const btn = document.createElement("button");
  btn.textContent = "Inventario completo 📦";
  btn.onclick = () => mostrarInventarioCompleto();
  sub.appendChild(btn);

  // Categorías
  categorias.forEach((cat) => {
    const b = document.createElement("button");
    b.textContent = cat;
    b.onclick = () => mostrarSoloCategoria(cat);
    sub.appendChild(b);
  });
}

/* ============================================================
   INVENTARIO
============================================================ */

async function mostrar() {
  const r = await fetch(`${API}/productos`);
  productosCache = await r.json();
  renderProductos(productosCache);
}

function renderProductos(lista) {
  const tb = document.getElementById("tablaProductos");

  tb.innerHTML = lista
    .map(
      (p, idx) => `
    <tr>
      <td>${idx + 1}</td>
      <td>${p.nombre_producto}</td>
      <td>${p.etiqueta || ""}</td>
      <td class="${
        p.stock <= 5
          ? "stock-bajo"
          : p.stock <= 15
          ? "stock-medio"
          : "stock-alto"
      }">${p.stock}</td>
      <td>$${formatearPrecio(p.precio)}</td>
      <td>
        <button onclick="editarProducto(${p.id})">✏️</button>
        <button onclick="eliminarProducto(${p.id})">🗑️</button>
      </td>
    </tr>
  `
    )
    .join("");
}

function buscarProducto() {
  const texto = document.getElementById("buscador").value.toLowerCase();
  const filtrado = productosCache.filter(
    (p) =>
      p.nombre_producto.toLowerCase().includes(texto) ||
      (p.etiqueta && p.etiqueta.toLowerCase().includes(texto))
  );
  renderProductos(filtrado);
}

function mostrarSoloCategoria(cat) {
  ocultarTodo();
  document.getElementById("dashboard").style.display = "block";

  // Aseguramos que el menú esté abierto y con flecha hacia abajo
  const sub = document.getElementById("submenu-inventario");
  sub.style.display = "block";
  document.getElementById("arrow-inv").textContent = "▾";

  const filtrado = productosCache.filter((p) => p.etiqueta === cat);
  renderProductos(filtrado);
}

/* ============================================================
   AGREGAR / EDITAR / ELIMINAR PRODUCTO
============================================================ */

async function abrirAgregarProducto() {
  const { value: nombre } = await Swal.fire({
    title: "Nombre del producto",
    input: "text",
    inputPlaceholder: "Ej: Aceite 10W-40",
    showCancelButton: true,
  });
  if (!nombre) return;

  const { value: etiqueta } = await Swal.fire({
    title: "Categoría / etiqueta",
    input: "text",
    inputPlaceholder: "Ej: Aceite Motor, Aditivos...",
    showCancelButton: true,
  });
  if (!etiqueta) return;

  const { value: stock } = await Swal.fire({
    title: "Stock inicial",
    input: "number",
    inputValue: 0,
    showCancelButton: true,
  });
  if (stock === null) return;

  const { value: precio } = await Swal.fire({
    title: "Precio",
    input: "number",
    inputValue: 0,
    showCancelButton: true,
  });
  if (precio === null) return;

  await fetch(`${API}/productos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nombre_producto: nombre,
      etiqueta,
      stock: Number(stock),
      precio: Number(precio),
    }),
  });

  Swal.fire("Guardado", "Producto agregado correctamente", "success");
  await mostrar();
  await cargarCategorias();
}

async function editarProducto(id) {
  const p = productosCache.find((x) => x.id === id);
  if (!p) return;

  const { value: nombre } = await Swal.fire({
    title: "Editar nombre",
    input: "text",
    inputValue: p.nombre_producto,
    showCancelButton: true,
  });
  if (!nombre) return;

  const { value: etiqueta } = await Swal.fire({
    title: "Editar categoría",
    input: "text",
    inputValue: p.etiqueta,
    showCancelButton: true,
  });
  if (!etiqueta) return;

  const { value: stock } = await Swal.fire({
    title: "Editar stock",
    input: "number",
    inputValue: p.stock,
    showCancelButton: true,
  });
  if (stock === null) return;

  const { value: precio } = await Swal.fire({
    title: "Editar precio",
    input: "number",
    inputValue: p.precio,
    showCancelButton: true,
  });
  if (precio === null) return;

  await fetch(`${API}/productos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nombre_producto: nombre,
      etiqueta,
      stock: Number(stock),
      precio: Number(precio),
    }),
  });

  Swal.fire("Correcto", "Producto actualizado", "success");
  await mostrar();
  await cargarCategorias();
}

async function eliminarProducto(id) {
  const r = await Swal.fire({
    title: "¿Eliminar producto?",
    text: "Esto no se puede deshacer",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Sí, eliminar",
  });
  if (!r.isConfirmed) return;

  await fetch(`${API}/productos/${id}`, { method: "DELETE" });
  Swal.fire("Eliminado", "Producto borrado", "success");
  await mostrar();
  await cargarCategorias();
}

/* ============================================================
   LAVADOS / SERVICIOS
============================================================ */

function mostrarLavados() {
  ocultarTodo();
  document.getElementById("lavados").style.display = "block";
  cargarLavadosHoy();
}

async function registrarLavado() {
  const tipo = document.getElementById("lavadoTipo").value;
  const detalles = document.getElementById("lavadoDetalles").value.trim();
  const precio = Number(document.getElementById("lavadoPrecio").value || 0);

  if (precio <= 0) {
    Swal.fire("Atención", "El precio debe ser mayor a 0", "warning");
    return;
  }

  await fetch(`${API}/lavados`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tipo, detalles, precio }),
  });

  Swal.fire("Guardado", "Servicio registrado correctamente", "success");

  document.getElementById("lavadoDetalles").value = "";
  document.getElementById("lavadoPrecio").value = 0;

  await cargarLavadosHoy();
  await cargarMovimientos();
}

async function cargarLavadosHoy() {
  const res = await fetch(`${API}/lavados`);
  const lavados = await res.json();

  const hoy = new Date();
  const hoyISO = hoy.toISOString().substring(0, 10);

  const lavadosDia = lavados.filter((l) => {
    const fecha = new Date(l.fecha);
    const fIso = fecha.toISOString().substring(0, 10);
    return fIso === hoyISO;
  });

  const cont = document.getElementById("lavadosHoy");
  cont.innerHTML = "";

  if (lavadosDia.length === 0) {
    cont.innerHTML = "<p>No hay lavados/servicios registrados hoy.</p>";
    return;
  }

  const totalDia = lavadosDia.reduce(
    (ac, l) => ac + Number(l.precio || 0),
    0
  );

  const card = document.createElement("div");
  card.className = "mes-card";

  const header = document.createElement("div");
  header.className = "mes-header activo";

  // NUEVO HEADER ESTILO PRO CON COLOR
  header.innerHTML = `
    <div class="mes-header-row">
      <div>
        <div class="mes-header-title">Hoy</div>
        <div class="mes-header-resumen">
          <span class="tag-lavados">Total lavados: $${formatearPrecio(totalDia)}</span>
        </div>
      </div>
      <div class="mes-header-right">
        <div class="mes-header-ver">Ver detalle</div>
        <div class="mes-arrow">▾</div>
      </div>
    </div>
  `;

  const contenido = document.createElement("div");
  contenido.className = "mes-contenido activo";

  contenido.innerHTML = lavadosDia
    .map(
      (l) => `
      <div class="venta-item lavado-pro">
        <div class="venta-info">
          <div class="venta-producto">🧽 ${l.tipo}</div>
          <div class="venta-detalle">
            Detalles: ${l.detalles || "—"} · Precio: $${formatearPrecio(l.precio)}
          </div>
          <div class="venta-fecha">${fechaDiaHoraCorta(l.fecha)}</div>
        </div>
        <button class="boton-eliminar" onclick="eliminarLavado(${l.id})">🗑</button>
      </div>
    `
    )
    .join("");

  header.onclick = () => toggleMes(header);

  card.appendChild(header);
  card.appendChild(contenido);
  cont.appendChild(card);
}


async function eliminarLavado(id) {
  const r = await Swal.fire({
    title: "¿Eliminar servicio?",
    text: "Se eliminará el registro del lavado/servicio.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Sí, eliminar",
  });
  if (!r.isConfirmed) return;

  const resp = await fetch(`${API}/lavados/${id}`, { method: "DELETE" });
  let data = {};
  try {
    data = await resp.json();
  } catch (e) {}

  if (data && data.error) {
    Swal.fire("Error", data.error, "error");
    return;
  }

  Swal.fire("Eliminado", "Servicio eliminado correctamente", "success");
  await cargarLavadosHoy();
  await cargarMovimientos();
}

/* ============================================================
   VENTAS
============================================================ */

async function mostrarVentas() {
  ocultarTodo();
  document.getElementById("ventas").style.display = "block";
  await cargarCategoriasVenta();
  await filtrarProductosVenta();
  await cargarVentas();
}

async function cargarCategoriasVenta() {
  const resp = await fetch(`${API}/categorias`);
  const categorias = await resp.json();
  const select = document.getElementById("ventaCategoria");

  select.innerHTML = "";
  categorias.forEach((cat) => {
    const opt = document.createElement("option");
    opt.value = cat;
    opt.textContent = cat;
    select.appendChild(opt);
  });
}

async function filtrarProductosVenta() {
  const categoria = document.getElementById("ventaCategoria").value;
  const lista = productosCache.filter((p) => p.etiqueta === categoria);

  const selectP = document.getElementById("ventaProducto");
  selectP.innerHTML = "";

  lista.forEach((p) => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = p.nombre_producto;
    selectP.appendChild(opt);
  });

  actualizarPrecioYTotal();
}

function actualizarPrecioYTotal() {
  const productoId = Number(document.getElementById("ventaProducto").value);
  const cantidad = Number(document.getElementById("ventaCantidad").value);

  const p = productosCache.find((x) => x.id === productoId);
  if (!p) return;

  document.getElementById("ventaPrecio").value =
    "$" + formatearPrecio(p.precio);
  document.getElementById("ventaTotal").value =
    "$" + formatearPrecio(p.precio * cantidad);
}

async function registrarVenta() {
  const producto_id = Number(document.getElementById("ventaProducto").value);
  const cantidad = Number(document.getElementById("ventaCantidad").value);

  if (cantidad <= 0) {
    Swal.fire("Error", "Cantidad debe ser mayor a 0", "error");
    return;
  }

  const resp = await fetch(`${API}/ventas`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ producto_id, cantidad }),
  });

  const data = await resp.json();
  if (data.error) {
    Swal.fire("Error", data.error, "error");
    return;
  }

  Swal.fire("Venta registrada", "", "success");
  await mostrar();
  await cargarVentas();
  await cargarMovimientos();
}

async function cargarVentas() {
  const resp = await fetch(`${API}/ventas`);
  const ventas = await resp.json();

  const cont = document.getElementById("ventasMeses");
  cont.innerHTML = "";

  const meses = {};
  ventas.forEach((v) => {
    const em = etiquetaMesClave(v.fecha);
    if (!meses[em.clave]) {
      meses[em.clave] = { label: em.label, detalle: [] };
    }
    meses[em.clave].detalle.push(v);
  });

  const claves = Object.keys(meses).sort();
  claves.forEach((k) => {
    const m = meses[k];
    const card = document.createElement("div");
    card.className = "mes-card";

    /* HEADER */
    const header = document.createElement("div");
    header.className = "mes-header";

    let totalMes = m.detalle.reduce(
      (ac, v) => ac + Number(v.total || 0),
      0
    );

    /* Header con color verde PRO */
    header.innerHTML = `
      <div class="mes-header-row">
        <div>
          <div class="mes-header-title">${m.label}</div>
          <div class="mes-header-resumen">
            <span class="tag-ventas-pro">Total ventas: $${formatearPrecio(totalMes)}</span>
          </div>
        </div>
        <div class="mes-header-right">
          <div class="mes-header-ver">Ver detalle</div>
          <div class="mes-arrow">▾</div>
        </div>
      </div>
    `;

    const contenido = document.createElement("div");
    contenido.className = "mes-contenido";

    /* LISTA DE VENTAS CON BORDE VERDE */
    contenido.innerHTML = m.detalle
      .map(
        (v) => `
        <div class="venta-item venta-pro-venta">
          <div class="venta-info">
            <div class="venta-producto">💰 ${v.nombre_producto}</div>
            <div class="venta-detalle">
              Cantidad: ${v.cantidad} · 
              Precio unitario: $${formatearPrecio(v.precio_unitario)} · 
              Total: $${formatearPrecio(v.total)}
            </div>
            <div class="venta-fecha">${fechaDiaHoraCorta(v.fecha)}</div>
          </div>
          <button class="boton-eliminar" onclick="eliminarVenta(${v.id})">🗑</button>
        </div>
      `
      )
      .join("");

    header.onclick = () => toggleMes(header);

    card.appendChild(header);
    card.appendChild(contenido);
    cont.appendChild(card);
  });
}



async function eliminarVenta(id) {
  const r = await Swal.fire({
    title: "¿Eliminar venta?",
    text: "Se devolverá el stock del producto.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Sí, eliminar",
  });
  if (!r.isConfirmed) return;

  const resp = await fetch(`${API}/ventas/${id}`, { method: "DELETE" });
  let data = {};
  try {
    data = await resp.json();
  } catch (e) {}

  if (data && data.error) {
    Swal.fire("Error", data.error, "error");
    return;
  }

  Swal.fire("Eliminado", "La venta fue eliminada", "success");
  await mostrar();
  await cargarVentas();
  await cargarMovimientos();
}

/* ============================================================
   COMPRAS
============================================================ */

async function mostrarCompras() {
  ocultarTodo();
  document.getElementById("compras").style.display = "block";
  await cargarCategoriasCompra();
  await filtrarProductosCompra();
  await cargarCompras();
}

async function cargarCategoriasCompra() {
  const resp = await fetch(`${API}/categorias`);
  const categorias = await resp.json();
  const select = document.getElementById("compraCategoria");

  select.innerHTML = "";
  categorias.forEach((cat) => {
    const opt = document.createElement("option");
    opt.value = cat;
    opt.textContent = cat;
    select.appendChild(opt);
  });
}

async function filtrarProductosCompra() {
  const categoria = document.getElementById("compraCategoria").value;
  const lista = productosCache.filter((p) => p.etiqueta === categoria);

  const selectP = document.getElementById("compraProducto");
  selectP.innerHTML = "";

  lista.forEach((p) => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = p.nombre_producto;
    selectP.appendChild(opt);
  });

  actualizarTotalCompra();
}

function actualizarTotalCompra() {
  const cantidad = Number(document.getElementById("compraCantidad").value);
  const precio = Number(document.getElementById("compraPrecio").value);
  document.getElementById("compraTotal").value =
    "$" + formatearPrecio(cantidad * precio);
}

async function registrarCompra() {
  const producto_id = Number(document.getElementById("compraProducto").value);
  const cantidad = Number(document.getElementById("compraCantidad").value);
  const precio_compra = Number(document.getElementById("compraPrecio").value);

  if (cantidad <= 0 || precio_compra <= 0) {
    Swal.fire("Error", "Valores inválidos", "error");
    return;
  }

  await fetch(`${API}/compras`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ producto_id, cantidad, precio_compra }),
  });

  Swal.fire("Compra registrada", "", "success");
  await mostrar();
  await cargarCompras();
  await cargarMovimientos();
}

async function cargarCompras() {
  const resp = await fetch(`${API}/compras`);
  const compras = await resp.json();

  const cont = document.getElementById("comprasMeses");
  cont.innerHTML = "";

  const meses = {};
  compras.forEach((c) => {
    const em = etiquetaMesClave(c.fecha);
    if (!meses[em.clave]) {
      meses[em.clave] = { label: em.label, detalle: [] };
    }
    meses[em.clave].detalle.push(c);
  });

  const claves = Object.keys(meses).sort();
  claves.forEach((k) => {
    const m = meses[k];
    const card = document.createElement("div");
    card.className = "mes-card";

    /* HEADER */
    const header = document.createElement("div");
    header.className = "mes-header";

    let totalMes = m.detalle.reduce(
      (ac, c) => ac + Number(c.total_compra || 0),
      0
    );

    /* HEADER CON COLOR PRO */
    header.innerHTML = `
      <div class="mes-header-row">
        <div>
          <div class="mes-header-title">${m.label}</div>
          <div class="mes-header-resumen">
            <span class="tag-compras-pro">Total compras: $${formatearPrecio(totalMes)}</span>
          </div>
        </div>
        <div class="mes-header-right">
          <div class="mes-header-ver">Ver detalle</div>
          <div class="mes-arrow">▾</div>
        </div>
      </div>
    `;

    const contenido = document.createElement("div");
    contenido.className = "mes-contenido";

    /* LISTA DE COMPRAS CON BORDE NARANJO */
    contenido.innerHTML = m.detalle
      .map(
        (c) => `
        <div class="venta-item compra-pro">
          <div class="venta-info">
            <div class="venta-producto">🛒 ${c.nombre_producto}</div>
            <div class="venta-detalle">
              Cantidad: ${c.cantidad} · 
              Precio compra: $${formatearPrecio(c.precio_compra)} · 
              Total: $${formatearPrecio(c.total_compra)}
            </div>
            <div class="venta-fecha">${fechaDiaHoraCorta(c.fecha)}</div>
          </div>
          <button class="boton-eliminar" onclick="eliminarCompra(${c.id})">🗑</button>
        </div>
      `
      )
      .join("");

    header.onclick = () => toggleMes(header);

    card.appendChild(header);
    card.appendChild(contenido);
    cont.appendChild(card);
  });
}



async function eliminarCompra(id) {
  const r = await Swal.fire({
    title: "¿Eliminar compra?",
    text: "Se ajustará el stock del producto.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Sí, eliminar",
  });
  if (!r.isConfirmed) return;

  const resp = await fetch(`${API}/compras/${id}`, { method: "DELETE" });
  let data = {};
  try {
    data = await resp.json();
  } catch (e) {}

  if (data && data.error) {
    Swal.fire("Error", data.error, "error");
    return;
  }

  Swal.fire("Eliminado", "La compra fue eliminada", "success");
  await mostrar();
  await cargarCompras();
  await cargarMovimientos();
}

/* ============================================================
   MOVIMIENTOS (MITAD/MITAD + BARRAS + LAVADOS)
============================================================ */

function mostrarMovimientos() {
  ocultarTodo();
  document.getElementById("movimientos").style.display = "block";
  cargarMovimientos();
}

async function cargarMovimientos() {
  const cont = document.getElementById("tablaMovimientos");
  cont.innerHTML = "Cargando movimientos...";

  const [respV, respC, respL] = await Promise.all([
    fetch(`${API}/ventas`),
    fetch(`${API}/compras`),
    fetch(`${API}/lavados`),
  ]);

  const ventas = await respV.json();
  const compras = await respC.json();
  const lavados = await respL.json();

  const meses = {};

  ventas.forEach((v) => {
    const em = etiquetaMesClave(v.fecha);
    if (!meses[em.clave]) {
      meses[em.clave] = {
        label: em.label,
        ventas: [],
        compras: [],
        lavados: [],
      };
    }
    meses[em.clave].ventas.push(v);
  });

  compras.forEach((c) => {
    const em = etiquetaMesClave(c.fecha);
    if (!meses[em.clave]) {
      meses[em.clave] = {
        label: em.label,
        ventas: [],
        compras: [],
        lavados: [],
      };
    }
    meses[em.clave].compras.push(c);
  });

  lavados.forEach((l) => {
    const em = etiquetaMesClave(l.fecha);
    if (!meses[em.clave]) {
      meses[em.clave] = {
        label: em.label,
        ventas: [],
        compras: [],
        lavados: [],
      };
    }
    meses[em.clave].lavados.push(l);
  });

  const claves = Object.keys(meses).sort();
  cont.innerHTML = "";

  if (claves.length === 0) {
    cont.innerHTML = "<p>No hay movimientos registrados.</p>";
    return;
  }

  claves.forEach((k) => {
    const m = meses[k];

    let totalVentas = m.ventas.reduce(
      (ac, v) => ac + Number(v.total || 0),
      0
    );
    let totalCompras = m.compras.reduce(
      (ac, c) => ac + Number(c.total_compra || 0),
      0
    );
    let totalLavados = m.lavados.reduce(
      (ac, l) => ac + Number(l.precio || 0),
      0
    );

    let ganancia = totalVentas + totalLavados - totalCompras;

    const card = document.createElement("div");
    card.className = "mes-card";

  
    
    const header = document.createElement("div");
    header.className = "mes-header";
    header.innerHTML = `
      <div class="mes-header-row">
        <div>
          <div class="mes-header-title">${m.label}</div>
          <div class="mes-header-resumen">
            <span class="tag-ventas">Ventas: $${formatearPrecio(
              totalVentas
            )}</span> ·
            <span class="tag-compras">Compras: $${formatearPrecio(
              totalCompras
            )}</span> ·
            Lavados: $${formatearPrecio(totalLavados)} ·
            <span class="tag-ganancia ${
              ganancia >= 0 ? "ganancia-positiva" : "ganancia-negativa"
            }">
              Ganancia: $${formatearPrecio(ganancia)}
            </span>
          </div>
        </div>
        <div class="mes-header-right">
          <div class="mes-header-ver">Ver detalle</div>
          <div class="mes-arrow">▾</div>
        </div>
      </div>
    `;

    const contenido = document.createElement("div");
    contenido.className = "mes-contenido";

    /* MITAD / MITAD — VENTAS IZQUIERDA / COMPRAS DERECHA */
    const columnas = document.createElement("div");
    columnas.className = "mov-columns";

    /* Ventas */
    const colV = document.createElement("div");
    colV.className = "mov-col ventas";
    colV.innerHTML = `<div class="mov-ventas-title">💰 Ventas</div>`;

    m.ventas.forEach((v) => {
      colV.innerHTML += `
        <div class="venta-item">
          <div class="venta-info">
            <div class="venta-producto">${v.nombre_producto}</div>
            <div class="venta-detalle">
              Cant: ${v.cantidad} · Precio: $${formatearPrecio(
        v.precio_unitario
      )} · Total: $${formatearPrecio(v.total)}
            </div>
            <div class="venta-fecha">${fechaDiaHoraCorta(v.fecha)}</div>
          </div>
          <button class="boton-eliminar" onclick="eliminarVenta(${
            v.id
          })">🗑</button>
        </div>
      `;
    });

    /* Compras */
    const colC = document.createElement("div");
    colC.className = "mov-col compras";
    colC.innerHTML = `<div class="mov-compras-title">🛒 Compras</div>`;

    m.compras.forEach((c) => {
      colC.innerHTML += `
        <div class="venta-item">
          <div class="venta-info">
            <div class="venta-producto">${c.nombre_producto}</div>
            <div class="venta-detalle">
              Cant: ${c.cantidad} · Precio compra: $${formatearPrecio(
        c.precio_compra
      )} · Total: $${formatearPrecio(c.total_compra)}
            </div>
            <div class="venta-fecha">${fechaDiaHoraCorta(c.fecha)}</div>
          </div>
          <button class="boton-eliminar" onclick="eliminarCompra(${
            c.id
          })">🗑</button>
        </div>
      `;
    });

    columnas.appendChild(colV);
    columnas.appendChild(colC);
    contenido.appendChild(columnas);

    /* LAVADOS — ABAJO SEPARADO */
    if (m.lavados.length > 0) {
      contenido.innerHTML += `<h4>🧽 Lavados / Servicios</h4>`;
      m.lavados.forEach((l) => {
        contenido.innerHTML += `
          <div class="venta-item lavado-pro">
            <div class="venta-info">
              <div class="venta-producto">${l.tipo}</div>
              <div class="venta-detalle">
                Detalle: ${l.detalles || "—"} · Precio: $${formatearPrecio(
          l.precio
        )}
              </div>
              <div class="venta-fecha">${fechaDiaHoraCorta(l.fecha)}</div>
            </div>
            <button class="boton-eliminar" onclick="eliminarLavado(${
              l.id
            })">🗑</button>
          </div>
        `;
      });
    }

    header.onclick = () => toggleMes(header);

    card.appendChild(header);
    card.appendChild(contenido);
    cont.appendChild(card);
  });
}

/* ============================================================
   NAVEGACIÓN / AJUSTES
============================================================ */

function ocultarTodo() {
  document.querySelectorAll(".content").forEach((sec) => {
    sec.style.display = "none";
  });
}

function mostrarDashboard() {
  ocultarTodo();
  document.getElementById("dashboard").style.display = "block";
}

function mostrarAjustes() {
  ocultarTodo();
  document.getElementById("ajustes").style.display = "block";

  const temaGuardado = localStorage.getItem("temaVasconcellos") || "azul";
  document.getElementById("temaSelect").value = temaGuardado;
  aplicarTema(temaGuardado);
}

function aplicarTema(tema) {
  document.body.classList.remove(
    "tema-azul",
    "tema-verde",
    "tema-rojo",
    "tema-morado"
  );
  document.body.classList.add("tema-" + tema);
}

function cambiarTema() {
  const tema = document.getElementById("temaSelect").value;
  aplicarTema(tema);
  localStorage.setItem("temaVasconcellos", tema);
}

function restaurarTema() {
  aplicarTema("azul");
  document.getElementById("temaSelect").value = "azul";
  localStorage.setItem("temaVasconcellos", "azul");
}

/* ============================================================
   INICIO
============================================================ */

document.addEventListener("DOMContentLoaded", async () => {
  const temaGuardado = localStorage.getItem("temaVasconcellos") || "azul";
  aplicarTema(temaGuardado);

  await mostrar();
  await cargarCategorias();
  mostrarDashboard();
});