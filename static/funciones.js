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
    document.getElementById('stepbystep').innerHTML = `<center><p style="opacity: 0.2; font-weight: 700; color: #16167f;">Aqui se mostrará el procedimiento</p></center>`;
    document.getElementById('result').style.display = 'none';
}

function mostrarloader() {
    document.getElementById('loader').style.display = 'flex';
}

function realizarPeticionPOST(endPoint) {
    console.log(`peticion realizada a en: ${endPoint}`);
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
            console.log(data);
        })
        .catch(error => {
            console.error('Error al realizar la solicitud::', error);
            console.log(datos);
        });
}

function prueba() {
    console.log('Hola');
}