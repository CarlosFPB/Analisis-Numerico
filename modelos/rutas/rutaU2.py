from flask import Blueprint, render_template, request
import os
import time

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
from modelos.unidad_dos.solucion_ecuaciones.metodo_grafico.Graficador import graficador

# Crear un Blueprint
U2 = Blueprint('U2', __name__)

# grafico
@U2.route('/metodos/grafico', methods=['GET'])
def grafico():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Grafico.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/grafico', methods=['POST'])
def calcular_grafico():
    json_data = request.json
    respuesta = graficador.calcular_grafico(json_data)
    return respuesta



#metodos iterativos cerrados

@U2.route('/metodos/iterativos/cerrados/Biseccion', methods=['GET'])
def renderizar_biseccion():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Biseccion.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/iterativos/cerrados/Biseccion', methods=['POST'])
def calcular_biseccion():
    json_data = request.json
    respuesta = medoto_biseccion.calcular_biseccion(json_data)
    return respuesta

@U2.route('/metodos/iterativos/cerrados/Falsa_posicion', methods=['GET'])
def renderizar_falsa_posicion():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Falsa_posicion.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/iterativos/cerrados/Falsa_posicion', methods=['POST'])
def calcular_falsa_posicion():
    json_data = request.json
    respuesta = metodo_falsa_posicion.calcular_falsa_posicion(json_data)
    return respuesta

#metodos iterativos abiertos

@U2.route('/metodos/directos/abiertos/newton', methods=['GET'])
def Newton():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Newton.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/directos/abiertos/newton', methods=['POST'])
def calcular_newton():
    json_data = request.json
    respuesta = metodo_newton.calcular_newton(json_data)
    return respuesta

@U2.route('/metodos/directos/abiertos/Newton-Modificado', methods=['GET'])
def Newton_Modificado():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Newton_modificado.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/directos/abiertos/Newton-Modificado', methods=['POST'])
def calcular_newton_modificado():
    json_data = request.json
    respuesta = metodo_newton_modificado.calcular_newton_modificado(json_data)
    return respuesta

@U2.route('/metodos/directos/abiertos/punto-Fijo', methods=['GET'])
def Punto_fijo():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Punto_fijo.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/directos/abiertos/punto-Fijo', methods=['POST'])
def calcular_punto_fijo():
    json_data = request.json
    respuesta = metodo_punto_fijo.calcular_punto_fijo(json_data)
    return respuesta    

@U2.route('/metodos/directos/abiertos/Secante', methods=['GET'])
def Secante():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Secante.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/directos/abiertos/Secante', methods=['POST'])
def calcular_secante():
    json_data = request.json
    respuesta = metodo_secante.calcular_secante(json_data)
    return respuesta

#metodos iterativos polinomicos

@U2.route('/metodos/iterativos/polinomicos/bairstow', methods=['GET'])
def Bairstow():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Bairstow.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/iterativos/polinomicos/Bairstow', methods=['POST'])
def calcular_bairstow():
    json_data = request.json
    respuesta = metodo_bairstow.calcular_bairstow(json_data)
    return respuesta

@U2.route('/metodos/iterativos/polinomicos/horner', methods=['POST'])
def calcular_horner():
    json_data = request.json
    respuesta = metodo_horner.calcular_Horner(json_data)
    return respuesta

@U2.route('/metodos/iterativos/polinomicos/horner', methods=['GET'])
def Horner():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Horner.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/iterativos/polinomicos/muller', methods=['POST'])
def calcular_muller():
    json_data = request.json
    respuesta = metodo_muller.calcular_Muller(json_data)
    return respuesta

@U2.route('/metodos/iterativos/polinomicos/muller', methods=['GET'])
def Muller():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Muller.html', keyboard_content=keyboard_content, time=time.time())

#metodos directos

@U2.route('/metodos/directos/gradomenos2/lineal', methods=['GET'])
def renderizar_lineal():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Lineal.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/directos/gradomenos2/lineal', methods=['POST'])
def calcular_lineal():
    json_data = request.json
    respuesta = metodo_lineal.calcular_lineal(json_data)
    return respuesta

@U2.route('/metodos/directos/gradomenos2/cuartica', methods=['GET'])
def renderizar_cuartica():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Cuadratica.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/directos/gradomenos2/cuartica', methods=['POST'])
def calcular_cuartica():
    json_data = request.json
    respuesta = metodo_cuadratico.calcular_cuadratico(json_data)
    return respuesta

@U2.route('/metodos/directos/gradomas3/Ferrari', methods=['GET'])
def renderizar_ferrari():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Ferrari.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/directos/gradomas3/Ferrari', methods=['POST'])
def calcular_ferrari():
    json_data = request.json
    respuesta = metodo_ferrari.calcular_ferrari(json_data)
    return respuesta

@U2.route('/metodos/directos/gradomas3/Tartaglia', methods=['GET'])
def renderizar_tartaglia():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_dos/Tartaglia.html', keyboard_content=keyboard_content, time=time.time())

@U2.route('/metodos/directos/gradomas3/Tartaglia', methods=['POST'])
def calcular_tartaglia():
    json_data = request.json
    respuesta = metodo_tartaglia.calcular_tartaglia(json_data)
    return respuesta
