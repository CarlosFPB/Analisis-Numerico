
from flask import jsonify
import sympy as sp
import numpy as np
from ....extras.Funciones import respuesta_json, verificaciones
from ....extras.latex import conversla, conversla_html
from ....extras.Integrales import Trapecio, integr_obtener, verificacion_puntos_tabla
class metodo_trapecio:
    @staticmethod
    def calcular_trapecio(*args):
        
        try:
            instancia_respuesta = respuesta_json()
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
                res = metodo_trapecio.trapecio_compuesto(funcion, limites, variables, args[1], f_x)
                return jsonify(res), 200
            else:  # simple, tener en cuenta que solo tiene que ser integral unidimensional
                if len(variables) > 1:
                    resp = instancia_respuesta.responder_error("La integral debe ser unidimensional")
                    return jsonify(resp), 400
                resp = metodo_trapecio.trapecio_simple(funcion, variables, limites, f_x)
                return jsonify(resp), 200

        except Exception as e:
            resp = instancia_respuesta.responder_error(f"Error interno en el servidor {e}" )
            return jsonify(resp), 500

    
    @staticmethod
    def trapecio_simple(funcion, variables, limites, f_x):
        instancia_respuesta = respuesta_json()
        I = Trapecio.trapecio_simple(limites[0],limites[1], funcion.subs(variables[0], limites[0]), funcion.subs(variables[0], limites[1]))
        instancia_respuesta.crear_tabla()
        instancia_respuesta.agregar_titulo1("Trapecio Simple")
        fx1 = conversla_html.mathl_(f_x)
        instancia_respuesta.agregar_parrafo(f"Integral: {fx1}")
        instancia_respuesta.agregar_fila(["Xi", "F(xi)"])
        instancia_respuesta.agregar_fila([limites[0], sp.N(funcion.subs(variables[0], limites[0]))])
        instancia_respuesta.agregar_fila([limites[1], sp.N(funcion.subs(variables[0], limites[1]))])
        instancia_respuesta.agregar_clave_valor("Respuesta: ", I)
        instancia_respuesta.agregar_titulo1("Formula")
        html_content = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mo>(</mo><mi>b</mi><mo>-</mo><mi>a</mi><mo>)</mo><mfrac><mrow><mi>f</mi><mo>(</mo><mi>a</mi><mo>)</mo><mo>+</mo><mi>f</mi><mo>(</mo><mi>b</mi><mo>)</mo></mrow><mn>2</mn></mfrac></math>"""
        instancia_respuesta.agregar_parrafo(f"Formula: {html_content}")
        html_content = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mo>(</mo><mi>{limites[1]}</mi><mo>-</mo><mi>{limites[0]}</mi><mo>)</mo><mfrac><mrow><mi>{sp.N(funcion.subs(variables[0], limites[0]))}</mi><mo>+</mo><mi>{sp.N(funcion.subs(variables[0], limites[1]))}</mi></mrow><mn>2</mn></mfrac></math>"""
        instancia_respuesta.agregar_parrafo(f"{html_content} = {I}")
        instancia_respuesta.agregar_titulo1("Datos")
        instancia_respuesta.agregar_tabla()
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return resp

    @staticmethod
    def trapecio_compuesto(funcion, limites, variables, intervalos, f_x):
        instancia_respuesta = respuesta_json()
        
        instancia_respuesta.agregar_titulo1("Trapecio Compuesto")
        fx1 = conversla_html.mathl_(f_x)
        instancia_respuesta.agregar_parrafo(f"Integral: {fx1}")
        instancia_respuesta.agregar_titulo1("Formula")
        html_content = """<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mo>(</mo><mi>b</mi><mo>-</mo><mi>a</mi><mo>)</mo><mfrac><mrow><mi>f</mi><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>+</mo><mn>2</mn><munderover accent='false' accentunder='false'><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>n</mi><mo>-</mo><mn>1</mn></mrow></munderover><mi>f</mi><mo>(</mo><msub><mi>x</mi><mi>i</mi></msub><mo>)</mo><mo>+</mo><mi>f</mi><mo>(</mo><msub><mi>x</mi><mi>n</mi></msub><mo>)</mo></mrow><mrow><mn>2</mn><mi>n</mi></mrow></mfrac></math>"""
        instancia_respuesta.agregar_parrafo(html_content)
        instancia_respuesta.agregar_titulo1("Datos")
        count_a = 0
        count_b = 1
        for variable in variables:
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(["Xi", "f(xi)"])
            tabla_datos = []
            h = (limites[count_b] - limites[count_a]) / intervalos
            xi = limites[count_a]
            for i in range(intervalos + 1):
                tabla_datos.append([xi, funcion.subs(variable, xi).evalf()])
                instancia_respuesta.agregar_fila(tabla_datos[i])
                xi += h
            suma_intermedios = 0
           
            tabla_datos = np.array(tabla_datos)
            
            for u in range(intervalos):
                if u == 0:
                    continue
                else:
                    suma_intermedios += tabla_datos[u, 1]
            I = Trapecio.trapecio_compuesto(limites[count_a], limites[count_b], tabla_datos[0,1], suma_intermedios, tabla_datos[intervalos, 1], intervalos)
            count_a += 2
            count_b += 2
            funcion = I
            instancia_respuesta.agregar_tabla()
            fx1 = conversla_html.mathl_(I)
            instancia_respuesta.agregar_parrafo(f"Resultado: {fx1}")
        
        instancia_respuesta.agregar_clave_valor_segundo("Respuesta: ", I)
        
        
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return resp


