
from flask import jsonify
import sympy as sp
from ....extras.Funciones import respuesta_json
from ....extras.latex import conversla, conversla_html
from ....extras.Integrales import integr_obtener, cuadratura_gaussiana_formula

class cuadratura_gaussiana():
    @staticmethod
    def calcular_cuadratura_gaussiana(json_data):
        try:
            instancia_respuesta = respuesta_json()
            #obtener integral y numero de puntos de la cuadratura gaussiana
            try:
                f_x = conversla.latex_(json_data["latex"])
                puntos = int(json_data["puntos"])
                
                print("Puntos",type(puntos))
            except sp.SympifyError:
                 resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                 return jsonify(resp), 400
            except TypeError as e:
                 resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                 return jsonify(resp), 400
            except:
                resp = instancia_respuesta.responder_error("No se ingreso una integral")
                return jsonify(resp), 400
            #Obtener funcion pura, limites y variables
            try:
                funcion, variables, limites = integr_obtener.integr_Obtener(f_x)
                if len(variables) > 1 or len(limites) > 2:
                    resp = instancia_respuesta.responder_error("Solo se permiten integrales unidimensionales")
                    return jsonify(resp), 400
            except ValueError as e:
                resp = instancia_respuesta.responder_error("La integral tiene que ser definida (contener limites)")
                return jsonify(resp), 400
            except NameError as e:
                resp = instancia_respuesta.responder_error("No se permiten caracteres especiales")
                return jsonify(resp), 400
            except Exception as e:
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400

            #codigo de cuadratura gaussiana
            instancia_respuesta.agregar_titulo1("Metodo Cuadratura gaussiana")
            fx1 = conversla_html.mathl_(f_x)
            instancia_respuesta.agregar_parrafo(f"Integral: {fx1}")
            instancia_respuesta.agregar_titulo1("Formula")
            html_conten = """<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><munderover accent='false' accentunder='false'><mo>&#x222b;</mo><mrow><mi>z</mi><mi>a</mi></mrow><mrow><mi>z</mi><mi>b</mi></mrow></munderover><mi>w</mi><mo>(</mo><mi>z</mi><mo>)</mo><mi>f</mi><mo>(</mo><mi>z</mi><mo>)</mo><mi>d</mi><mi>z</mi></math>"""
            instancia_respuesta.agregar_parrafo(f"{html_conten}")
            html_conten = """<math xmlns="http://www.w3.org/1998/Math/MathML"><munderover accent='false' accentunder='false'><mo>&#x222b;</mo><mi>a</mi><mi>b</mi></munderover><mi>f</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mi lspace="0.2em" rspace="0">d</mi><mi>x</mi><mo>=</mo><mfrac><mrow><mo>(</mo><mi>b</mi><mo>-</mo><mi>a</mi><mo>)</mo></mrow><mn>2</mn></mfrac><munderover accent='false' accentunder='false'><mo>&#x2211;</mo><mrow><mi>k</mi><mo>=</mo><mn>0</mn></mrow><mi>n</mi></munderover><msub><mi>W</mi><mi>k</mi></msub><mi>f</mi><mo>(</mo><mfrac><mrow><mo>(</mo><mi>b</mi><mo>-</mo><mi>a</mi><mo>)</mo><msub><mi>t</mi><mi>k</mi></msub><mo>+</mo><mo>(</mo><mi>b</mi><mo>-</mo><mi>a</mi><mo>)</mo></mrow><mn>2</mn></mfrac><mo>)</mo></math>"""
            instancia_respuesta.agregar_parrafo(f"{html_conten}")
            count_a = 0
            count_b = 1
            integral = 0
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(["w(z)f(z)"])
            for j in range(puntos):
                I = cuadratura_gaussiana_formula.cuadratura_gaussiana(j, limites[count_a], limites[count_b], funcion, variables[0], puntos)
                instancia_respuesta.agregar_fila([I])
                integral += I   
            instancia_respuesta.agregar_titulo1("Datos")
            instancia_respuesta.agregar_tabla()
            instancia_respuesta.agregar_parrafo(f"Sumatoria w(z)f(z) = {integral}")
            instancia_respuesta.agregar_parrafo(f"I = {limites[count_b]} - {limites[count_a]} / 2 * {integral} = {((limites[count_b]-limites[count_a])/2)*integral}")
            integral = ((limites[count_b]-limites[count_a])/2)*integral
            count_a += 2
            count_b += 2
            integral = sp.N(integral)
            
            instancia_respuesta.agregar_clave_valor_segundo("Respuesta: ", integral)
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200

        except Exception as e:
                resp = instancia_respuesta.responder_error(f"Error interno en el servidor" )
                return jsonify(resp), 500
    
