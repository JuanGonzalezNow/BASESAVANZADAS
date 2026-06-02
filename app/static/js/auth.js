/* ═══════════════════════════════════════════════════════
   auth.js — RIDEAXIS
═══════════════════════════════════════════════════════ */

/* ── TOAST ──────────────────────────────────────────────── */
function showToast(message, subtitle = '', type = 'success') {
    const existing = document.getElementById('rideaxis-toast');
    if (existing) existing.remove();

    if (!document.getElementById('toast-keyframes')) {
        const s = document.createElement('style');
        s.id = 'toast-keyframes';
        s.textContent = `
            @keyframes toastIn  { from{opacity:0;transform:translateX(40px) scale(.95)} to{opacity:1;transform:translateX(0) scale(1)} }
            @keyframes toastOut { from{opacity:1;transform:translateX(0) scale(1)} to{opacity:0;transform:translateX(40px) scale(.95)} }
        `;
        document.head.appendChild(s);
    }

    const isSuccess = type === 'success';
    const color     = isSuccess ? '#16a34a' : '#dc2626';
    const bgCircle  = isSuccess ? '#dcfce7'  : '#fee2e2';
    const icon      = isSuccess
        ? `<polyline points="20 6 9 17 4 12"></polyline>`
        : `<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>`;

    const toast = document.createElement('div');
    toast.id = 'rideaxis-toast';
    toast.innerHTML = `
        <div style="
            position:fixed; top:24px; right:24px; z-index:9999;
            background:#fff; border-radius:16px;
            box-shadow:0 8px 40px rgba(0,0,0,.18),0 2px 8px rgba(0,0,0,.08);
            padding:16px 20px 16px 16px;
            display:flex; align-items:flex-start; gap:14px;
            min-width:300px; max-width:360px;
            border-left:4px solid ${color};
            font-family:'Barlow',sans-serif;
            animation:toastIn .4s cubic-bezier(.34,1.56,.64,1) forwards;
        ">
            <div style="width:38px;height:38px;min-width:38px;background:${bgCircle};border-radius:50%;display:flex;align-items:center;justify-content:center;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                     stroke="${color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    ${icon}
                </svg>
            </div>
            <div style="flex:1;padding-top:2px;">
                <p style="margin:0;font-weight:900;font-size:14px;color:#111827;">${message}</p>
                ${subtitle ? `<p style="margin:4px 0 0;font-size:12px;color:#6b7280;font-weight:600;">${subtitle}</p>` : ''}
            </div>
            <button id="toast-close-btn" style="background:none;border:none;cursor:pointer;color:#9ca3af;font-size:16px;padding:0;line-height:1;margin-top:2px;">✕</button>
        </div>`;

    document.body.appendChild(toast);
    document.getElementById('toast-close-btn').addEventListener('click', () => dismissToast(toast));
    setTimeout(() => dismissToast(toast), 4500);
}

function dismissToast(toast) {
    if (!toast?.isConnected) return;
    const inner = toast.querySelector('div');
    if (inner) inner.style.animation = 'toastOut .3s ease forwards';
    setTimeout(() => toast.remove(), 320);
}

/* ── HELPERS DE ERROR ────────────────────────────────────── */
function setFieldError(errorId, msg, inputEl) {
    const el = document.getElementById(errorId);
    if (!el) return;
    if (msg) {
        el.textContent = msg;
        el.classList.remove('hidden');
        if (inputEl) {
            inputEl.style.borderColor = '#dc2626';
            inputEl.style.boxShadow   = '0 0 0 3px rgba(220,38,38,0.09)';
        }
    } else {
        el.textContent = '';
        el.classList.add('hidden');
        if (inputEl) {
            inputEl.style.borderColor = '';
            inputEl.style.boxShadow   = '';
        }
    }
}

function clearErrors(formId) {
    document.querySelectorAll(`#${formId} small`).forEach(el => {
        el.classList.add('hidden');
        el.textContent = '';
    });
    document.querySelectorAll(`#${formId} .auth-input`).forEach(el => {
        el.style.borderColor = '';
        el.style.boxShadow   = '';
    });
}

/* ── VALIDACIÓN EN TIEMPO REAL ───────────────────────────── */
const REGEX_LETRAS   = /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s'-]+$/;
const REGEX_TELEFONO = /^\d+$/;

