// frontend/app.js
// --- 1. CONFIGURACIÓN E INICIALIZACIÓN ---

// Firebase Configuración
const firebaseConfig = {
  apiKey: "AIzaSyCnRsFfXs1Zk3oP6iLCBCzjC_oNb1gS30U",
  authDomain: "taximetro-d36bd.firebaseapp.com",
  projectId: "taximetro-d36bd",
  storageBucket: "taximetro-d36bd.firebasestorage.app",
  messagingSenderId: "42572035384",
  appId: "1:42572035384:web:f0f69f4ca2065a043cfdcd",
  measurementId: "G-H81L9LP2EL"
};

const API_URL = "http://127.0.0.1:8000/api/v1/taxi";

// Inicializar
if (!firebase.apps.length) firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

let state = {
    user: null,
    pollingTimer: null,
    enCarrera: false
};

// --- ELEMENTOS DOM ---
const dom = {
    views: { login: document.getElementById('view-login'), dashboard: document.getElementById('view-dashboard') },
    user: { name: document.getElementById('userName'), email: document.getElementById('userEmail') },
    kpi: { ganancias: document.getElementById('kpiGanancias'), carreras: document.getElementById('kpiCarreras') },
    display: {
        precio: document.getElementById('displayPrecio'),
        tiempo: document.getElementById('displayTiempo'),
        badge: document.getElementById('badgeEstado')
    },
    btns: {
        login: document.getElementById('btnLogin'),
        logout: document.getElementById('btnLogout'),
        start: document.getElementById('btnStart'),
        toggle: document.getElementById('btnToggle'),
        stop: document.getElementById('btnStop'),
        configSave: document.getElementById('btnSaveConfig'),
        openConfig: document.getElementById('btnOpenConfig')
    },
    inputs: { parado: document.getElementById('inputTarifaParado'), mov: document.getElementById('inputTarifaMov') },
    modals: {
        config: new bootstrap.Modal(document.getElementById('modalConfig')),
        history: new bootstrap.Modal(document.getElementById('modalHistory'))
    }
};

// --- AUTH ---
auth.onAuthStateChanged(user => {
    if (user) {
        state.user = user;
        
        dom.user.name.textContent = user.displayName || "Conductor";
        dom.user.email.textContent = user.email;
        
        const avatarContainer = document.querySelector('.avatar-circle');
        if (user.photoURL) {
            avatarContainer.innerHTML = `<img src="${user.photoURL}" alt="User">`;
        } else {
            avatarContainer.innerHTML = `<i class="fas fa-user"></i>`;
        }

        cambiarVista('dashboard');
        iniciarSistema();
    } else {
        state.user = null;
        detenerSistema();
        cambiarVista('login');
    }
});

dom.btns.login.addEventListener('click', async () => {
    const provider = new firebase.auth.GoogleAuthProvider();
    provider.setCustomParameters({
        prompt: 'select_account'
    });

    try { 
        await auth.signInWithPopup(provider); 
    } 
    catch (e) { 
        console.error("Login Error:", e);
        Swal.fire({
            title: 'Error de Acceso',
            text: e.message,
            icon: 'error',
            confirmButtonColor: '#ef4444'
        }); 
    }
});

dom.btns.logout.addEventListener('click', () => {
    if (state.enCarrera) return Swal.fire('Error', 'Termina la carrera antes de salir', 'warning');
    auth.signOut();
});

// --- API WRAPPER ---
async function api(endpoint, method = 'GET', body = null) {
    if (!state.user) return null;
    const token = await state.user.getIdToken();
    const opts = { method, headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' } };
    if (body) opts.body = JSON.stringify(body);
    
    const res = await fetch(`${API_URL}${endpoint}`, opts);
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Error Servidor');
    }
    return await res.json();
}

// --- LÓGICA SISTEMA ---
function iniciarSistema() {
    actualizarTodo();
    if (state.pollingTimer) clearInterval(state.pollingTimer);
    state.pollingTimer = setInterval(actualizarStatus, 1000);
}

function detenerSistema() {
    if (state.pollingTimer) clearInterval(state.pollingTimer);
}

async function actualizarTodo() {
    await actualizarStatus();
    await cargarKPIs();
}

