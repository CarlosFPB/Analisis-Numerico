from flask import jsonify
import  sympy as sp
import numpy as np
from .....extras.Funciones import errores, respuesta_json

class metodo_punto_fijo():


    @staticmethod
    def calcular_punto_fijo(json_data):
        try:
            x = sp.symbols("x")
            #instanciar respuesta json
            instancia_respuesta = respuesta_json()
            
            #obtener los valores del json
            ##f_x = sp.simplify(json_data["funcion"])
            #Verificar la funcion obtenida
            try:
                #Ecuaion de la funcion
                g_x = sp.sympify(json_data["funcion_g_x"])
                resultado = g_x.subs(x, 2)
                if resultado > 0:
                    pass
            except sp.SympifyError:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            except TypeError as e:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            
            g_prima = sp.diff(g_x)

            try:
                error_aceptado = float(json_data["tolerancia"])
                x_actual = float(json_data["xi"])
            except ValueError as e:
                resp = instancia_respuesta.responder_error("Error en los datos ingresados" + str(e))
                return jsonify(resp), 400
            
            x_anterior = 0
            iteracion = 0

            instancia_respuesta.agregar_titulo1("Punto Fijo")
            instancia_respuesta.agregar_parrafo("A continuacion se muestra la tabla de iteraciones del metodo de punto fijo, para encontrar la raiz de la funcion ingresada.")
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(['Iteracion', 'X', 'g(x)', 'Error'])

            while True:
                iteracion += 1
                g_prima_evaluada = float(g_prima.subs(x, x_actual))
                g_x_evaluada = float(g_x.subs(x, x_actual))
                x_anterior = x_actual
                x_actual = g_x_evaluada
                error_acomulado = errores.error_aproximado_porcentual(x_anterior,x_actual)
                
                instancia_respuesta.agregar_fila([iteracion, x_actual, g_x_evaluada, error_acomulado])

                if(error_acomulado < error_aceptado):
                    break
                elif abs(g_prima_evaluada) > 1:
                    print("El metodo no converge")
                    instancia_respuesta = instancia_respuesta.responder_error("El metodo no converge con los valores dados\nIntente con otros valores")
                    return jsonify(instancia_respuesta), 400
                
            #print("La raiz aproximada es: ", x_actual)
            instancia_respuesta.agregar_tabla()
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            print(e)
            resp = instancia_respuesta.responder_error("Error interno en el servidor")
            return jsonify(resp), 500

