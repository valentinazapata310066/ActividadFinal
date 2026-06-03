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

async function crearEspacio() {
    const token = getToken()
    const nombre = document.getElementById("nombre").value
    const ubicacion = document.getElementById("ubicacion").value
    const capacidad = document.getElementById("capacidad").value
    const estado = document.getElementById("estado").value
    const mensaje = document.getElementById("mensajeEspacio")

    if (!nombre || !ubicacion || !capacidad) {
        mensaje.textContent = "Complete todos los campos"
        mensaje.style.color = "red"
        return
    }

    try {
        const response = await fetch(`${API_URL}/espacios/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({
                nombre,
                ubicacion,
                capacidad: parseInt(capacidad),
                estado
            })
        })

        if (response.ok) {
            mensaje.textContent = "✅ Espacio creado exitosamente"
            mensaje.style.color = "green"
            document.getElementById("nombre").value = ""
            document.getElementById("ubicacion").value = ""
            document.getElementById("capacidad").value = ""
            cargarEspacios()
        } else {
            const error = await response.json()
            mensaje.textContent = "❌ " + (error.detail || "Error al crear espacio")
            mensaje.style.color = "red"
        }
    } catch (error) {
        mensaje.textContent = "❌ Error al conectar con el servidor"
        mensaje.style.color = "red"
    }
}

// ─── RESERVAS ───────────────────────────────────────────

async function cargarReservas() {
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
                    <button onclick="aprobarReserva(${r.id_reserva})">✅ Aprobar</button>
                    <button onclick="rechazarReserva(${r.id_reserva})">❌ Rechazar</button>
                </div>
            `
        })
    } catch (error) {
        console.error("Error cargando reservas:", error)
    }
}

async function aprobarReserva(id) {
    const token = getToken()
    const response = await fetch(`${API_URL}/reservas/${id}/estado`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ estado: "aprobada" })
    })
    if (response.ok) {
        alert("Reserva aprobada ✅")
        cargarReservas()
    }
}

async function rechazarReserva(id) {
    const token = getToken()
    const response = await fetch(`${API_URL}/reservas/${id}/estado`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ estado: "rechazada" })
    })
    if (response.ok) {
        alert("Reserva rechazada ❌")
        cargarReservas()
    }
}

// ─── INICIO ─────────────────────────────────────────────

window.onload = () => {
    if (!getToken()) {
        window.location.href = "login.html"
        return
    }
    cargarEspacios()
    cargarReservas()
}