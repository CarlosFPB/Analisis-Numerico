from flask import jsonify
import  sympy as sp
import numpy as np
from ......extras.Funciones import errores, respuesta_json, verificaciones
from ......extras.latex import conversla, conversla_html

class metodo_punto_fijo():


    @staticmethod
    def calcular_punto_fijo(json_data):
        
        x = sp.symbols("x")
        # instanciar respuesta json
        instancia_respuesta = respuesta_json()

        # obtener los valores del json
        ## f_x = sp.simplify(json_data["funcion"])
        # Verificar la funcion obtenida
        try:
            # Ecuaion de la funcion
            g_x = conversla.latex_(json_data["latex"])
            resultado = g_x.subs(x, 2)
            if resultado > 0:
                pass
        except sp.SympifyError:
            resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
            return jsonify(resp), 400
        except TypeError as e:
            resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
            return jsonify(resp), 400

        # verificar que sea grado mayor a 0
        if verificaciones.obtener_grado(g_x) != None:  # es porq es polinomica sino no importa el grado
            if verificaciones.obtener_grado(g_x) < 2:
                resp = instancia_respuesta.responder_error("La función debe ser de grado 2 o mayor")
                return jsonify(resp), 400
        # verificar que tenga raices reales
        if verificaciones.posee_raices_reales(g_x) == False:
            resp = instancia_respuesta.responder_error(
            "La función no tiene raices reales por tanto no se puede aplicar el metodo de punto fijo")
            return jsonify(resp), 400

        try:
            error_aceptado = float(json_data["tolerancia"])
            x_actual = float(json_data["xi"])
        except ValueError as e:
            resp = instancia_respuesta.responder_error("Error en los datos ingresados" + str(e))
            return jsonify(resp), 400
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en los datos ingresados" + str(e))
            return jsonify(resp), 400
            
        try:
            g_prima = sp.diff(g_x)
            x_anterior = 0
            iteracion = 0

            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_titulo1("Valores Iniciales")
            fx1 = conversla_html.mathl_(g_x)
            instancia_respuesta.agregar_parrafo(f"Funcion: {fx1}")
            instancia_respuesta.agregar_clave_valor("Xi:",x_actual)
            instancia_respuesta.agregar_clave_valor("Tolerancia:",error_aceptado)
            instancia_respuesta.agregar_titulo1("El calculo de la raiz se hace por la siguiente formula: ")
            html_conten = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><msub><mi>X</mi><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><mi>g</mi><mrow><mo fence="true" form="prefix">(</mo><msub><mi>X</mi><mi>n</mi></msub><mo fence="true" form="postfix">)</mo></mrow></mrow></math>"""
            instancia_respuesta.agregar_parrafo(f"Formula: {html_conten}")
            html_conten = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>X</mi><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><mi>{float(g_x.subs(x, x_actual))}</mi></math>"""
            instancia_respuesta.agregar_parrafo(f"Iteración 1: {html_conten}")
            instancia_respuesta.agregar_parrafo(f"Derivada de La función: {conversla_html.mathl_(g_prima)}")
            instancia_respuesta.agregar_parrafo(f"Convergencia: {float(g_prima.subs(x, x_actual))} < 1")
            instancia_respuesta.agregar_fila(['Iteracion', 'X', 'g(x)', 'g\'(x)', 'Error'])

            while True:
                iteracion += 1
                g_prima_evaluada = float(g_prima.subs(x, x_actual))
                g_x_evaluada = float(g_x.subs(x, x_actual))
                x_anterior = x_actual
                x_actual = g_x_evaluada
                x_actual = sp.N(x_actual)
                if x_actual == 0:
                    instancia_respuesta.agregar_parrafo(f"El valor calculado de x es 0, en la iteracion #{iteracion}, por lo tanto no se puede realizar el calculo del error acomulado")
                    instancia_respuesta.agregar_fila([iteracion, x_anterior, g_x_evaluada,g_prima_evaluada, "Error no calculado"])
                    instancia_respuesta.agregar_titulo1("Se muestra la tabla de iteraciones")
                    instancia_respuesta.agregar_tabla()
                    resp= instancia_respuesta.obtener_y_limpiar_respuesta()
                    return jsonify(resp), 200
                error_acomulado = errores.error_aproximado_porcentual(x_anterior,x_actual)
                error_acomulado = sp.N(error_acomulado)
                instancia_respuesta.agregar_fila([iteracion, x_actual, g_x_evaluada,g_prima_evaluada, error_acomulado])
                if(error_acomulado < error_aceptado):
                    break
                elif abs(g_prima_evaluada) > 1:
                    print("El metodo no converge")
                    resp = instancia_respuesta.responder_error("El metodo no converge con los valores dados\nIntente con otros valores")
                    return jsonify(resp), 400
                
            instancia_respuesta.agregar_tabla()
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            print(e)
            resp = instancia_respuesta.responder_error("Error interno en el servidor")
            return jsonify(resp), 500

