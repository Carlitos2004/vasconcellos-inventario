document.addEventListener('DOMContentLoaded', () => {
  const USE_LOCAL_STORAGE = true;
  const PAGE_SIZE = 8;

  // === ANIMACIÓN SCROLL REVEAL ===
  const setupScrollReveal = () => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, { threshold: 0.1 });

    document.querySelectorAll('.product-card, .service-item, .promo-card').forEach((card, index) => {
        card.classList.add('reveal-item');
        card.style.transitionDelay = `${(index % 4) * 100}ms`;
        observer.observe(card);
    });
  };

  const ui = {
    cartBtns: document.querySelectorAll('#header-cart-button, .sport-cart-btn'),
    sidebar: document.getElementById('cart-sidebar'),
    backdrop: document.getElementById('cart-backdrop'),
    closeBtn: document.getElementById('close-cart-btn'),
    itemsContainer: document.getElementById('cart-items-container'),
    totalEl: document.getElementById('cart-total-price'),
    checkoutBtn: document.getElementById('checkout-btn'),
    badge: document.getElementById('header-cart-badge'),
    toast: document.getElementById('toast-container'),
    grid: document.getElementById('product-grid'),
    catalogoSection: document.getElementById('catalogo'),
    skeleton: document.getElementById('skeleton-grid'),
    search: document.getElementById('search-input'),
    sort: document.getElementById('sort-select'),
    prev: document.getElementById('page-prev'),
    next: document.getElementById('page-next'),
    pageInfo: document.getElementById('page-info')
  };

  const state = { products: [], filtered: [], page: 1, cart: {} };

  const toast = (msg) => {
    if (!ui.toast) return;
    const el = document.createElement('div');
    el.className = 'toast';
    el.innerHTML = `<i class="fas fa-check"></i> ${msg}`;
    ui.toast.appendChild(el);
    setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 300); }, 3000);
  };

  const initCart = () => {
    if (USE_LOCAL_STORAGE) {
      const saved = localStorage.getItem('vascon_cart_v5');
      if (saved) state.cart = JSON.parse(saved);
      renderCart();
    }
  };
  const saveCart = () => {
    if (USE_LOCAL_STORAGE) localStorage.setItem('vascon_cart_v5', JSON.stringify(state.cart));
    renderCart();
  };
  const updateCart = (id, delta) => {
    if (!state.cart[id]) return;
    state.cart[id].quantity += delta;
    if (state.cart[id].quantity <= 0) delete state.cart[id];
    saveCart();
  };
  const addToCart = (product) => {
    if (state.cart[product.id]) {
      state.cart[product.id].quantity++;
    } else {
      state.cart[product.id] = { ...product, quantity: 1 };
    }
    saveCart();
    toast(`Añadido: ${product.name}`);
    if(ui.badge) {
       ui.badge.style.transform = 'scale(1.5)';
       setTimeout(() => ui.badge.style.transform = 'scale(1)', 200);
    }
  };
  const renderCart = () => {
    const items = Object.values(state.cart);
    const total = items.reduce((sum, i) => sum + (i.price * i.quantity), 0);
    const count = items.reduce((sum, i) => sum + i.quantity, 0);

    if (ui.badge) {
      ui.badge.textContent = count;
      ui.badge.style.display = count > 0 ? 'flex' : 'none';
    }

    if (ui.itemsContainer) {
      if (items.length === 0) {
        ui.itemsContainer.innerHTML = `<div style="text-align:center; padding:40px; color:#666;"><i class="fas fa-shopping-cart" style="font-size:2rem; margin-bottom:10px;"></i><p>Tu carrito está vacío</p></div>`;
        if (ui.checkoutBtn) ui.checkoutBtn.disabled = true;
      } else {
        if (ui.checkoutBtn) ui.checkoutBtn.disabled = false;
        ui.itemsContainer.innerHTML = items.map(item => `
          <div class="cart-item-clean">
            <img src="${item.image_url}" alt="${item.name}">
            <div class="cart-item-info">
              <div style="font-weight:700; color:#fff;">${item.name}</div>
              <div style="color:#888;">$${item.price.toLocaleString('es-CL')}</div>
              <div style="display:flex; align-items:center; gap:10px; margin-top:5px;">
                <button onclick="window.cartAction('${item.id}', -1)" style="background:#333; color:#fff; border:none; width:24px; border-radius:4px; cursor:pointer;">-</button>
                <span>${item.quantity}</span>
                <button onclick="window.cartAction('${item.id}', 1)" style="background:#333; color:#fff; border:none; width:24px; border-radius:4px; cursor:pointer;">+</button>
              </div>
            </div>
            <button onclick="window.cartRemove('${item.id}')" style="background:none; border:none; color:#666; cursor:pointer;">&times;</button>
          </div>
        `).join('');
      }
    }
    if (ui.totalEl) ui.totalEl.textContent = `$${total.toLocaleString('es-CL')}`;
  };
  window.cartAction = (id, delta) => updateCart(id, delta);
  window.cartRemove = (id) => { delete state.cart[id]; saveCart(); };

  const initStore = () => {
    if (!ui.grid) return;
    state.products = Array.from(ui.grid.querySelectorAll('.product-card'));
    if (ui.skeleton) ui.skeleton.style.display = 'none';
    ui.grid.hidden = false;
    filter();
  };

  const filter = () => {
    const q = ui.search ? ui.search.value.toLowerCase() : '';
    const sort = ui.sort ? ui.sort.value : 'name-asc';

    state.filtered = state.products.filter(el => el.dataset.name.toLowerCase().includes(q));

    state.filtered.sort((a, b) => {
      const pa = parseFloat(a.dataset.price), pb = parseFloat(b.dataset.price);
      const na = a.dataset.name, nb = b.dataset.name;
      if (sort === 'price-asc') return pa - pb;
      if (sort === 'price-desc') return pb - pa;
      if (sort === 'name-desc') return nb.localeCompare(na);
      return na.localeCompare(nb);
    });

    state.page = 1;
    renderPage(false);
  };

  const renderPage = (doScroll = false) => {
    ui.grid.innerHTML = '';
    const total = Math.ceil(state.filtered.length / PAGE_SIZE);
    const start = (state.page - 1) * PAGE_SIZE;
    const show = state.filtered.slice(start, start + PAGE_SIZE);

    if (show.length === 0) ui.grid.innerHTML = '<p style="grid-column:1/-1; text-align:center;">Sin resultados.</p>';
    else show.forEach(el => ui.grid.appendChild(el));

    if (ui.pageInfo) ui.pageInfo.textContent = `PÁGINA ${state.page} / ${total || 1}`;
    if (ui.prev) ui.prev.disabled = state.page <= 1;
    if (ui.next) ui.next.disabled = state.page >= total;
    
    // === SCROLL ELIMINADO ===
    // (El bloque window.scrollTo ha sido removido para evitar el salto)
    
    setupScrollReveal();
  };

  ui.cartBtns.forEach(b => b.addEventListener('click', () => {
    ui.sidebar.classList.add('open');
    if (ui.backdrop) ui.backdrop.classList.add('open');
  }));

  const closeCart = () => {
    ui.sidebar.classList.remove('open');
    if (ui.backdrop) ui.backdrop.classList.remove('open');
  };
  if (ui.closeBtn) ui.closeBtn.addEventListener('click', closeCart);
  if (ui.backdrop) ui.backdrop.addEventListener('click', closeCart);

  document.addEventListener('click', e => {
    const btn = e.target.closest('.add-to-cart-btn');
    if (!btn) return;
    const card = btn.closest('.product-card');
    addToCart({
      id: btn.dataset.id,
      name: card.dataset.name,
      price: card.dataset.price,
      image_url: card.querySelector('img').src
    });
  });

  if (ui.search) ui.search.addEventListener('input', filter);
  if (ui.sort) ui.sort.addEventListener('change', filter);
  
  if (ui.prev) ui.prev.addEventListener('click', () => { 
      if (state.page > 1) { state.page--; renderPage(false); }
  });
  if (ui.next) ui.next.addEventListener('click', () => { 
      if (state.page < Math.ceil(state.filtered.length / PAGE_SIZE)) { state.page++; renderPage(false); }
  });

  if (ui.checkoutBtn) ui.checkoutBtn.addEventListener('click', () => {
    const items = Object.values(state.cart);
    let msg = "Hola, cotización:\n";
    items.forEach(i => msg += `- ${i.quantity}x ${i.name}\n`);
    msg += `\nTotal: ${ui.totalEl.textContent}`;
    window.open(`https://wa.me/56912345678?text=${encodeURIComponent(msg)}`, '_blank');
  });

  const backToTopBtn = document.getElementById('back-to-top');
  if (backToTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 500) backToTopBtn.classList.add('show');
      else backToTopBtn.classList.remove('show');
    });
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  const header = document.querySelector('.header');
  if(header) {
      window.addEventListener('scroll', () => {
        if (window.scrollY > 50) header.classList.add('scrolled');
        else header.classList.remove('scrolled');
      });
  }

  initCart();
  initStore();
  window.setupScrollReveal();
});