/*function cerrarSesion(){
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

function crearEspacio(){

    let mensaje = document.getElementById("mensajeEspacio");

    mensaje.innerText =
        "Espacio pendiente de conexión backend";
}*/

function cerrarSesion(){
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

let espacios = [];

function crearEspacio(){

    let nombre =
        document.getElementById("nombre").value;

    let ubicacion =
        document.getElementById("ubicacion").value;

    let capacidad =
        document.getElementById("capacidad").value;

    let estado =
        document.getElementById("estado").value;

    let mensaje =
        document.getElementById("mensajeEspacio");

    if(
        nombre=="" ||
        ubicacion=="" ||
        capacidad==""
    ){
        mensaje.innerText =
            "Complete todos los campos";
        return;
    }

    let nuevoEspacio = {
        nombre,
        ubicacion,
        capacidad,
        estado
    };

    espacios.push(nuevoEspacio);

    mensaje.innerText =
        "Espacio agregado (modo prueba)";

    mostrarEspacios();

    document.getElementById("nombre").value="";
    document.getElementById("ubicacion").value="";
    document.getElementById("capacidad").value="";
}

function mostrarEspacios(){

    let lista =
        document.getElementById("listaEspacios");

    lista.innerHTML="";

    espacios.forEach((e,index)=>{

        lista.innerHTML += `
            <div class="cardEspacio">
                <h3>${e.nombre}</h3>
                <p>${e.ubicacion}</p>
                <p>Capacidad: ${e.capacidad}</p>
                <p>Estado: ${e.estado}</p>

                <button onclick="eliminarEspacio(${index})">
                    Eliminar
                </button>
            </div>
        `;
    });
}

function eliminarEspacio(index){
    espacios.splice(index,1);
    mostrarEspacios();
}