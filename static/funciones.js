document.body.innerHTML += `
<dialog id="loader">
        <div class="hamster-bg">
            <div aria-label="Orange and tan hamster running in a metal wheel" role="img" class="wheel-and-hamster">
                <div class="wheel"></div>
                <div class="hamster">
                    <div class="hamster__body">
                        <div class="hamster__head">
                            <div class="hamster__ear"></div>
                            <div class="hamster__eye"></div>
                            <div class="hamster__nose"></div>
                        </div>
                        <div class="hamster__limb hamster__limb--fr"></div>
                        <div class="hamster__limb hamster__limb--fl"></div>
                        <div class="hamster__limb hamster__limb--br"></div>
                        <div class="hamster__limb hamster__limb--bl"></div>
                        <div class="hamster__tail"></div>
                    </div>
                </div>
                <div class="spoke"></div>
            </div>
            <center>
                <span class="loadingTxt">Cargando...</span>
            </center>
        </div>
    </dialog>
    `

let toastify = function (mensaje, type = 1) {
    color = ""
    switch (type) {
        case 1:
            color = "linear-gradient(to right, #00b09b, #96c93d)"
            break;
        case 2:
            color = "linear-gradient(135deg, #37f965 0%, #0e9740 100%)"
            break;
        case 3:
            color = "linear-gradient(135deg, #11e3ee 0%, #008cdd 100%)"
            break;
        case 4:
            color = "linear-gradient(to right, #ff416c, #ff4b2b)"
            break;
        case 5:
            color = "linear-gradient(to right, #aaaaaa, #555555)";
            break;
    }


    Toastify({
        text: mensaje,
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            background: color,
        },
        onClick: function () { } // Callback after click
    }).showToast();
}

function guardarPDF(divId) {


    toastify('Guardando PDF...', 3);
    var divContent = document.getElementById(divId);
    var contenidoOriginal = document.body.innerHTML;
    window.print();
}

function borrarPasos() {
    ocultarStepByStep();
    toastify('Borrando pasos...', 4);
    $stepbystep = document.getElementById('stepbystep');
    let inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.style.transition = "all 0.5s ease";
        input.style.backgroundColor = "rgba(255, 150, 0, 0.2)";
        input.value = '';
        setTimeout(() => {
            input.style.backgroundColor = "";
        }, 500);
    });

    setTimeout(() => {

        $stepbystep.innerHTML = `<center><p style="opacity: 0.2; font-weight: 700; color: #16167f;">Aqui se mostrará el procedimiento</p></center>`;
        $stepbystep.style.width = "unset";
        mostrarStepByStep();
        document.getElementById('result').style.display = 'none';
    }, 500);
}

function mostrarloader() {
    document.getElementById('loader').style.display = 'flex';
}

function mostrarDialog(id) {
    document.getElementById(id).style.display = 'flex';
    setTimeout(() => {
        document.getElementById(id).style.opacity = 1;
    }, 1);
    document.addEventListener('click', function (event) {
        var dialog = document.getElementById(id);
        var content = document.querySelector('.contenido');
        if (event.target === dialog) {
            content.classList.add('close');
            cerrarDialog(id);
        }
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                cerrarDialog(id);
            }
        }
        );
    });
}

function cerrarDialog(id) {
    document.getElementById(id).style.opacity = 0;
    setTimeout(() => {
        document.getElementById(id).style.display = 'none';
    }, 500);
    document.removeEventListener('click', function (event) { });
    document.removeEventListener('keydown', function (event) { });
}

let ocultarStepByStep = function () {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
    $stepbystep = document.getElementById('stepbystep');
    $stepbystep.style.transform = "scale(0)";
    $stepbystep.style.opacity = 0;
}

let mostrarStepByStep = function () {
    $stepbystep = document.getElementById('stepbystep');
    $stepbystep.style.transform = "scale(1)";
    $stepbystep.style.opacity = 1;
    $stepbystep.style.height = "unset";
}

