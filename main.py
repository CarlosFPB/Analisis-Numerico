from flask import Flask, render_template, request, jsonify, redirect
import os

# Importaciones de métodos
from modelos.unidad_dos.solucion_ecuaciones.iterativos.cerrados.biseccion.Biseccion import medoto_biseccion
from modelos.unidad_dos.solucion_ecuaciones.iterativos.cerrados.falsa_posicion.Falsa_posicion import metodo_falsa_posicion
from modelos.unidad_dos.solucion_ecuaciones.iterativos.abiertos.newton.Newton import metodo_newton
from modelos.unidad_dos.solucion_ecuaciones.iterativos.abiertos.newton_modificado.Newton_modificado import metodo_newton_modificado
from modelos.unidad_dos.solucion_ecuaciones.iterativos.abiertos.punto_fijo.Punto_fijo import metodo_punto_fijo
from modelos.unidad_dos.solucion_ecuaciones.iterativos.abiertos.secante.Secante import metodo_secante
from modelos.unidad_dos.solucion_ecuaciones.iterativos.polinomicos.bairstow.Bairstow import metodo_bairstow
from modelos.unidad_dos.solucion_ecuaciones.iterativos.polinomicos.horner.Horner import metodo_horner
from modelos.unidad_dos.solucion_ecuaciones.iterativos.polinomicos.muller.Muller import metodo_muller
from modelos.unidad_dos.solucion_ecuaciones.directos.polinomicas_menor_2.lineal.Lineal import metodo_lineal
from modelos.unidad_dos.solucion_ecuaciones.directos.polinomicas_menor_2.cuadratica.Cuadratica import metodo_cuadratico
from modelos.unidad_dos.solucion_ecuaciones.directos.polinomicas_mayor_3.ferrari.Ferrari import metodo_ferrari
from modelos.unidad_dos.solucion_ecuaciones.directos.polinomicas_mayor_3.tartaglia.Tartaglia import metodo_tartaglia

#interpolacion
from modelos.unidad_tres.interpolacion.lagrange.Lagrange import metodo_lagrange
from modelos.unidad_tres.interpolacion.newton_recursivo.Newton_recursivo import metodo_newton_recursivo
from modelos.unidad_tres.interpolacion.newton_fracciones_divididas.Newton_fracciones_divididas import metodo_newton_fracciones_divididas
from modelos.unidad_tres.interpolacion.hermite.Hermite import metodo_hermite
from modelos.unidad_tres.interpolacion.trazadores_cubicos.Trazadores import metodo_trazadores
from modelos.unidad_tres.interpolacion.interpolacion_lineal.Interpolacion_lineal import metodo_interpolacion_lineal

#diferenciacion e integracion
from modelos.unidad_cuatro.diferenciacion.derivadas.Diferenciacion import metodos_diferenciacion
from modelos.unidad_cuatro.diferenciacion.richardson.Richardson import metodo_richardson


app = Flask(__name__, static_url_path='/static')

#raiz y errores
@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    # Redirige automáticamente a la URL de la imagen del gato
    return redirect("https://http.cat/404", code=302)

@app.errorhandler(504)
def page_not_found(e):
    #informar que el servidor no responde
    resp = {'error' :  'El servidor no responde'}
    return jsonify(resp), 504

#metodos iterativos cerrados

@app.route('/metodos/iterativos/cerrados/Biseccion', methods=['GET'])
def renderizar_biseccion():
    return render_template('unidad_dos/Biseccion.html')

@app.route('/metodos/iterativos/cerrados/Biseccion', methods=['POST'])
def calcular_biseccion():
    json_data = request.json
    respuesta = medoto_biseccion.calcular_biseccion(json_data)
    return respuesta

@app.route('/metodos/iterativos/cerrados/Falsa_posicion', methods=['GET'])
def renderizar_falsa_posicion():
    return render_template('unidad_dos/Falsa_posicion.html')

