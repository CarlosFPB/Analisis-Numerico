from flask import Blueprint, render_template, request
import os
import time

#diferenciacion e integracion
from modelos.unidad_cuatro.diferenciacion.derivadas.Diferenciacion import metodos_diferenciacion
from modelos.unidad_cuatro.diferenciacion.richardson.Richardson import metodo_richardson

#integracion
from modelos.unidad_cuatro.Integracion.Integracion import integracion_

# Crear un Blueprint
U4 = Blueprint('U4', __name__)



#metodos de diferenciacion e integracion

@U4.route('/metodos/diferenciacion/derivadas', methods=['POST'])
def calcular_derivadas():
    json_data = request.json
    respuesta = metodos_diferenciacion.calcular_derivada(json_data)
    return respuesta

@U4.route('/metodos/diferenciacion/derivadas', methods=['GET'])
def Diferenciacion():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_cuatro/Diferenciacion.html', keyboard_content=keyboard_content, time=time.time())


@U4.route('/metodos/diferenciacion/richardson', methods=['POST'])
def calcular_richardson():
    json_data = request.json
    respuesta = metodo_richardson.calcular_richardson(json_data)
    return respuesta

@U4.route('/metodos/diferenciacion/richardson', methods=['GET'])
def Richardson():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_cuatro/Richardson.html', keyboard_content=keyboard_content, time=time.time())


 #integracion

@U4.route('/metodos/integracion/trapecio-simpson', methods =['POST'])
def calcular_integracion():
    json_data = request.json
    respuesta = integracion_.calcular_integracion(json_data)
    return respuesta

@U4.route('/metodos/integracion/trapecio-simpson', methods = ['GET'])
def Integracion():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_cuatro/Trapecio_Simpson.html', keyboard_content=keyboard_content, time=time.time())