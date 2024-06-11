from flask import jsonify
import  sympy as sp
import numpy as np
from ......extras.Funciones import errores, newton_modificado, respuesta_json, verificaciones
from modelos.extras.latex import conversla

class metodo_newton_modificado():
    @staticmethod
    def calcular_newton_modificado(json_data):
        try:
            x = sp.symbols("x")
            #instanciar respuesta json
            instancia_respuesta = respuesta_json()

           #Verificar la funcion obtenida
            try:
                #Ecuaion de la funcion
                f_x = conversla.latex_(json_data["latex"])
                resultado = f_x.subs(x, 2)
                if resultado > 0:
                    pass
            except sp.SympifyError:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            except TypeError as e:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            
            #verificar que sea grado mayor a 0
            if verificaciones.obtener_grado(f_x) != None:#es porq es polinomica sino no importa el grado
                if verificaciones.obtener_grado(f_x) < 1:
                    resp = instancia_respuesta.responder_error("La función debe ser de grado 1 o mayor")
                    return jsonify(resp), 400
            
            f_prima = sp.diff(f_x)
            f_prima_prima = sp.diff(f_prima)

            try:
                x_actual = float(json_data["xi"])
                error_aceptado = float(json_data["tolerancia"])
            except ValueError as e:
                resp = instancia_respuesta.responder_error("Error en los datos ingresados" + str(e))
                return jsonify(resp), 400
            except Exception as e:
                resp = instancia_respuesta.responder_error("Error en los datos ingresados" + str(e))
                return jsonify(resp), 400
            
            x_anterior = 0
            error_acomulado = 100
            iteracion = 0


            instancia_respuesta.agregar_titulo1("Newton Modificado")
            instancia_respuesta.agregar_parrafo("asdas")
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(['Iteracion', 'X0', 'F(x0)', 'F\'(x0)', 'F\'\'(x0)', 'Xi', 'Error'])

            while True:
                iteracion += 1
                f_prima_evaluada = f_prima.subs(x, x_actual)
                f_x_evaluada = f_x.subs(x, x_actual)
                f_prima_prima_evaluada = f_prima_prima.subs(x, x_actual)
                x_anterior = x_actual
                x_actual = newton_modificado.aproximacion(f_x_evaluada, f_prima_evaluada,f_prima_prima_evaluada, x_anterior)
                x_actual = sp.N(x_actual)
                error_acomulado = errores.error_aproximado_porcentual(x_anterior,x_actual)
                error_acomulado = sp.N(error_acomulado)
                instancia_respuesta.agregar_fila([iteracion, x_anterior, f_x_evaluada, f_prima_evaluada, f_prima_prima_evaluada, x_actual, error_acomulado])
                if(error_acomulado < error_aceptado):
                    break
                #evaluar el criterio de convergencia
                f_prima_evaluada = f_prima.subs(x, x_actual)
                f_prima_prima_evaluada = f_prima_prima.subs(x, x_actual)
                f_x_evaluada = f_x.subs(x, x_actual)
                if f_prima_evaluada == 0:#evaluando que no haya divicion sobre 0
                    print("La derivada evaluada en la raiz es 0")
                    instancia_respuesta.agregar_parrafo(f"La derivada evaluada en la raiz es 0, en la iteracion #{iteracion}, por lo tanto no se puede continuar con el metodo")
                    break
                criterio = abs((f_prima_evaluada*f_prima_prima_evaluada)/(f_prima_evaluada**2))
                if criterio > 1:
                    print("El criterio de convergencia no se cumple")
                    resp = instancia_respuesta.responder_error("El criterio de convergencia no se cumple")
                    return jsonify(resp), 400
            instancia_respuesta.agregar_tabla()
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error interno del codigo" + str(e))
            return jsonify(resp), 500