@app.route('/metodos/iterativos/cerrados/Falsa_posicion', methods=['POST'])
def calcular_falsa_posicion():
    json_data = request.json
    respuesta = metodo_falsa_posicion.calcular_falsa_posicion(json_data)
    return respuesta

#metodos iterativos abiertos

@app.route('/metodos/directos/abiertos/newton', methods=['GET'])
def Newton():
    return render_template('unidad_dos/Newton.html')

@app.route('/metodos/directos/abiertos/newton', methods=['POST'])
def calcular_newton():
    json_data = request.json
    respuesta = metodo_newton.calcular_newton(json_data)
    return respuesta

@app.route('/metodos/directos/abiertos/Newton-Modificado', methods=['GET'])
def Newton_Modificado():
    return render_template('unidad_dos/Newton_modificado.html')

@app.route('/metodos/directos/abiertos/Newton-Modificado', methods=['POST'])
def calcular_newton_modificado():
    json_data = request.json
    respuesta = metodo_newton_modificado.calcular_newton_modificado(json_data)
    return respuesta

@app.route('/metodos/directos/abiertos/punto-Fijo', methods=['GET'])
def Punto_fijo():
    return render_template('unidad_dos/Punto_fijo.html')

@app.route('/metodos/directos/abiertos/punto-Fijo', methods=['POST'])
def calcular_punto_fijo():
    json_data = request.json
    respuesta = metodo_punto_fijo.calcular_punto_fijo(json_data)
    return respuesta    

@app.route('/metodos/directos/abiertos/Secante', methods=['GET'])
def Secante():
    return render_template('unidad_dos/Secante.html')

@app.route('/metodos/directos/abiertos/Secante', methods=['POST'])
def calcular_secante():
    json_data = request.json
    respuesta = metodo_secante.calcular_secante(json_data)
    return respuesta

#metodos iterativos polinomicos

@app.route('/metodos/iterativos/polinomicos/bairstow', methods=['GET'])
def Bairstow():
    return render_template('unidad_dos/Bairstow.html')

@app.route('/metodos/iterativos/polinomicos/Bairstow', methods=['POST'])
def calcular_bairstow():
    json_data = request.json
    respuesta = metodo_bairstow.calcular_bairstow(json_data)
    return respuesta

@app.route('/metodos/iterativos/polinomicos/horner', methods=['POST'])
def calcular_horner():
    json_data = request.json
    respuesta = metodo_horner.calcular_Horner(json_data)
    return respuesta

@app.route('/metodos/iterativos/polinomicos/horner', methods=['GET'])
def Horner():
    return render_template('unidad_dos/Horner.html')

@app.route('/metodos/iterativos/polinomicos/muller', methods=['POST'])
def calcular_muller():
    json_data = request.json
    respuesta = metodo_muller.calcular_Muller(json_data)
    return respuesta

@app.route('/metodos/iterativos/polinomicos/muller', methods=['GET'])
def Muller():
    return render_template('unidad_dos/Muller.html')

#metodos directos

@app.route('/metodos/directos/gradomenos2/lineal', methods=['GET'])
def renderizar_lineal():
    return render_template('unidad_dos/Lineal.html')

@app.route('/metodos/directos/gradomenos2/lineal', methods=['POST'])
def calcular_lineal():
    json_data = request.json
    respuesta = metodo_lineal.calcular_lineal(json_data)
    return respuesta

@app.route('/metodos/directos/gradomenos2/cuartica', methods=['GET'])
def renderizar_cuartica():
    return render_template('unidad_dos/Cuadratica.html')

@app.route('/metodos/directos/gradomenos2/cuartica', methods=['POST'])
def calcular_cuartica():
    json_data = request.json
    respuesta = metodo_cuadratico.calcular_cuadratico(json_data)
    return respuesta

@app.route('/metodos/directos/gradomas3/Ferrari', methods=['GET'])
def renderizar_ferrari():
    return render_template('unidad_dos/Ferrari.html')

