from flask import Blueprint, render_template, request
import os
import time

#diferenciacion e integracion
from modelos.unidad_cuatro.diferenciacion.derivadas.Diferenciacion import metodos_diferenciacion
from modelos.unidad_cuatro.diferenciacion.richardson.Richardson import metodo_richardson

#integracion
#integracion
from modelos.unidad_cuatro.Integracion.Integracion import integracion_
from modelos.unidad_cuatro.Integracion.Cuadratura_gaussiana.cuadratura_gaussiana import cuadratura_gaussiana
from modelos.unidad_cuatro.Integracion.Rosemberg.Rosemberg import metodo_Rosemberg
from modelos.unidad_cuatro.Integracion.Simpson_Adaptativo.simpson_adaptativo import simpson_adaptativo
from modelos.unidad_cuatro.Integracion.Boyle.Boyle import metodo_boyle

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

#Cuadratura gaussiana
@U4.route('/metodos/integracion/cuadratura-gaussiana', methods = ['POST'])
def calcular_cuadratura_gaussiana():
    json_data = request.json
    respuesta = cuadratura_gaussiana.calcular_cuadratura_gaussiana(json_data)
    return respuesta

@U4.route('/metodos/integracion/cuadratura-gaussiana', methods = ['GET'])
def cuadratura_gaussiana_re():
    keyboard_content = render_template('KeyboardMath.html', time=time.time())
    return render_template('unidad_cuatro/Cuadratura_gaussiana.html', keyboard_content=keyboard_content, time=time.time())

#Rosembergg
@U4.route('/metodos/integracion/metodo-rosemberg', methods = ['POST'])
def calcular_rosemberg():
    json_data = request.json
    respuesta = metodo_Rosemberg.calcular_Rosemberg(json_data)
    return respuesta

@U4.route('/metodos/integracion/metodo-rosemberg', methods = ['GET'])
def metodo_rosemberg():
    keyboard_content = render_template('KeyboardMath.html', time=time.time())
    return render_template('unidad_cuatro/Rosemberg.html', keyboard_content=keyboard_content, time=time.time())


#Simpson adaptativo
@U4.route('/metodos/integracion/metodo-Simpson_adaptativo', methods = ['POST'])
def calcular_simpsonAdaptativo():
    json_data = request.json
    respuesta = simpson_adaptativo.calcular_simpson_adaptativo(json_data)
    return respuesta

@U4.route('/metodos/integracion/metodo-Simpson_adaptativo', methods = ['GET'])
def metodo_simpsonAdaptativo():
    keyboard_content = render_template('KeyboardMath.html', time=time.time())
    return render_template('unidad_cuatro/Simpson_adaptativo.html', keyboard_content=keyboard_content, time=time.time())

#Metodo de boyle
@U4.route('/metodos/integracion/metodo-boyle', methods =['POST'])
def calcular_boyle():
    json_data = request.json
    respuesta = metodo_boyle.calcular_boyle(json_data)
    return respuesta

@U4.route('/metodos/integracion/metodo-boyle', methods = ['GET'])
def metodo__boyle():
    keyboard_content = render_template('KeyboardMath.html', time=time.time())
    return render_template('unidad_cuatro/boyle.html', keyboard_content=keyboard_content, time=time.time())