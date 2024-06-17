import traceback

from flask import jsonify
import sympy as sp
import numpy as np
from ....extras.Funciones import respuesta_json, verificaciones
from ....extras.latex import conversla, conversla_html

class metodo_trapecio:
    @staticmethod
    def calcular_trapecio(*args):
        instancia_respuesta = respuesta_json()
        try:
            # Obtener integral
            try:
                f_x = conversla.latex_(args[0])
            except sp.SympifyError:
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400
            except TypeError as e:
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400

            # En base a la cantidad de argumentos se va a elegir si es simple o compuesto
            try:
                funcion, variables, limites = integr_obtener.integr_Obtener(f_x)
            except ValueError as e:
                resp = instancia_respuesta.responder_error("La integral tiene que ser definida (contener limites)")
                return jsonify(resp), 400
            except NameError as e:
                traceback.print_exc()
                resp = instancia_respuesta.responder_error("No se permiten caracteres especiales")
                return jsonify(resp), 400
            except Exception as e:
                traceback.print_exc()
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400

            cantidad = len(args)
            if cantidad == 2:  # compuesto
                return metodo_trapecio.trapecio_compuesto(funcion, limites, variables, args[1])
            else:  # simple, tener en cuenta que solo tiene que ser integral unidimensional
                if len(variables) > 1:
                    resp = instancia_respuesta.responder_error("La integral debe ser unidimensional")
                    return jsonify(resp), 400
                resp = metodo_trapecio.trapecio_simple(funcion, variables, limites, f_x)
                return jsonify(resp), 200

        except Exception as e:
            traceback.print_exc()
            print(e)
            resp = instancia_respuesta.responder_error(f"Error interno en el servidor" )
            return jsonify(resp), 500

    @staticmethod
    def trapecio_simple(funcion, variables, limites, f_x):
        instancia_respuesta = respuesta_json()
        I = (limites[1] - limites[0]) * ((funcion.subs(variables[0], limites[0]) + funcion.subs(variables[0], limites[1])) / 2)
        I = (I).evalf()
        print("Resultado I: ", I)
        print("Tipo: ", type(I))
        instancia_respuesta.crear_tabla()
        instancia_respuesta.agregar_titulo1("Trapecio Simple")
        fx1 = conversla_html.mathl_(f_x)
        instancia_respuesta.agregar_parrafo(f"Integral: {fx1}")
        instancia_respuesta.agregar_clave_valor("Respuesta: ", I)
        instancia_respuesta.agregar_tabla()
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return resp

    @staticmethod
    def trapecio_compuesto(funcion, limites, variables, intervalos):
        instancia_respuesta = respuesta_json()
        tabla_datos = np.array([])
        for variable in variables:
            count_a = 0
            count_b = 1
            h = (limites[count_b] - limites[count_a]) / intervalos
            xi = limites[count_a]
            for i in range(intervalos + 1):
                tabla_datos = np.append(tabla_datos, [xi, funcion.subs(variable, xi)])
                xi += h
            suma_intermedios = 0
            for u in range(intervalos):
                if u == 0:
                    continue
                else:
                    suma_intermedios += tabla_datos[u, 1]
            I = ((limites[count_b] - limites[count_a]) * (tabla_datos[0, 1] + 2 * suma_intermedios + tabla_datos[intervalos, 1])) / (2 * intervalos)
            count_a += 2
            count_b += 2
            funcion = I

        I = float(I)
        print("Resultado I: ", I)
        print("Tipo: ", type(I))
        instancia_respuesta.crear_tabla()
        instancia_respuesta.agregar_titulo1("Trapecio Compuesto")
        instancia_respuesta.agregar_clave_valor("Respuesta: ", I)
        instancia_respuesta.agregar_tabla()
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return jsonify(resp), 200
