function login(){

    let correo = document.getElementById("correo").value;
    let password = document.getElementById("password").value;
    let mensaje = document.getElementById("mensaje");

    if(correo === "" || password === ""){
        mensaje.innerText = "Complete todos los campos";
        return;
    }

    mensaje.innerText = "Login pendiente de conexión con backend...";
}