from flask import Blueprint, render_template, request
import os
import time


#interpolacion
from modelos.unidad_tres.interpolacion.lagrange.Lagrange import metodo_lagrange
from modelos.unidad_tres.interpolacion.newton_recursivo.Newton_recursivo import metodo_newton_recursivo
from modelos.unidad_tres.interpolacion.newton_fracciones_divididas.Newton_fracciones_divididas import metodo_newton_fracciones_divididas
from modelos.unidad_tres.interpolacion.hermite.Hermite import metodo_hermite
from modelos.unidad_tres.interpolacion.trazadores_cubicos.Trazadores import metodo_trazadores
from modelos.unidad_tres.interpolacion.interpolacion_lineal.Interpolacion_lineal import metodo_interpolacion_lineal


# Crear un Blueprint
U3 = Blueprint('U3', __name__)


#metodos de interpolacion

@U3.route('/metodos/interpolacion/lagrange', methods=['POST'])
def calcular_lagrange():
    json_data = request.json
    respuesta = metodo_lagrange.calcular_lagrange(json_data)
    return respuesta

@U3.route('/metodos/interpolacion/lagrange', methods=['GET'])
def Interpolacion_Lagrange():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_tres/Interpolacion_Lagrange.html', keyboard_content=keyboard_content, time=time.time())

@U3.route('/metodos/interpolacion/newton_recursivo', methods=['POST'])
def calcular_newton_recursivo():
    json_data = request.json
    respuesta = metodo_newton_recursivo.calcular_newton_recursivo(json_data)
    return respuesta

@U3.route('/metodos/interpolacion/newton_recursivo', methods=['GET'])
def Newton_Recursivo():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_tres/Interpolacion_Newton_Recursivo.html', keyboard_content=keyboard_content, time=time.time())


@U3.route('/metodos/interpolacion/newton_fracciones_divididas', methods=['POST'])
def calcular_newton_fracciones_divididas():
    json_data = request.json
    respuesta = metodo_newton_fracciones_divididas.calcular_newton_fracciones_divididas(json_data)
    return respuesta

@U3.route('/metodos/interpolacion/newton_fracciones_divididas', methods=['GET'])
def Newton_Fracciones_Divididas():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_tres/Interpolacion_Newton_Fracciones_Divididas.html', keyboard_content=keyboard_content, time=time.time())

@U3.route('/metodos/interpolacion/hermite', methods=['POST'])
def calcular_hermite():
    json_data = request.json
    respuesta = metodo_hermite.calcular_hermite(json_data)
    return respuesta

@U3.route('/metodos/interpolacion/hermite', methods=['GET'])
def Hermite():
    keyboard_content = render_template('KeyboardMath.html',time=time.time())
    return render_template('unidad_tres/Interpolacion_Hermite.html', keyboard_content=keyboard_content, time=time.time())
 
@U3.route('/metodos/interpolacion/trazadores_cubicos', methods=['GET'])
def Trazadores():
    return render_template('unidad_tres/Interpolacion_Trazadores.html')

@U3.route('/metodos/interpolacion/trazadores_cubicos', methods=['POST'])
def calcular_trazadores():
    json_data = request.json
    respuesta = metodo_trazadores.calcular_trazadores(json_data)
    return respuesta

@U3.route('/metodos/interpolacion/lineal', methods=['GET'])
def Interpolacion_lineal():
    return render_template('unidad_tres/Interpolacion_Lineal.html')

@U3.route('/metodos/interpolacion/lineal', methods=['POST'])
def calcular_interpolacion_lineal():
    json_data = request.json
    respuesta = metodo_interpolacion_lineal.calcular_interpolacion(json_data)
    return respuesta
