    let texto = "";
let stepbyStep = document.getElementById("stepbystep");



export function CargaComletada() {
    toastify("Carga completada", 2)
    const loading = document.getElementById('loader')
    loading.style.display = 'none'
    
    const $calcular = document.getElementById('calcular');
    const $guardar = document.getElementById('guardar');
    const $borrar = document.getElementById('borrar');
    const $cargarModelo = document.getElementById('cargarModelo');
    
    $calcular.style.display = 'flex';
    $guardar.style.display = 'flex';
    $borrar.style.display = 'flex';
    $cargarModelo.style.display = 'none';
}

export function mostrarLoader() {
    const loading = document.getElementById('loader')
    loading.style.display = 'flex'
}

export function ocultarLoader() {
    const loading = document.getElementById('loader')
    loading.style.display = 'none'
}


export function obtenerTexto() {
    return texto
}
export function resetarTexto() {
    texto = ""
}
export function agregarTexto(textoNuevo) {
    texto += "<p>" + textoNuevo + "</p>"
}

export function agregarTitulo1(textoNuevo) {
    texto += '<p class="titulo1">' + textoNuevo + "</p>"
}

export function creartabla(arreglo) {
    let tabla = '<div class="tablecontainer"><table>'
    arreglo.forEach(row => {
        tabla += "<tr>"
        row.forEach(value => {
            tabla += "<td>" + value + "</td>"
        })
        tabla += "</tr>"

    })
    tabla += "</table></div>"
    texto += tabla

}
export function añadirsalto() {
    texto += "<br>"
}
export function añadirTab() {
    texto += "\t"
}
export function mostrarTexto() {
    stepbyStep.innerHTML = texto
    toastify("Cálculo completado", 2)
}