async function actualizarStatus() {
    try {
        const data = await api('/status');
        
        if (data.estado === 'LIBRE') {
            dom.display.precio.textContent = `0.00 ${data.moneda}`;
            dom.display.tiempo.textContent = `00:00`;
        } else {
            dom.display.precio.textContent = `${data.importe_actual.toFixed(2)} ${data.moneda}`;
            const m = Math.floor(data.tiempo_transcurrido / 60).toString().padStart(2, '0');
            const s = (data.tiempo_transcurrido % 60).toString().padStart(2, '0');
            dom.display.tiempo.textContent = `${m}:${s}`;
        }

        actualizarUIEstado(data.estado);
        state.enCarrera = (data.estado !== 'LIBRE');

    } catch (e) { console.error(e); }
}

function actualizarUIEstado(estado) {
    const badge = dom.display.badge;
    const btns = dom.btns;

    // Reset Clases
    badge.className = 'badge-custom';
    btns.toggle.className = 'btn btn-action';

    if (estado === 'LIBRE') {
        badge.classList.add('badge-libre');
        badge.textContent = 'LIBRE';
        
        btns.start.classList.remove('d-none');
        btns.toggle.classList.add('d-none');
        btns.stop.classList.add('d-none');
        
        dom.btns.openConfig.disabled = false;

    } else {
        // En carrera
        btns.start.classList.add('d-none');
        btns.toggle.classList.remove('d-none');
        btns.stop.classList.remove('d-none');
        dom.btns.openConfig.disabled = true;

        if (estado === 'MOVIMIENTO') {
            badge.classList.add('badge-mov');
            badge.innerHTML = '<i class="fas fa-bolt me-1"></i> EN MOVIMIENTO';
            
            // Botón Toggle: Si se mueve, opción es DETENER
            btns.toggle.innerHTML = '<i class="fas fa-hand-paper me-2"></i> DETENERSE';
            btns.toggle.classList.add('btn-parar'); // Amarillo/Naranja

        } else { // PARADO
            badge.classList.add('badge-parado');
            badge.innerHTML = '<i class="fas fa-pause me-1"></i> PARADO';
            
            // Botón Toggle: Si está parado, opción es MARCHA
            btns.toggle.innerHTML = '<i class="fas fa-tachometer-alt me-2"></i> MARCHA';
            btns.toggle.classList.add('btn-marcha'); // Verde
        }
    }
}

async function cargarKPIs() {
    try {
        const kpis = await api('/dashboard');
        dom.kpi.ganancias.textContent = `${kpis.total_ganado.toFixed(2)} €`;
        dom.kpi.carreras.textContent = kpis.total_carreras;
    } catch (e) {}
}

// --- ACCIONES ---

dom.btns.start.addEventListener('click', async () => {
    try { await api('/start', 'POST', {}); actualizarTodo(); } catch(e){}
});

dom.btns.toggle.addEventListener('click', async () => {
    try { await api('/toggle', 'POST'); actualizarStatus(); } catch(e){}
});

// --- FINALIZAR CARRERA (Ticket Detallado) ---
dom.btns.stop.addEventListener('click', async () => {
    const confirm = await Swal.fire({
        title: '¿Finalizar Viaje?',
        text: 'Se detendrá el contador y se generará el cobro.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#3f3f46',
        confirmButtonText: 'Sí, Finalizar',
        background: '#18181b', color: '#fff'
    });

    if (confirm.isConfirmed) {
        try {
            const ticket = await api('/stop', 'POST');
            
            state.enCarrera = false;
            dom.display.precio.textContent = `0.00 €`;
            dom.display.tiempo.textContent = `00:00`;
            actualizarUIEstado('LIBRE'); 
            
            cargarKPIs();

            const tMov = ticket.tarifa_movimiento_aplicada || 0;
            const tPar = ticket.tarifa_parado_aplicada || 0;

            const ticketHTML = `
                <div class="text-start p-3" style="font-family: 'Inter', sans-serif; background: #27272a; border-radius: 8px; color: #e4e4e7;">
                    
                    <!-- ENCABEZADO -->
                    <div class="d-flex justify-content-between border-bottom border-secondary mb-3 pb-2">
                        <span class="text-secondary text-uppercase small">Concepto</span>
                        <span class="text-secondary text-uppercase small">Subtotal</span>
                    </div>

                    <!-- FILA 1: MOVIMIENTO -->
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <span><i class="fas fa-bolt text-success me-2"></i>En Marcha</span>
                            <span class="fw-bold text-white">${ticket.coste_movimiento.toFixed(2)} €</span>
                        </div>
                        <div class="small text-secondary ps-4">
                            ${ticket.tiempo_movimiento} seg <span class="mx-1">x</span> ${tMov.toFixed(2)} €/s
                        </div>
                    </div>

                    <!-- FILA 2: PARADO -->
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <span><i class="fas fa-hand-paper text-warning me-2"></i>En Espera</span>
                            <span class="fw-bold text-white">${ticket.coste_parado.toFixed(2)} €</span>
                        </div>
                        <div class="small text-secondary ps-4">
                            ${ticket.tiempo_parado} seg <span class="mx-1">x</span> ${tPar.toFixed(2)} €/s
                        </div>
                    </div>

                    <!-- TOTAL -->
                    <div class="border-top border-secondary pt-3 mt-2 d-flex justify-content-between align-items-center">
                        <span class="fs-5">DURACIÓN TOTAL: ${ticket.total_tiempo}s</span>
                        <span class="fs-1 fw-bold text-success">${ticket.total_coste.toFixed(2)} €</span>
                    </div>
                </div>
            `;

            Swal.fire({
                title: '🧾 TICKET DE VIAJE',
                html: ticketHTML,
                icon: 'success',
                background: '#18181b', color: '#fff',
                confirmButtonColor: '#10b981',
                confirmButtonText: 'Aceptar y Cerrar',
                width: '500px' 
            });

        } catch (e) { Swal.fire('Error', e.message, 'error'); }
    }
});

