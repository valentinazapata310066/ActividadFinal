function cerrarSesion(){
    localStorage.removeItem("token");
    window.location.href="login.html";
}

let reservas=[];

function crearReserva(){

    let espacio =
        document.getElementById("espacio").value;

    let fecha =
        document.getElementById("fecha").value;

    let horaInicio =
        document.getElementById("horaInicio").value;

    let horaFin =
        document.getElementById("horaFin").value;

    let mensaje =
        document.getElementById("mensajeReserva");

    if(
        espacio=="" ||
        fecha=="" ||
        horaInicio=="" ||
        horaFin==""
    ){
        mensaje.innerText =
            "Complete todos los campos";
        return;
    }

    let reserva = {
        espacio,
        fecha,
        horaInicio,
        horaFin
    };

    reservas.push(reserva);

    mensaje.innerText =
        "Reserva creada (modo prueba)";

    mostrarReservas();

    document.getElementById("espacio").value="";
    document.getElementById("fecha").value="";
    document.getElementById("horaInicio").value="";
    document.getElementById("horaFin").value="";
}

function mostrarReservas(){

    let lista =
        document.getElementById("listaReservas");

    lista.innerHTML="";

    reservas.forEach((r,index)=>{

        lista.innerHTML += `
            <div class="cardEspacio">
                <h3>${r.espacio}</h3>
                <p>${r.fecha}</p>
                <p>${r.horaInicio} - ${r.horaFin}</p>

                <button onclick="cancelarReserva(${index})">
                    Cancelar
                </button>
            </div>
        `;
    });
}

function cancelarReserva(index){
    reservas.splice(index,1);
    mostrarReservas();
}