function attachRealTimeValidation() {
    const nombreInput = document.querySelector('#registroForm [name="nombre"]');
    if (nombreInput) {
        nombreInput.addEventListener('input', () => {
            const val = nombreInput.value;
            if (val && !REGEX_LETRAS.test(val)) {
                setFieldError('registroError_nombre', 'El nombre solo puede contener letras.', nombreInput);
            } else {
                setFieldError('registroError_nombre', '', nombreInput);
            }
        });
    }

    const apellidoInput = document.querySelector('#registroForm [name="apellido"]');
    if (apellidoInput) {
        apellidoInput.addEventListener('input', () => {
            const val = apellidoInput.value;
            if (val && !REGEX_LETRAS.test(val)) {
                setFieldError('registroError_apellido', 'El apellido solo puede contener letras.', apellidoInput);
            } else {
                setFieldError('registroError_apellido', '', apellidoInput);
            }
        });
    }

    const telefonoInput = document.querySelector('#registroForm [name="telefono"]');
    if (telefonoInput) {
        telefonoInput.addEventListener('input', () => {
            const val = telefonoInput.value;
            if (val && !REGEX_TELEFONO.test(val)) {
                setFieldError('registroError_telefono', 'El teléfono solo puede contener números.', telefonoInput);
            } else {
                setFieldError('registroError_telefono', '', telefonoInput);
            }
        });
    }

    ['correo_electronico', 'numero_documento', 'contrasena_hash', 'id_tipo_documento'].forEach(name => {
        const el = document.querySelector(`#registroForm [name="${name}"]`);
        if (el) el.addEventListener('input', () => setFieldError(`registroError_${name}`, '', el));
    });

    ['correo_electronico', 'contrasena_hash'].forEach(name => {
        const el = document.querySelector(`#loginForm [name="${name}"]`);
        if (el) el.addEventListener('input', () => setFieldError(`loginError_${name}`, '', el));
    });
}

/* ── REGISTRO ────────────────────────────────────────────── */
document.getElementById('registroForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearErrors('registroForm');

    const btn = e.target.querySelector('.auth-btn');
    const originalText = btn.textContent;
    btn.textContent = 'Creando cuenta...';
    btn.disabled = true;

    const formData = new FormData(document.getElementById('registroForm'));

    try {
        const response = await fetch('/auth/registro', {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': formData.get('csrf_token') }
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('loginModal').classList.remove('open');
            document.getElementById('registroForm').reset();
            clearErrors('registroForm');
            setTimeout(() => switchTab('login'), 300);
            setTimeout(() => {
                showToast(
                    '¡Cuenta creada con éxito!',
                    `Bienvenido/a${data.nombre ? ', ' + data.nombre : ''}. Ya puedes iniciar sesión.`,
                    'success'
                );
            }, 400);

        } else {
            if (data.errors) {
                Object.keys(data.errors).forEach(field => {
                    const errorEl = document.getElementById(`registroError_${field}`);
                    const inputEl = document.querySelector(`#registroForm [name="${field}"]`);
                    if (errorEl) { errorEl.textContent = data.errors[field]; errorEl.classList.remove('hidden'); }
                    if (inputEl) { inputEl.style.borderColor = '#dc2626'; inputEl.style.boxShadow = '0 0 0 3px rgba(220,38,38,0.09)'; }
                });
            } else {
                showToast('Error al registrar', data.message || 'Intenta de nuevo.', 'error');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión', 'Verifica tu internet e intenta de nuevo.', 'error');
    } finally {
        btn.textContent = originalText;
        btn.disabled = false;
    }
});

/* ── LOGIN ───────────────────────────────────────────────── */
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearErrors('loginForm');

    const btn = e.target.querySelector('.auth-btn');
    const originalText = btn.textContent;
    btn.textContent = 'Ingresando...';
    btn.disabled = true;

    const formData = new FormData(document.getElementById('loginForm'));

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': formData.get('csrf_token') }
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('loginModal').classList.remove('open');
            showToast('¡Bienvenido de nuevo!', data.message || '', 'success');

            // Redireccionar según rol
            if (data.es_admin) {
                setTimeout(() => location.href = '/admin/dashboard', 1000);
            } else {
                setTimeout(() => location.reload(), 1000);
            }
        } else {
            if (data.errors) {
                Object.keys(data.errors).forEach(field => {
                    const errorEl = document.getElementById(`loginError_${field}`);
                    const inputEl = document.querySelector(`#loginForm [name="${field}"]`);
                    if (errorEl) { errorEl.textContent = data.errors[field]; errorEl.classList.remove('hidden'); }
                    if (inputEl) { inputEl.style.borderColor = '#dc2626'; inputEl.style.boxShadow = '0 0 0 3px rgba(220,38,38,0.09)'; }
                });
            } else {
                showToast('Error al ingresar', data.message || 'Correo o contraseña incorrectos.', 'error');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión', 'Verifica tu internet e intenta de nuevo.', 'error');
    } finally {
        btn.textContent = originalText;
        btn.disabled = false;
    }
});

/* ── INICIALIZAR ─────────────────────────────────────────── */
attachRealTimeValidation();