// --- HISTORIAL DETALLADO ---
document.getElementById('btnOpenHistory').addEventListener('click', async () => {
    const tbody = document.getElementById('tableHistoryBody');
    tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4">Cargando datos...</td></tr>';
    
    try {
        const history = await api('/history');
        tbody.innerHTML = '';

        if (!history || history.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-muted">No hay viajes registrados</td></tr>';
            return;
        }

        history.forEach(h => {
            // Formateo de Fecha
            let dateStr = "N/A";
            try {
                const d = new Date(h.timestamp);
                dateStr = d.toLocaleString('es-ES', { 
                    day: '2-digit', month: '2-digit', hour: '2-digit', minute:'2-digit' 
                });
            } catch (err) { console.error(err); }

            // Tarifas (Fallback a '?' si son registros viejos sin tarifa guardada)
            const tMov = h.tarifa_movimiento_aplicada ? h.tarifa_movimiento_aplicada.toFixed(2) : '?';
            const tPar = h.tarifa_parado_aplicada ? h.tarifa_parado_aplicada.toFixed(2) : '?';

            const row = `
                <tr>
                    <td class="ps-4">
                        <div class="fw-bold text-white">${dateStr}</div>
                    </td>
                    <td class="text-secondary align-middle">${h.total_tiempo}s</td>
                    <td class="align-middle">
                        <!-- Desglose de Tiempos -->
                        <div class="text-white small mb-1">
                            <span class="me-2"><i class="fas fa-bolt text-success"></i> ${h.tiempo_movimiento}s</span>
                            <span><i class="fas fa-hand-paper text-warning"></i> ${h.tiempo_parado}s</span>
                        </div>
                        <!-- Desglose de Tarifas (Nuevo) -->
                        <div class="text-secondary" style="font-size: 0.75rem;">
                            Tarifas: Mov(${tMov}€) / Stop(${tPar}€)
                        </div>
                    </td>
                    <td class="text-end pe-4 align-middle">
                        <span class="fw-bold text-success fs-5">${h.total_coste.toFixed(2)} €</span>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });

    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-danger">Error al cargar historial</td></tr>';
        console.error(e);
    }
});

// --- CONFIGURACIÓN ---
document.getElementById('btnOpenConfig').addEventListener('click', async () => {
    try {
        const conf = await api('/config');
        dom.inputs.parado.value = conf.tarifa_parado;
        dom.inputs.mov.value = conf.tarifa_movimiento;
    } catch(e) {}
});

dom.btns.configSave.addEventListener('click', async () => {
    const p = parseFloat(dom.inputs.parado.value);
    const m = parseFloat(dom.inputs.mov.value);
    if(p<=0 || m<=0) return Swal.fire('Error', 'Valores inválidos', 'error');

    try {
        await api('/config', 'PUT', { tarifa_parado: p, tarifa_movimiento: m, moneda: "€" });
        dom.modals.config.hide();
        Swal.fire({title: 'Guardado', icon: 'success', toast: true, position: 'top-end', timer: 2000, showConfirmButton: false});
    } catch(e) { Swal.fire('Error', e.message, 'error'); }
});

// Helper Vista
function cambiarVista(v) {
    if(v==='login') { dom.views.login.classList.remove('d-none'); dom.views.dashboard.classList.add('d-none'); }
    else { dom.views.login.classList.add('d-none'); dom.views.dashboard.classList.remove('d-none'); }
}