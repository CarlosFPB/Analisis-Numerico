
from flask import jsonify
import sympy as sp
import numpy as np
from ....extras.Funciones import respuesta_json, verificaciones
from ....extras.latex import conversla, conversla_html
from ....extras.Integrales import integr_obtener

class metodo_Rosemberg():
    @staticmethod
    def calcular_Rosemberg(json_data):
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
            if len(variables) > 1:
                resp = instancia_respuesta.responder_error("La integral debe ser unidimensional")
                return jsonify(resp), 400
            #Metodo de Rosemberg
            instancia_respuesta.agregar_titulo1("Metodo Rosemberg")
            fx1 = conversla_html.mathl_(f_x)
            instancia_respuesta.agregar_parrafo(f"Integral: {fx1}")
            instancia_respuesta.agregar_titulo1("Formula")
            html_content = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mrow><mo>(</mo><mfrac><mrow><mi>b</mi><mo>-</mo><mi>a</mi></mrow><mrow><msup><mn>2</mn><mi>n</mi></msup></mrow></mfrac><mo>)</mo></mrow><mo>(</mo><mi>f</mi><mrow><mo>(</mo><mrow><msub><mi>x</mi><mn>0</mn></msub></mrow><mo>)</mo></mrow><mo>+</mo><mn>2</mn><munderover accent='false' accentunder='false'><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>n</mi><mo>-</mo><mn>1</mn></mrow></munderover><mi>f</mi><mo>(</mo><msub><mi>x</mi><mi>i</mi></msub><mo>)</mo><mo>+</mo><mi>f</mi><mrow><mo>(</mo><mrow><msub><mi>x</mi><mi>n</mi></msub></mrow><mo>)</mo></mrow><mo>)</mo></math>"""
            instancia_respuesta.agregar_parrafo(f"Formula Trapecio: {html_content}")
            html_content = """<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>(</mo><mi>k</mi><mo>+</mo><mn>1</mn><mo>,</mo><mo>&#xA0;</mo><mi>i</mi><mo>)</mo><mo>=</mo><mfrac><mrow><msup><mn>4</mn><mi>k</mi></msup><mi>I</mi><mo>(</mo><mi>k</mi><mo>-</mo><mn>1</mn><mo>,</mo><mo>&#xA0;</mo><mi>i</mi><mo>+</mo><mn>1</mn><mo>)</mo><mo>-</mo><mi>I</mi><mo>(</mo><mi>k</mi><mo>-</mo><mn>1</mn><mo>,</mo><mo>&#xA0;</mo><mi>i</mi><mo>)</mo></mrow><mrow><msup><mn>4</mn><mi>k</mi></msup><mo>-</mo><mn>1</mn></mrow></mfrac></math>"""
            instancia_respuesta.agregar_parrafo(f"Extrapolación de Richardson: {html_content}")
            instancia_respuesta.agregar_titulo1("Datos")
            integrales=[]
            for i in range(1, nivel+1):
                if i == 1:
                    for j in range(1, nivel+1):
                        integral = metodo_Rosemberg.calcular_Trapecio(funcion, limites[0], limites[1], j, variables[0])
                        integrales.append([integral])  
                else:
                    for j in range(1, nivel - i + 2):
                        primer = (4**(i-1))/(4**(i-1)-1)
                        valor1 = integrales[j][i-2]
                        segundo = 1/(4**(i-1)-1)
                        valor2 = integrales[j-1][i-2]
                        valor = primer * valor1 - segundo * valor2
                        integrales[j-1].append(valor) 
                        instancia_respuesta.agregar_parrafo(f"I{i, j} = {valor}")
                        
            instancia_respuesta.crear_tabla()   
            array_titulo = []
            for j in range (1, nivel+1):
                array_titulo.append(f"Nivel {j}")
            instancia_respuesta.agregar_fila(array_titulo)
            for filas in integrales:
                instancia_respuesta.agregar_fila(filas)
            instancia_respuesta.agregar_clave_valor_segundo("Resultado: ",integrales[0][-1])
            #instancia_respuesta.agregar_clave_valor("Respuesta: ", I)
            instancia_respuesta.agregar_tabla()
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200

        except Exception as e:
                resp = instancia_respuesta.responder_error(f"Error interno en el servidor" )
                return jsonify(resp), 500
   
    @staticmethod
    def calcular_Trapecio(f_x, a, b, n, variable):
        
        intervalos = int((2**n)/2)
        # Calculo de h
        h = (b - a) / intervalos
        #Calculo de los puntos
        matriz_puntos = []
        for i in range(intervalos + 1):
            punto = a + i * h
            matriz_puntos.append([punto, f_x.subs(variable, punto)])
        suma_interna = sum([i[1] for i in matriz_puntos[1:-1]])
        integral = (matriz_puntos[-1][0] - matriz_puntos[0][0]) * (matriz_puntos[0][1] + (2 * suma_interna) + matriz_puntos[-1][1]) / (2 ** n)
        return float(integral)