async function cargarEspacios() {
    const token = localStorage.getItem("token")
    const espacios = await getEspacios(token)
    const lista = document.getElementById("lista-espacios")
    lista.innerHTML = ""

    espacios.forEach(e => {
        lista.innerHTML += `
            <div class="card">
                <h3>${e.nombre}</h3>
                <p>📍 ${e.ubicacion}</p>
                <p>👥 Capacidad: ${e.capacidad}</p>
                <p>Estado: ${e.estado}</p>
            </div>
        `
    })
}

async function cargarMisReservas() {
    const token = localStorage.getItem("token")
    const reservas = await getReservas(token)
    const lista = document.getElementById("lista-reservas")
    lista.innerHTML = ""

    reservas.forEach(r => {
        lista.innerHTML += `
            <div class="card">
                <p>📅 ${r.fecha} | ⏰ ${r.hora_inicio} - ${r.hora_fin}</p>
                <p>Estado: <strong>${r.estado}</strong></p>
            </div>
        `
    })
}

async function crearReservaForm() {
    const token = localStorage.getItem("token")
    const datos = {
        id_espacio: parseInt(document.getElementById("id_espacio").value),
        fecha: document.getElementById("fecha").value,
        hora_inicio: document.getElementById("hora_inicio").value,
        hora_fin: document.getElementById("hora_fin").value,
        cantidad_asistentes: parseInt(document.getElementById("cantidad_asistentes").value)
    }

    const resultado = await crearReserva(token, datos)
    const mensaje = document.getElementById("mensaje-reserva")

    if (resultado.id_reserva) {
        mensaje.textContent = "✅ Reserva creada exitosamente"
        mensaje.style.color = "green"
        cargarMisReservas()
    } else {
        mensaje.textContent = "❌ " + (resultado.detail || "Error al crear reserva")
        mensaje.style.color = "red"
    }
}

function cerrarSesion() {
    localStorage.clear()
    window.location.href = "login.html"
}

window.onload = () => {
    if (!localStorage.getItem("token")) {
        window.location.href = "login.html"
    }
    cargarEspacios()
    cargarMisReservas()
}