class metodo_trapecio_tabla():
    @staticmethod
    def calcular_trapecio_tabla(matrizPuntos, tipo):

        try:
            instancia_respuesta = respuesta_json()
            try:
                #verificar si la matriz de puntos es valida
                if not verificaciones.es_matriz(matrizPuntos):
                    resp = instancia_respuesta.responder_error("La matriz de puntos no es valida")
                    return jsonify(resp), 400
            except:
                resp = instancia_respuesta.responder_error("Error en los datos ingresados")
                return jsonify(resp), 400
            

            #Parsear tabla y comprobar errores
            tabla_matriz = verificacion_puntos_tabla.verificar_tabla(matrizPuntos)

            if isinstance(tabla_matriz, str):
                #Caso error
                resp  = instancia_respuesta.responder_error(tabla_matriz)
                return jsonify(resp), 400
            else: 
                puntos_x, puntos_y = tabla_matriz

           
            #Verificar si los puntos x tiene el mismo valor de h
            incremento = float(puntos_x[1] - puntos_x[0])
            for i in range(len(puntos_x)-1):
                if round(puntos_x[i+1] - puntos_x[i], 10) != incremento:
                    resp = instancia_respuesta.responder_error(f"Se encontro diferente ancho en un punto de x (el punto{puntos_x[i+1]} con el punto {puntos_x[i]})")
                    return jsonify(resp), 400
            #Verificar con cual tipo se tiene que resolver 
            if tipo == "Simple":
                resp = metodo_trapecio_tabla.trapecio_simple_tabla(puntos_x, puntos_y)
                return resp
            else: # Compuesto
                resp = metodo_trapecio_tabla.trapecio_compuesto_tabla(puntos_x, puntos_y)
                return resp
        except Exception as e:
            resp = instancia_respuesta.responder_error(f"Error interno en el servidor" )
            return jsonify(resp), 500
        
    @staticmethod
    def trapecio_simple_tabla(puntos_x, puntos_y):
        instancia_respuesta = respuesta_json()
        #Calcular trapecio simple
        resultado_suma = 0 
        instancia_respuesta.crear_tabla()
        instancia_respuesta.agregar_fila(["Intervalo", "Puntos x", "Puntos f(x)", "Resultado"])
        for i in range(len(puntos_x)-1):
            resultado = Trapecio.trapecio_simple(puntos_x[i], puntos_x[i+1], puntos_y[i], puntos_y[i+1])
            resultado_suma += resultado
            instancia_respuesta.agregar_fila([i+1, puntos_x[i:i+2], puntos_y[i:i+2], resultado]) # Fixed the issue by changing [i:i+1] to [i:i+2]
        instancia_respuesta.agregar_tabla()
        instancia_respuesta.agregar_clave_valor("Resultado: ", resultado_suma)
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return jsonify(resp), 200        

    @staticmethod
    def trapecio_compuesto_tabla(puntos_x, puntos_y):
        instancia_respuesta = respuesta_json()
        if len(puntos_x) < 4:
            resp = instancia_respuesta.responder_error("Se necesitan por lo menos 4 datos tabulados para resolver por Trapecio Compuesto")
            return jsonify(resp), 400

        # Calcular intervalos
        n = (len(puntos_x)-1)
        h = puntos_x[1] - puntos_x[0]  # Calculo de h
        resultado = Trapecio.trapecio_compuesto(puntos_x[0], puntos_x[-1], puntos_y[0], sum(puntos_y[1:-1]), puntos_y[-1], n)
        instancia_respuesta.agregar_clave_valor("Resultado: ", resultado)
        instancia_respuesta.agregar_clave_valor("Intervalos: ", n)
        instancia_respuesta.agregar_clave_valor("h: ", h)
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return jsonify(resp), 200

