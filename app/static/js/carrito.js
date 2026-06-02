/* ═══════════════════════════════════════════════════════
   carrito.js — Gestión del Carrito de Compras RIDEAXIS
═══════════════════════════════════════════════════════ */

async function addToCart(idMoto, modeloMoto = '') {
    if (!isLoggedIn) {
        toggleLoginModal();
        switchTab('login');
        showToast('Debes iniciar sesión para agregar al carrito', '', 'error');
        return;
    }

    try {
        const response = await fetch('/carrito/agregar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify({ id_moto: idMoto, cantidad: 1 })
        });

        const data = await response.json();

        if (data.success) {
            showToast('¡Agregado al carrito!', `${modeloMoto || 'Moto'} agregada correctamente.`, 'success');
            updateCartBadge();
        } else {
            showToast('Error', data.message || 'No se pudo agregar al carrito', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión', 'Intenta de nuevo', 'error');
    }
}

async function removeFromCart(idMoto) {
    try {
        const response = await fetch('/carrito/eliminar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify({ id_moto: idMoto })
        });

        const data = await response.json();

        if (data.success) {
            showToast('Removido', 'Item eliminado del carrito', 'success');
            updateCartBadge();
            location.reload();
        } else {
            showToast('Error', data.message || 'No se pudo remover del carrito', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión', 'Intenta de nuevo', 'error');
    }
}
