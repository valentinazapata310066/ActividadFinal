// Función para login
async function loginUsuario(correo, password) {
    const formData = new URLSearchParams();
    formData.append('username', correo);
    formData.append('password', password);
    
    const response = await fetch('/auth/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error de autenticación');
    }
    
    const data = await response.json();
    console.log('Respuesta del servidor:', data);
    return data;
}

// Función principal de login
async function login() {
    const correo = document.getElementById("correo").value;
    const password = document.getElementById("password").value;
    const mensaje = document.getElementById("mensaje");

    if (!correo || !password) {
        mensaje.textContent = "Por favor ingresa correo y contraseña";
        mensaje.style.color = "red";
        return;
    }

    try {
        const data = await loginUsuario(correo, password);
        console.log('Token recibido:', data.access_token);

        if (data.access_token) {
            // Guardar token
            localStorage.setItem("token", data.access_token);
            
            // Decodificar el token para obtener el rol
            try {
                const payload = JSON.parse(atob(data.access_token.split(".")[1]));
                console.log('Payload decodificado:', payload);
                localStorage.setItem("rol", payload.rol);
                localStorage.setItem("id_usuario", payload.id_usuario);
                
                // Redirigir según el rol
                if (payload.rol === "admin") {
                    window.location.href = "/admin.html";
                } else {
                    window.location.href = "/usuario.html";
                }
            } catch (decodeError) {
                console.error('Error decodificando token:', decodeError);
                mensaje.textContent = "Error procesando la autenticación";
                mensaje.style.color = "red";
            }
        } else {
            mensaje.textContent = "Correo o contraseña incorrectos";
            mensaje.style.color = "red";
        }
    } catch (error) {
        console.error('Error detallado:', error);
        mensaje.textContent = error.message || "Error al conectar con el servidor";
        mensaje.style.color = "red";
    }
}

// Función para verificar autenticación
function verificarAutenticacion() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/login.html";
    }
    return token;
}

// Función para cerrar sesión
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("rol");
    localStorage.removeItem("id_usuario");
    window.location.href = "/login.html";
}

// Ejecutar cuando la página cargue
document.addEventListener('DOMContentLoaded', function() {
    console.log('Página de login cargada');
    // Si ya está autenticado, redirigir
    const token = localStorage.getItem("token");
    if (token && window.location.pathname === '/login.html') {
        const rol = localStorage.getItem("rol");
        if (rol === "admin") {
            window.location.href = "/admin.html";
        } else if (rol === "usuario") {
            window.location.href = "/usuario.html";
        }
    }
});