function cambiarEstadoSugerencias() {
    let estado = document.querySelector(".sugerencias").style.right;
    let ancho = document.querySelector(".sugerencias").offsetWidth;
    if (estado == "0px" || estado == "") {
        document.querySelector(".sugerencias").style.right = `calc(-${ancho}px + 10px)`;
    } else {
        document.querySelector(".sugerencias").style.right = "0px";
    }
    let viñeta = document.querySelector(".viñeta");
    if (viñeta.style.transform === "") {
        viñeta.style.transform = "rotate(180deg)";
    } else {
        viñeta.style.transform = "";
    }
}

function mostrarEjercicio() {
    for (let i = 1; i < ejercicios.length; i++) {
        let ejercicio = ejercicios[i];
        let div = document.createElement("div");
        div.innerHTML = `Ejericio ${i}`;
        div.setAttribute("onclick", `cargarEjercicio(${i})`);
        document.getElementById("ejercicios").appendChild(div);
    }
}

setTimeout(() => {
    mostrarEjercicio();
}, 200);

setTimeout(() => {
    cambiarEstadoSugerencias()
}, 4000);

function cargarEjercicio(i) {

    try {
        let ejercicio = ejercicios[i];
        variables.forEach((variable, index) => {
            document.getElementById(variable).value = ejercicio[index];
        });
        toastify(`Ejercicio #${i}`, 1);
    } catch (error) {
        toastify('Error al cargar el ejercicio', 4);
    }
}

//#region Manejo de peticiones
function realizarPeticionPOST(endPoint, datos) {
    console.log(`peticion realizada a en: ${endPoint}`);
    toastify('Realizando petición...', 1);
    fetch(endPoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(datos),
    })
        .then(response => {
            let status = response.status;
            console.log(`Status: ${status}`);
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data.hasOwnProperty("error")) {
                mostrarError(data.error);
            } else {
                toastify('Mostrando pasos...', 2);
                mostrarPasos(data)
            }
        })
        .catch(error => {
            // Maneja el error
            toastify('Error al realizar la solicitud', 4);
            toastify(error, 5);
            console.error('Error al realizar la solicitud::', error);
        });
}


function mostrarError(error) {
    ocultarStepByStep();

    setTimeout(() => {
        
    toastify('Error al realizar la solicitud', 4);
    toastify(error, 5);
    console.error('Error al realizar la solicitud::', error);

    $stepbystep = document.getElementById('stepbystep');
    $stepbystep.innerHTML = `<center><p style="opacity: 0.7; font-weight: 700; color: red;">${error}</p></center>`;
    mostrarStepByStep();
    }, 500);

}

function mostrarPasos(arrayPasos) {

    ocultarStepByStep();

    let creaTabla = function (arreglo) {
        let tabla = '<center><div class="tablecontainer"><table>'
        arreglo.forEach(row => {
            tabla += "<tr>"
            row.forEach(value => {
                tabla += "<td>" + value + "</td>"
            })
            tabla += "</tr>"
        })
        tabla += "</table></div></center>"
        return tabla
    }
    let añadirClaveValor = function (clave, valor) {
        return `<p class="clavevalor"><span>${clave}</span><span>${valor}</span></p>`;
    }
    let añadirlinea = function (linea) {
        return `<p>${linea}</p>`;
    }
    let agregarTitulo1 = function (titulo) {
        return `<p class="titulo1">${titulo}</p>`;
    }
    let añadirSalto = function () {
        return `<br>`;
    }
    let añadirTab = function () {
        return `\t`;
    }
    let texto = "";

    let intervalo = 500;

    setTimeout(() => {
        arrayPasos.forEach(linea => {
            switch (linea.type) {
                case "parrafo":
                    texto += añadirlinea(linea.content);
                    break;
                case "titulo1":
                    texto += agregarTitulo1(linea.content);
                    break;
                case "clavevalor":
                    texto += añadirClaveValor(linea.content[0], linea.content[1]);
                    break;
                case "salto":
                    texto += añadirSalto();
                    break;
                case "tabla":
                    texto += creaTabla(linea.content);
                    break;
                case "tab":
                    texto += añadirTab();
                    break;
                default:
                    texto += añadirlinea(linea.content);
                    break;
            }
        });
        document.getElementById('stepbystep').innerHTML = texto;
        mostrarStepByStep();
    }, intervalo);

    toastify('Pasos cargados', 2);
}

