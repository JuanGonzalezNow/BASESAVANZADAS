/* ═══════════════════════════════════════════════════════
   checkout.js — Lógica del Checkout RIDEAXIS
═══════════════════════════════════════════════════════ */

async function procesarCompra() {
    const metodoPago = document.getElementById('metodoPago').value;
    const terminos = document.getElementById('terminos').checked;
    const direccion = document.getElementById('direccion').value;
    const ciudad = document.getElementById('ciudad').value;
    const codigoPostal = document.getElementById('codigoPostal').value;

    if (!metodoPago) {
        showToast('Error', 'Selecciona un método de pago', 'error');
        return;
    }

    if (!terminos) {
        showToast('Error', 'Debes aceptar los términos y condiciones', 'error');
        return;
    }

    if (!direccion || !ciudad || !codigoPostal) {
        showToast('Error', 'Completa todos los datos de entrega', 'error');
        return;
    }

    const btn = document.querySelector('button[onclick="procesarCompra()"]');
    const originalText = btn.textContent;
    btn.textContent = 'Procesando...';
    btn.disabled = true;

    try {
        const response = await fetch('/checkout/procesar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]')?.value || ''
            },
            body: JSON.stringify({
                id_metodo_pago: parseInt(metodoPago),
                direccion: direccion,
                ciudad: ciudad,
                codigo_postal: codigoPostal
            })
        });

        const data = await response.json();

        if (data.success) {
            showToast('¡Compra Exitosa!', `Factura #${data.numero_factura} - Total: $${parseInt(data.total).toLocaleString('es-CO')}`, 'success');
            setTimeout(() => {
                location.href = `/compra-exitosa/${data.id_factura}`;
            }, 1500);
        } else {
            showToast('Error', data.message || 'No se pudo procesar la compra', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión', 'Intenta de nuevo', 'error');
    } finally {
        btn.textContent = originalText;
        btn.disabled = false;
    }
}
