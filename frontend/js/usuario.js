const API_URL = "http://localhost:8000"

function getToken() {
    return localStorage.getItem("token")
}

function cerrarSesion() {
    localStorage.clear()
    window.location.href = "login.html"
}

// ─── ESPACIOS ───────────────────────────────────────────

async function cargarEspacios() {
    const token = getToken()
    try {
        const response = await fetch(`${API_URL}/espacios/`, {
            headers: { Authorization: `Bearer ${token}` }
        })
        const espacios = await response.json()
        const lista = document.getElementById("listaEspacios")
        lista.innerHTML = ""
        espacios.forEach(e => {
            lista.innerHTML += `
                <div class="cardEspacio">
                    <h3>${e.nombre}</h3>
                    <p>📍 ${e.ubicacion}</p>
                    <p>👥 Capacidad: ${e.capacidad}</p>
                    <p>Estado: <strong>${e.estado}</strong></p>
                </div>
            `
        })
    } catch (error) {
        console.error("Error cargando espacios:", error)
    }
}

// ─── RESERVAS ───────────────────────────────────────────

async function cargarMisReservas() {
    const token = getToken()
    try {
        const response = await fetch(`${API_URL}/reservas/`, {
            headers: { Authorization: `Bearer ${token}` }
        })
        const reservas = await response.json()
        const lista = document.getElementById("listaReservas")
        lista.innerHTML = ""
        reservas.forEach(r => {
            lista.innerHTML += `
                <div class="cardEspacio">
                    <p><strong>Reserva #${r.id_reserva}</strong></p>
                    <p>📅 ${r.fecha} | ⏰ ${r.hora_inicio} - ${r.hora_fin}</p>
                    <p>👥 Asistentes: ${r.cantidad_asistentes}</p>
                    <p>Estado: <strong>${r.estado}</strong></p>
                    <button onclick="cancelarReserva(${r.id_reserva})">🗑️ Cancelar</button>
                </div>
            `
        })
    } catch (error) {
        console.error("Error cargando reservas:", error)
    }
}

async function crearReserva() {
    const token = getToken()
    const id_espacio = document.getElementById("espacio").value
    const fecha = document.getElementById("fecha").value
    const hora_inicio = document.getElementById("horaInicio").value
    const hora_fin = document.getElementById("horaFin").value
    const cantidad_asistentes = document.getElementById("cantidad").value
    const mensaje = document.getElementById("mensajeReserva")

    if (!id_espacio || !fecha || !hora_inicio || !hora_fin || !cantidad_asistentes) {
        mensaje.textContent = "Complete todos los campos"
        mensaje.style.color = "red"
        return
    }

    try {
        const response = await fetch(`${API_URL}/reservas/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({
                id_espacio: parseInt(id_espacio),
                fecha,
                hora_inicio,
                hora_fin,
                cantidad_asistentes: parseInt(cantidad_asistentes)
            })
        })

        if (response.ok) {
            mensaje.textContent = "✅ Reserva creada exitosamente"
            mensaje.style.color = "green"
            document.getElementById("espacio").value = ""
            document.getElementById("fecha").value = ""
            document.getElementById("horaInicio").value = ""
            document.getElementById("horaFin").value = ""
            document.getElementById("cantidad").value = ""
            cargarMisReservas()
        } else {
            const error = await response.json()
            mensaje.textContent = "❌ " + (error.detail || "Error al crear reserva")
            mensaje.style.color = "red"
        }
    } catch (error) {
        mensaje.textContent = "❌ Error al conectar con el servidor"
        mensaje.style.color = "red"
    }
}

async function cancelarReserva(id) {
    const token = getToken()
    const response = await fetch(`${API_URL}/reservas/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` }
    })
    if (response.ok) {
        alert("Reserva cancelada")
        cargarMisReservas()
    }
}

// ─── INICIO ─────────────────────────────────────────────

window.onload = () => {
    if (!getToken()) {
        window.location.href = "login.html"
        return
    }
    cargarEspacios()
    cargarMisReservas()
}