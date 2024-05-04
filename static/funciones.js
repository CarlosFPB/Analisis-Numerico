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
}, 100);

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
    toastify('Borrando pasos...', 4);
    $stepbystep = document.getElementById('stepbystep');

    $stepbystep.innerHTML = `<center><p style="opacity: 0.2; font-weight: 700; color: #16167f;">Aqui se mostrará el procedimiento</p></center>`;
    $stepbystep.style.width = "unset";
    document.getElementById('result').style.display = 'none';
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

setTimeout(() => {
    cambiarEstadoSugerencias()
}, 4000);

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
        .then(response => response.json())
        .then(data => {
            // Maneja la respuesta del servidor
            toastify('Mostrando pasos...', 2);
            console.log(data);
            mostrarPasos(data)
        })
        .catch(error => {
            // Maneja el error
            toastify('Error al realizar la solicitud', 4);
            toastify(error, 5);
            console.error('Error al realizar la solicitud::', error);
            console.log(datos);

        });
}

function prueba() {
    console.log('Hola');
}


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


function mostrarPasos(arrayPasos) {
    let creaTabla = function (arreglo) {
        let tabla = '<div class="tablecontainer"><table>'
        arreglo.forEach(row => {
            tabla += "<tr>"
            row.forEach(value => {
                tabla += "<td>" + value + "</td>"
            })
            tabla += "</tr>"
        })
        tabla += "</table></div>"
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



    $stepbystep = document.getElementById('stepbystep');
    $stepbystep.innerHTML = texto;
    $stepbystep.style.width = "min-content";
}



let mockJson = [
    {
        "content": "Metodo de Biseccion",
        "type": "titulo1"
    },
    {
        "content": ["f(x):", "x^3 - 7x^2 + 14x - 6"],
        "type": "clavevalor"
    },
    {
        "content": "Este metodo nos sirve para encontrar la raiz de una ecuacion, para ello se necesita una funcion f(x) continua en un intervalo [a,b] que contenga a la raiz.",
        "type": "parrafo"
    },
    {
        "content": [
            [
                "Iteracion",
                "X1",
                "Xu",
                "Xr",
                "f(Xr)",
                "Condicion",
                "Error"
            ],
            [
                "1",
                "0.1",
                "0.8",
                "0.8",
                "-0.282233171099891",
                "<0",
                "100"
            ],
            [
                "2",
                "0.45",
                "0.8",
                "0.45",
                "0.151010157102128",
                ">0",
                "77.77777777777779"
            ],
            [
                "3",
                "0.45",
                "0.625",
                "0.625",
                "-0.0168374822961602",
                "<0",
                "27.999999999999996"
            ],
            [
                "4",
                "0.5375",
                "0.625",
                "0.5375",
                "0.00876353787302869",
                ">0",
                "16.279069767441865"
            ],
            [
                "5",
                "0.5375",
                "0.58125",
                "0.58125",
                "-0.00102993808767554",
                "<0",
                "7.526881720430119"
            ],
            [
                "6",
                "0.559375",
                "0.58125",
                "0.559375",
                "0.000569412832638296",
                ">0",
                "3.910614525139681"
            ],
            [
                "7",
                "0.559375",
                "0.5703125",
                "0.5703125",
                "-6.05141018501493e-5",
                "<0",
                "1.9178082191780899"
            ],
            [
                "8",
                "0.56484375",
                "0.5703125",
                "0.56484375",
                "4.39517676379043e-5",
                ">0",
                "0.9681881051175697"
            ],
            [
                "9",
                "0.56484375",
                "0.567578125",
                "0.567578125",
                "-2.45657024490014e-6",
                "<0",
                "0.481761871989"
            ],
            [
                "10",
                "0.5662109375",
                "0.567578125",
                "0.5662109375",
                "5.26857160350921e-6",
                ">0",
                "0.24146257330115406"
            ],
            [
                "11",
                "0.56689453125",
                "0.567578125",
                "0.56689453125",
                "5.69730752705318e-7",
                ">0",
                "0.12058570198105867"
            ],
            [
                "12",
                "0.56689453125",
                "0.567236328125",
                "0.567236328125",
                "-5.68417934047504e-8",
                "<0",
                "0.060256520616342034"
            ]
        ],
        "type": "tabla"
    }
]