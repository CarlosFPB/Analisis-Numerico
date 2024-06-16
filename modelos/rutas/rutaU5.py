from flask import Blueprint, render_template, request
import os
import time

#metodos multipasos
from modelos.unidad_cinco.multipasos.Multipasos import metodo_multipasos
from modelos.unidad_cinco.iterativos.Runge_kutta import metodo_runge_kutta
from modelos.unidad_cinco.iterativos.Euler import metodo_euler
from modelos.unidad_cinco.iterativos.Taylor import metodo_taylor

# Crear un Blueprint
U5 = Blueprint('U5', __name__)

#metodos unidad 5
@U5.route('/metodos/unidad_cinco/iterativos/multipasos', methods=['POST'])
def calcular_multipasos():
    json_data = request.json
    respuesta = metodo_multipasos.calcular_multipasos(json_data)
    return respuesta

@U5.route('/metodos/unidad_cinco/iterativos/multipasos', methods=['GET'])
def Multipasos():
    return render_template('unidad_cinco/Multipasos.html')

@U5.route('/metodos/unidad_cinco/iterativos/Runge_kutta', methods=['POST'])
def calcular_runge_kutta():
    json_data = request.json
    respuesta = metodo_runge_kutta.calcular_metodo_runge_kutta(json_data)
    return respuesta

@U5.route('/metodos/unidad_cinco/iterativos/Runge_kutta', methods=['GET'])
def Runge_kutta():
    return render_template('unidad_cinco/Runge_kutta.html')

@U5.route('/metodos/unidad_cinco/iterativos/euler', methods=['POST'])
def calcular_euler():
    json_data = request.json
    respuesta = metodo_euler.calcular_euler(json_data)
    return respuesta

@U5.route('/metodos/unidad_cinco/iterativos/euler', methods=['GET'])
def Euler():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_cinco/Euler.html', keyboard_content=keyboard_content, time=time.time())


@U5.route('/metodos/unidad_cinco/iterativos/taylor', methods=['POST'])
def calcular_taylor():
    json_data = request.json
    respuesta = metodo_taylor.calcular_taylor(json_data)
    return respuesta

@U5.route('/metodos/unidad_cinco/iterativos/taylor', methods=['GET'])
def Taylor():
    return render_template('unidad_cinco/Taylor.html')