@app.route('/metodos/directos/gradomas3/Ferrari', methods=['POST'])
def calcular_ferrari():
    json_data = request.json
    respuesta = metodo_ferrari.calcular_ferrari(json_data)
    return respuesta

@app.route('/metodos/directos/gradomas3/Tartaglia', methods=['GET'])
def renderizar_tartaglia():
    return render_template('unidad_dos/Tartaglia.html')

@app.route('/metodos/directos/gradomas3/Tartaglia', methods=['POST'])
def calcular_tartaglia():
    json_data = request.json
    respuesta = metodo_tartaglia.calcular_tartaglia(json_data)
    return respuesta
    
#metodos de interpolacion

@app.route('/metodos/interpolacion/lagrange', methods=['POST'])
def calcular_lagrange():
    json_data = request.json
    respuesta = metodo_lagrange.calcular_lagrange(json_data)
    return respuesta

@app.route('/metodos/interpolacion/lagrange', methods=['GET'])
def Interpolacion_Lagrange():
    return render_template('unidad_tres/Interpolacion_Lagrange.html')

@app.route('/metodos/interpolacion/newton_recursivo', methods=['POST'])
def calcular_newton_recursivo():
    json_data = request.json
    respuesta = metodo_newton_recursivo.calcular_newton_recursivo(json_data)
    return respuesta

@app.route('/metodos/interpolacion/newton_recursivo', methods=['GET'])
def Newton_Recursivo():
    return render_template('unidad_tres/Interpolacion_Newton_Recursivo.html')


@app.route('/metodos/interpolacion/newton_fracciones_divididas', methods=['POST'])
def calcular_newton_fracciones_divididas():
    json_data = request.json
    respuesta = metodo_newton_fracciones_divididas.calcular_newton_fracciones_divididas(json_data)
    return respuesta

@app.route('/metodos/interpolacion/newton_fracciones_divididas', methods=['GET'])
def Newton_Fracciones_Divididas():
    return render_template('unidad_tres/Interpolacion_Newton_Fracciones_Divididas.html')

@app.route('/metodos/interpolacion/hermite', methods=['POST'])
def calcular_hermite():
    json_data = request.json
    respuesta = metodo_hermite.calcular_hermite(json_data)
    return respuesta

@app.route('/metodos/interpolacion/hermite', methods=['GET'])
def Hermite():
    return render_template('unidad_tres/Interpolacion_Hermite.html')
 
@app.route('/metodos/interpolacion/trazadores_cubicos', methods=['GET'])
def Trazadores():
    return render_template('unidad_tres/Interpolacion_Trazadores.html')

@app.route('/metodos/interpolacion/trazadores_cubicos', methods=['POST'])
def calcular_trazadores():
    json_data = request.json
    respuesta = metodo_trazadores.calcular_trazadores(json_data)
    return respuesta

@app.route('/metodos/interpolacion/lineal', methods=['GET'])
def Interpolacion_lineal():
    return render_template('unidad_tres/Interpolacion_Lineal.html')

@app.route('/metodos/interpolacion/lineal', methods=['POST'])
def calcular_interpolacion_lineal():
    json_data = request.json
    respuesta = metodo_interpolacion_lineal.calcular_interpolacion(json_data)
    return respuesta

#metodos de diferenciacion e integracion

@app.route('/metodos/diferenciacion/derivadas', methods=['POST'])
def calcular_derivadas():
    json_data = request.json
    respuesta = metodos_diferenciacion.calcular_derivada(json_data)
    return respuesta

@app.route('/metodos/diferenciacion/derivadas', methods=['GET'])
def Diferenciacion():
    return render_template('unidad_cuatro/Diferenciacion.html')

@app.route('/metodos/diferenciacion/richardson', methods=['POST'])
def calcular_richardson():
    json_data = request.json
    respuesta = metodo_richardson.calcular_richardson(json_data)
    return respuesta

@app.route('/metodos/diferenciacion/richardson', methods=['GET'])
def Richardson():
    return render_template('unidad_cuatro/Richardson.html')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
