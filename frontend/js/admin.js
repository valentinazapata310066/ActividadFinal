async function cargarTodasReservas() {
    const token = localStorage.getItem("token")
    const reservas = await getReservas(token)
    const lista = document.getElementById("lista-reservas")
    lista.innerHTML = ""

    reservas.forEach(r => {
        lista.innerHTML += `
            <div class="card">
                <p><strong>Reserva #${r.id_reserva}</strong></p>
                <p>📅 ${r.fecha} | ⏰ ${r.hora_inicio} - ${r.hora_fin}</p>
                <p>👤 Usuario: ${r.id_usuario}</p>
                <p>Estado: <strong>${r.estado}</strong></p>
                <button onclick="aprobar(${r.id_reserva})">✅ Aprobar</button>
                <button onclick="rechazar(${r.id_reserva})">❌ Rechazar</button>
            </div>
        `
    })
}

async function aprobar(id) {
    const token = localStorage.getItem("token")
    const resultado = await actualizarEstadoReserva(token, id, "aprobada")
    if (resultado.id_reserva) {
        alert("Reserva aprobada")
        cargarTodasReservas()
    }
}

async function rechazar(id) {
    const token = localStorage.getItem("token")
    const resultado = await actualizarEstadoReserva(token, id, "rechazada")
    if (resultado.id_reserva) {
        alert("Reserva rechazada")
        cargarTodasReservas()
    }
}

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

function cerrarSesion() {
    localStorage.clear()
    window.location.href = "login.html"
}

window.onload = () => {
    if (!localStorage.getItem("token")) {
        window.location.href = "login.html"
    }
    if (localStorage.getItem("rol") !== "admin") {
        window.location.href = "usuario.html"
    }
    cargarTodasReservas()
    cargarEspacios()
}