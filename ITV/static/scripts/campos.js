window.addEventListener("load", inicializar, false);

function inicializar() {
    clases(document.getElementById("id_rol"));
    document.getElementById("id_rol").addEventListener("click", campos, false);
}
var clasecliente=document.getElementsByClassName("cliente");
var clasetrabajador=document.getElementsByClassName("trabajador");

function clases(id){
    var listacliente=[
        document.getElementById("id_fecha_nacimiento"),
        document.getElementById("id_apellidos"),
        document.getElementById("id_dni")];
    var listatrabajador=[
        document.getElementById("id_puesto")];
    listacliente.forEach(id=>{
        id.parentNode.setAttribute("class","cliente bg-info bg-opacity-25")
    });
    listatrabajador.forEach(id=>id.parentNode.setAttribute("class","trabajador"));
    [...clasecliente].forEach(id=>id.setAttribute("style","display:none"));
    [...clasetrabajador].forEach(id=>id.setAttribute("style","display:none"));
    ocultar(id.value);
    mostrar(id.value);
}

function ocultar(opcion){
    if (opcion=="2"){
        [...clasetrabajador].forEach(id=>id.setAttribute("style","display:none"));              
    } else if (opcion == "3") {        
        [...clasecliente].forEach(id=>id.setAttribute("style","display:none")); 
    }  else { 
        [...clasetrabajador].forEach(id=>id.setAttribute("style","display:none")); 
        [...clasecliente].forEach(id=>id.setAttribute("style","display:none"));        
    }
}

function mostrar(opcion){
    if (opcion=="2"){
        [...clasecliente].forEach(id=>id.setAttribute("style","display:block"));              
    }

    if (opcion == "3") {        
        [...clasetrabajador].forEach(id=>id.setAttribute("style","display:block")); 
    }
}

function campos(e){
    var rol = e.currentTarget.value;
    ocultar(rol);
    mostrar(rol);
}