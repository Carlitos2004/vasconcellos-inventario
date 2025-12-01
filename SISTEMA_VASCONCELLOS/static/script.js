/* ============================================================
   VASCONCELLOS OS — SISTEMA OPERATIVO DE GESTIÓN (SPA)
   Archivo: static/js/script.js
   Conexión: Backend Flask (app.py)
============================================================ */

const API_BASE = ""; // Flask sirve todo desde la misma raíz, no tocar.

// === UTILIDADES ===
const clp = new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP'
});

// Al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    cargarProductos();
    cargarMovimientos();
    setupListeners();
});

// === 1. GESTIÓN DE PRODUCTOS ===

async function cargarProductos() {
    try {
        const res = await fetch(`${API_BASE}/productos`); // Llama a la API de Flask
        if (!res.ok) throw new Error("Error de red");
        const productos = await res.json();
        
        renderizarTabla(productos);
        renderizarSelects(productos); // Llena los selectores de Ventas/Compras
    } catch (e) {
        console.error("Error cargando inventario:", e);
        Swal.fire("Error", "No se pudo conectar con el servidor", "error");
    }
}

function renderizarTabla(productos) {
    const tbody = document.getElementById("tablaProductos");
    if (!tbody) return;

    tbody.innerHTML = "";
    productos.forEach(p => {
        // Determinamos estado del stock visualmente
        let stockClass = "";
        if(p.stock <= 2) stockClass = "color: red; font-weight: bold;";
        else if(p.stock <= 5) stockClass = "color: orange;";

        tbody.innerHTML += `
            <tr>
                <td>#${p.id}</td>
                <td>
                    <div style="font-weight:bold;">${p.nombre_producto}</div>
                    <small style="color:#666;">${p.etiqueta || 'General'}</small>
                </td>
                <td style="${stockClass}">${p.stock} un.</td>
                <td>${clp.format(p.precio)}</td>
                <td>
                    <button class="btn-sm btn-secondary" onclick="prepararVenta(${p.id}, '${p.nombre_producto}', ${p.precio})">
                        ⚡ Vender
                    </button>
                </td>
            </tr>
        `;
    });
}

// === 2. BÚSQUEDA Y FILTROS ===

function buscarProducto() {
    const texto = document.getElementById("buscador").value.toLowerCase();
    const filas = document.querySelectorAll("#tablaProductos tr");

    filas.forEach(fila => {
        const contenido = fila.innerText.toLowerCase();
        fila.style.display = contenido.includes(texto) ? "" : "none";
    });
}

// === 3. SISTEMA DE VENTAS ===

// Llena los selectores del formulario de ventas
function renderizarSelects(productos) {
    const selectVenta = document.getElementById("ventaProducto");
    if (!selectVenta) return;

    selectVenta.innerHTML = '<option value="">Seleccione un producto...</option>';
    productos.forEach(p => {
        selectVenta.innerHTML += `<option value="${p.id}" data-precio="${p.precio}">${p.nombre_producto} (Stock: ${p.stock})</option>`;
    });
}

// Actualiza el total cuando cambias la cantidad o producto
function actualizarPrecioYTotal() {
    const select = document.getElementById("ventaProducto");
    const inputCant = document.getElementById("ventaCantidad");
    const inputPrecio = document.getElementById("ventaPrecio");
    const inputTotal = document.getElementById("ventaTotal");

    if (select.value) {
        const precio = parseFloat(select.options[select.selectedIndex].dataset.precio);
        const cantidad = parseInt(inputCant.value) || 1;
        
        inputPrecio.value = precio; // Visual
        inputTotal.value = clp.format(precio * cantidad); // Visual
    }
}

async function registrarVenta() {
    const id = document.getElementById("ventaProducto").value;
    const cantidad = document.getElementById("ventaCantidad").value;
    const select = document.getElementById("ventaProducto");
    
    if (!id || !cantidad) {
        Swal.fire("Atención", "Selecciona un producto y cantidad", "warning");
        return;
    }

    const precio = parseFloat(select.options[select.selectedIndex].dataset.precio);
    const total = precio * parseInt(cantidad);

    try {
        const res = await fetch(`${API_BASE}/ventas`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                producto_id: id,
                cantidad: parseInt(cantidad),
                total: total
            })
        });

        const data = await res.json();
        
        if (res.ok) {
            Swal.fire("¡Éxito!", "Venta registrada correctamente", "success");
            cargarProductos(); // Recargar stock en la tabla
            cargarMovimientos(); // Recargar historial
            document.getElementById("ventaCantidad").value = 1;
        } else {
            Swal.fire("Error", data.error || "No se pudo registrar", "error");
        }
    } catch (e) {
        console.error(e);
        Swal.fire("Error", "Fallo de conexión", "error");
    }
}

// Atajo desde la tabla de productos
window.prepararVenta = function(id, nombre, precio) {
    // Cambiamos a la pestaña ventas (simulado)
    mostrarVentas(); 
    const select = document.getElementById("ventaProducto");
    select.value = id;
    actualizarPrecioYTotal();
    Swal.fire({
        title: 'Modo Venta Rápida',
        text: `Seleccionado: ${nombre}`,
        timer: 1500,
        showConfirmButton: false,
        icon: 'info'
    });
};

// === 4. MOVIMIENTOS E HISTORIAL ===

async function cargarMovimientos() {
    const container = document.getElementById("tablaMovimientos");
    if (!container) return;

    // Nota: Necesitas crear la ruta GET /movimientos en app.py si quieres ver esto dinámico
    // Por ahora, simulamos si no hay endpoint, o intentamos conectar.
    try {
        const res = await fetch(`${API_BASE}/movimientos`);
        if(res.ok) {
            const movs = await res.json();
            let html = `<table class="custom-table" style="width:100%"><thead><tr><th>Fecha</th><th>Tipo</th><th>Descripción</th><th>Monto</th></tr></thead><tbody>`;
            
            movs.forEach(m => {
                const color = m.tipo === 'INGRESO' ? 'green' : 'red';
                html += `
                    <tr>
                        <td>${new Date(m.fecha).toLocaleDateString()}</td>
                        <td style="color:${color}; font-weight:bold;">${m.tipo}</td>
                        <td>${m.descripcion}</td>
                        <td>${clp.format(m.monto)}</td>
                    </tr>
                `;
            });
            html += "</tbody></table>";
            container.innerHTML = html;
        }
    } catch(e) {
        container.innerHTML = "<p style='text-align:center; color:#666;'>No se pudieron cargar los movimientos recientes.</p>";
    }
}

// === 5. NAVEGACIÓN (UI) ===

function setupListeners() {
    // Lógica simple para ocultar/mostrar secciones (SPA)
    window.clickInventario = () => mostrarSeccion('dashboard');
    window.mostrarVentas = () => mostrarSeccion('ventas');
    window.mostrarMovimientos = () => mostrarSeccion('movimientos');
}

function mostrarSeccion(id) {
    // Ocultar todas
    document.querySelectorAll('.content').forEach(el => el.style.display = 'none');
    // Mostrar elegida
    const target = document.getElementById(id);
    if(target) {
        target.style.display = 'block';
        target.classList.add('fade-in'); // Asegúrate de tener animación CSS
    }
}