from flask import jsonify
import sympy as sp
import numpy as np
from ....extras.Funciones import respuesta_json, verificaciones
from ....extras.latex import conversla, conversla_html
from ....extras.Integrales import integr_obtener, metodod_boyle

class metodo_boyle():
    @staticmethod
    def calcular_boyle(json_data):
        try:
            instancia_respuesta = respuesta_json()
             # Obtener integral
            try:
                f_x = conversla.latex_(json_data["latex"])
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
           
            #Metodo de boyle si resuelve integrales multiples
            instancia_respuesta.agregar_titulo1("Metodo de Boyle")
            fx1 = conversla_html.mathl_(f_x)
            instancia_respuesta.agregar_parrafo(f"Integral: {fx1}")
            instancia_respuesta.agregar_titulo1("Formula")
            html_conten = """<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mo>(</mo><mfrac><mrow><mn>2</mn><mi>h</mi></mrow><mn>45</mn></mfrac><mo>)</mo><mo>[</mo><mn>7</mn><mi>f</mi><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>+</mo><mn>32</mn><mi>f</mi><mo>(</mo><msub><mi>x</mi><mn>1</mn></msub><mo>)</mo><mo>+</mo><mn>12</mn><mi>f</mi><mo>(</mo><msub><mi>x</mi><mn>2</mn></msub><mo>)</mo><mo>+</mo><mn>32</mn><mi>f</mi><mo>(</mo><msub><mi>x</mi><mn>3</mn></msub><mo>)</mo><mo>+</mo><mn>7</mn><mi>f</mi><mo>(</mo><msub><mi>x</mi><mn>4</mn></msub><mo>)</mo><mo>]</mo></math>"""
            instancia_respuesta.agregar_parrafo(f"{html_conten}")
            html_conten = """<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>h</mi><mo>=</mo><mfrac><mrow><mi>b</mi><mo>-</mo><mi>a</mi></mrow><mn>4</mn></mfrac></math>"""
            instancia_respuesta.agregar_parrafo(f"{html_conten}")
            instancia_respuesta.agregar_titulo1("Datos")
           
            count_a = 0
            count_b = 1
            for variable in variables:
                tabla_datos = []
                h = (limites[count_b] - limites[count_a]) / 4
                valor = limites[count_a]
                instancia_respuesta.crear_tabla()
                instancia_respuesta.agregar_fila(["Xn", "f(Xn)"])
                for j in range(1, 6):
                    eval = funcion.subs(variable, valor)
                    tabla_datos.append([valor, eval])
                    instancia_respuesta.agregar_fila([valor, sp.N(eval)])
                    valor = limites[count_a] + (h*j)
                instancia_respuesta.agregar_tabla()
                I = metodod_boyle.boyle(h, tabla_datos[0][1], tabla_datos[1][1], tabla_datos[2][1], tabla_datos[3][1], tabla_datos[4][1])
                
                count_a += 2
                count_b += 2
                funcion = I
                instancia_respuesta.agregar_parrafo(f"Resultado integral: {I}")
            instancia_respuesta.agregar_clave_valor_segundo("Respuesta: ", I)
            res = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(res),200
        except Exception as e:
                resp = instancia_respuesta.responder_error(f"Error interno en el servidor" )
                return jsonify(resp), 500
