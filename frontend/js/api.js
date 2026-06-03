const API_URL = "http://localhost:8000"

async function loginUsuario(correo, password) {
    const response = await fetch(`${API_URL}/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username: correo, password: password })
    })
    return response.json()
}

async function getEspacios(token) {
    const response = await fetch(`${API_URL}/espacios/`, {
        headers: { Authorization: `Bearer ${token}` }
    })
    return response.json()
}

async function crearReserva(token, datos) {
    const response = await fetch(`${API_URL}/reservas/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(datos)
    })
    return response.json()
}

async function getReservas(token) {
    const response = await fetch(`${API_URL}/reservas/`, {
        headers: { Authorization: `Bearer ${token}` }
    })
    return response.json()
}

async function actualizarEstadoReserva(token, id, estado) {
    const response = await fetch(`${API_URL}/reservas/${id}/estado`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ estado })
    })
    return response.json()
}