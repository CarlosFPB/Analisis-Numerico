
from flask import jsonify
import sympy as sp
import numpy as np
from ....extras.Funciones import respuesta_json, verificaciones
from ....extras.latex import conversla, conversla_html
from ....extras.Integrales import integr_obtener


class simpson_adaptativo():
    @staticmethod
    def calcular_simpson_adaptativo(json_data):
        try:
            instancia_respuesta = respuesta_json()
        
             # Obtener integral
            try:
                f_x = conversla.latex_(json_data["latex"])
                nivel = int(json_data["nivel"])
            except sp.SympifyError:
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400
            except TypeError as e:
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400  
            except:
                resp = instancia_respuesta.responder_error("No se ingreso una integral")
                return jsonify(resp), 400
           
            try:
                funcion, variables, limites = integr_obtener.integr_Obtener(f_x)
            except ValueError as e:
                resp = instancia_respuesta.responder_error("La integral tiene que ser definida (contener limites)")
                return jsonify(resp), 400
            except NameError as e:
                resp = instancia_respuesta.responder_error("No se permiten caracteres especiales")
                return jsonify(resp), 400
            except Exception as e:
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400
            

            #metodo simpson adaptativo


        except Exception as e:
                resp = instancia_respuesta.responder_error(f"Error interno en el servidor" )
                return jsonify(resp), 500
        
    @staticmethod
    def recursivo_simpson(f, a, b, epsilon):
        h = b - a
        c = (a + b) / 2
        s_ab = h * (f(a) + 4 * f(c) + f(b)) / 6
        
        # División en dos subintervalos
        d = (a + c) / 2
        e = (c + b) / 2
        s_ac = (c - a) * (f(a) + 4 * f(d) + f(c)) / 6
        s_cb = (b - c) * (f(c) + 4 * f(e) + f(b)) / 6
        
        if abs(s_ac + s_cb - s_ab) < 15 * epsilon:
            print("Resultado")
            return s_ac + s_cb + (s_ac + s_cb - s_ab) / 15
            
        else:
            print("Resultado:")
                        #Simpson izquierdo          Simpson derecho
            return recursivo_simpson(f, a, c, epsilon/2) + recursivo_simpson(f, c, b, epsilon/2)

