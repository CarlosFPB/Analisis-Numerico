
from flask import jsonify
import sympy as sp
import numpy as np
from .....extras.Funciones import respuesta_json, verificaciones
from .....extras.latex import conversla, conversla_html
from .....extras.Integrales import integr_obtener, Simpson_13

class metodo_simpson:
    @staticmethod
    def calcular_simpson13(*args):
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
            except:
                resp = instancia_respuesta.responder_error("No se ingreso una integral")
                return jsonify(resp), 400
            # En base a la cantidad de argumentos se va a elegir si es simple o compuesto
            try:
                funcion, variables, limites = integr_obtener.integr_Obtener(f_x)
            except ValueError as e:
                resp = instancia_respuesta.responder_error("La integral tiene que ser definida (contener limites)")
                return jsonify(resp), 400
            except NameError as e:
                resp = instancia_respuesta.responder_error("La integral no se ingreso correctamente o se introdujo un caracter especial")
                return jsonify(resp), 400
            except Exception as e:
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400

            cantidad = len(args)
            if cantidad == 2:  # compuesto
                res = metodo_simpson.simpson13_compuesto(funcion, limites, variables, args[1], f_x)
                return jsonify(res), 200
            else:  # simple, tener en cuenta que solo tiene que ser integral unidimensional
                if len(variables) > 1:
                    resp = instancia_respuesta.responder_error("La integral debe ser unidimensional")
                    return jsonify(resp), 400
                resp = metodo_simpson.simpson13_simple(funcion, variables, limites, f_x)
                return jsonify(resp), 200

        except Exception as e:
            print(e)
            resp = instancia_respuesta.responder_error(f"Error interno en el servidor" )
            return jsonify(resp), 500

    
    @staticmethod
    def simpson13_simple(funcion, variables, limites, f_x):
        h = (limites[1]-limites[0]) / 2
        instancia_respuesta = respuesta_json()
        fa = sp.N(funcion.subs(variables[0], limites[0]))
        fxm = sp.N(funcion.subs(variables[0], limites[0]+h))
        fb = sp.N(funcion.subs(variables[0], limites[0]+(2*h)))
        I = Simpson_13.simpson_simple(limites[0], limites[1], fa, fxm, fb)
        instancia_respuesta.crear_tabla()
        instancia_respuesta.agregar_titulo1("Simpson 1/3 Simple")
        
        fx1 = conversla_html.mathl_(f_x)
        instancia_respuesta.agregar_parrafo(f"Integral: {fx1}")
        instancia_respuesta.agregar_clave_valor("Respuesta: ", I)
        instancia_respuesta.agregar_titulo1("Formula")
        html_content = """<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mo>(</mo><mi>b</mi><mo>-</mo><mi>a</mi><mo>)</mo><mfenced open="[" close="]"><mfrac><mrow><mi>f</mi><mrow><mo>(</mo><mi>a</mi><mo>)</mo></mrow><mo>+</mo><mn>4</mn><mi>f</mi><mrow><mo>(</mo><mrow><msub><mi>x</mi><mi>m</mi></msub></mrow><mo>)</mo></mrow><mo>+</mo><mi>f</mi><mrow><mo>(</mo><mi>b</mi><mo>)</mo></mrow></mrow><mn>6</mn></mfrac></mfenced></math>"""
        instancia_respuesta.agregar_parrafo(f"Formula: {html_content}")
        html_content = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mrow><mo>(</mo><mrow><mi>{limites[1]}</mi><mo>-</mo><mi>{limites[0]}</mi></mrow><mo>)</mo></mrow><mfenced open="[" close="]"><mfrac><mrow><mi>{fa}</mi><mo>+</mo><mi>{4*fxm}</mi><mo>+</mo><mi>{fb}</mi></mrow><mn>6</mn></mfrac></mfenced></math>"""
        instancia_respuesta.agregar_parrafo(f"{html_content}")
        instancia_respuesta.agregar_parrafo(f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mi>{I}</mi></mathl>""")
        instancia_respuesta.agregar_titulo1("Datos")
        instancia_respuesta.agregar_fila(["Xi", "f(xi)"])
        instancia_respuesta.agregar_fila([limites[0], fa])
        instancia_respuesta.agregar_fila([limites[0]+h, fxm])
        instancia_respuesta.agregar_fila([limites[0]+(2*h), fb])
        instancia_respuesta.agregar_tabla()
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return resp

    @staticmethod
    def simpson13_compuesto(funcion, limites, variables, intervalos, f_x):
        instancia_respuesta = respuesta_json()

        #Respuesta con json
        instancia_respuesta.agregar_titulo1("Simpson 1/3 Compuesto")
        fx1 = conversla_html.mathl_(f_x)
        instancia_respuesta.agregar_parrafo(f"Integral: {fx1}")
        instancia_respuesta.agregar_titulo1("Formula")
        html_content = """<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mrow><mo>(</mo><mrow><mi>b</mi><mo>-</mo><mi>a</mi></mrow><mo>)</mo></mrow><mfrac><mrow><mi>f</mi><mrow><mo>(</mo><mrow><msub><mi>x</mi><mn>0</mn></msub></mrow><mo>)</mo></mrow><mo>+</mo><mn>4</mn><munderover accent='false' accentunder='false'><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>n</mi></munderover><mi>f</mi><mrow><mo>(</mo><mrow><msub><mi>x</mi><mrow><mi>m</mi><mi>i</mi></mrow></msub></mrow><mo>)</mo></mrow><mo>+</mo><mn>2</mn><munderover accent='false' accentunder='false'><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>n</mi><mo>-</mo><mn>1</mn></mrow></munderover><mi>f</mi><mfenced><mrow><msub><mi>x</mi><mi>i</mi></msub></mrow></mfenced><mo>+</mo><mi>f</mi><mrow><mo>(</mo><mrow><msub><mi>x</mi><mi>n</mi></msub></mrow><mo>)</mo></mrow></mrow><mrow><mn>6</mn><mi>n</mi></mrow></mfrac></math>"""
        instancia_respuesta.agregar_parrafo(html_content)
        instancia_respuesta.agregar_titulo1("Datos")

        count_a = 0
        count_b = 1
        for variable in variables:
            tabla_datos = []
            tabla_datos_subIntervalos = []
           
            h = (limites[count_b] - limites[count_a]) / intervalos
            xi = limites[count_a]
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(["Xi", "f(Xi)"])
            for i in range(intervalos + 1):
                tabla_datos.append([xi, funcion.subs(variable, xi).evalf()])
                instancia_respuesta.agregar_fila(tabla_datos[i])
                xi += h
            instancia_respuesta.agregar_tabla()
            tabla_datos_suma = sum(sublist[1] for sublist in tabla_datos)
            instancia_respuesta.agregar_parrafo(f"Suma f(Xi) = {tabla_datos_suma}")
            tabla_datos = np.array(tabla_datos)
            #calculamos h2 para los subintervalos
            h2 = (tabla_datos[1,0] - tabla_datos[0, 0]) / 2
            
            #agregar el primer valor, al primer valor de tabla principal se le suma el h2
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(["Xmi", "f(Xmi)"])
            for i in range(tabla_datos.size):
                if tabla_datos[i, 0]+h2 > tabla_datos[-1, 0]-h2:
                    break
                else:
                    tabla_datos_subIntervalos.append([tabla_datos[i, 0]+h2, funcion.subs(variable, tabla_datos[i, 0]+h2).evalf()])
                    instancia_respuesta.agregar_fila(tabla_datos_subIntervalos[i])

            instancia_respuesta.agregar_tabla()
            
            tabla_datos_subIntervalos = sum(sublist[1] for sublist in tabla_datos_subIntervalos)
            instancia_respuesta.agregar_parrafo(f"Suma f(Xmi): {tabla_datos_subIntervalos}")
            
            #Suma de valores intermedios
            suma_intermedios = 0
            for u in range(intervalos):
                if u == 0:
                    continue
                else:
                    suma_intermedios += tabla_datos[u, 1]

            I = Simpson_13.simpson_compuesto(limites[count_a], limites[count_b], tabla_datos[0, 1], suma_intermedios, tabla_datos_subIntervalos, tabla_datos[-1,-1], intervalos)
            count_a += 2
            count_b += 2
            funcion = I
            fx1 = conversla_html.mathl_(I)
            instancia_respuesta.agregar_parrafo(f"Resultado: {fx1}")

        instancia_respuesta.agregar_clave_valor_segundo("Respuesta: ", I)
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return resp
