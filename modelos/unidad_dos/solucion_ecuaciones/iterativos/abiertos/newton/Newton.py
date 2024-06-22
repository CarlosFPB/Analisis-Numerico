from flask import jsonify
import  sympy as sp
import numpy as np
from ......extras.Funciones import errores, newton, respuesta_json, verificaciones, commprobaciones_json
from ......extras.latex import conversla, conversla_html

class metodo_newton():

    @staticmethod
    def calcular_newton(json_data):
        
        x = sp.symbols("x")
        #instanciar respuesta json
        instancia_respuesta = respuesta_json()
        
        try:
            #Verificar la funcion obtenida
            response, status_code = commprobaciones_json.comprobar_funcionX_latex(json_data, instancia_respuesta)
            if status_code != 200:
                resp = response
                return resp, 400
            f_x = response
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error al obtener la función ingresada: "+str(e))
            return jsonify(resp), 400
        
        try:
            x_actual = float(json_data["xi"])
            error_aceptado = float(json_data["tolerancia"])
        except ValueError as e:
            resp = instancia_respuesta.responder_error("Error en los datos ingresados" + str(e))
            return jsonify(resp), 400
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en los datos ingresados" + str(e))
            return jsonify(resp), 400
            
        try:
            #verificar que sea grado mayor a 0
            if verificaciones.obtener_grado(f_x) != None:#es porq es polinomica sino no importa el grado
                if verificaciones.obtener_grado(f_x) < 1:
                    resp = instancia_respuesta.responder_error("La función debe ser de grado 1 o mayor")
                    return jsonify(resp), 400
                
            f_prima = sp.diff(f_x)
            f_prima_prima = sp.diff(f_prima)
           
            x_anterior = 0
            error_acomulado = 100
            iteracion = 0

            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_titulo1("Valores Iniciales")
            fx1 = conversla_html.mathl_(f_x)
            instancia_respuesta.agregar_parrafo(f"Función: {fx1}")
            instancia_respuesta.agregar_clave_valor("Xi: ",x_actual)
            instancia_respuesta.agregar_clave_valor("Tolerancia:",error_aceptado)
            instancia_respuesta.agregar_fila(['Iteracion', 'X1', 'f(X1)', 'f\'(X1)', 'X1+1', 'Error'])
            instancia_respuesta.agregar_titulo1("El calculo de la raiz se hace por la siguiente formula: ")
            html_contetn = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>X</mi><mrow><mi>i</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><mi>X</mi><mi>i</mi><mo>-</mo><mfrac><mrow><mi>f</mi><mo>(</mo><mi>X</mi><mi>i</mi><mo>)</mo></mrow><mrow><mi>f</mi><mo>&#xb4;</mo><mo>(</mo><mi>X</mi><mi>i</mi><mo>)</mo></mrow></mfrac></math>"""
            instancia_respuesta.agregar_parrafo(f"Formula: {html_contetn}")
            html_contetn = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>X</mi><mrow><mi>i</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><mi>{x_actual}</mi><mo>-</mo><mfrac><mi>{f_x.subs(x, x_actual)}</mi><mi>{f_prima.subs(x, x_actual)}</mi></mfrac></math>"""
            instancia_respuesta.agregar_parrafo(f"Iteración 1: {html_contetn} = {newton.aproximacion(f_x.subs(x, x_actual), f_prima.subs(x, x_actual), x_actual)}")
            while True:
                iteracion += 1
                f_prima_evaluada = f_prima.subs(x, x_actual)
                f_x_evaluada = f_x.subs(x, x_actual)
                x_anterior = x_actual
                x_actual = newton.aproximacion(f_x_evaluada, f_prima_evaluada, x_anterior)
                x_actual = sp.N(x_actual)
                if x_actual == 0:
                    instancia_respuesta.agregar_parrafo(f"El valor calculado de x es 0, en la iteracion #{iteracion}, por lo tanto no se puede realizar el calculo del error acomulado")
                    instancia_respuesta.agregar_fila([iteracion, x_anterior, f_x_evaluada, f_prima_evaluada, x_actual, "Error no calculado"])
                    instancia_respuesta.agregar_titulo1("Se muestra la tabla de iteraciones")
                    instancia_respuesta.agregar_tabla()
                    resp= instancia_respuesta.obtener_y_limpiar_respuesta()
                    return jsonify(resp), 200
                error_acomulado = errores.error_aproximado_porcentual(x_anterior,x_actual)
                error_acomulado = sp.N(error_acomulado)
                instancia_respuesta.agregar_fila([iteracion, x_anterior, f_x_evaluada, f_prima_evaluada, x_actual, error_acomulado])
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
            resp= instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error interno del codigo" + str(e))
            return jsonify(resp), 500





