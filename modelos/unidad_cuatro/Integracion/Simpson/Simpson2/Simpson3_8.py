
from flask import jsonify
import sympy as sp
import numpy as np
from .....extras.Funciones import respuesta_json, verificaciones
from .....extras.latex import conversla, conversla_html
from .....extras.Integrales import integr_obtener, Simpson_38, verificacion_puntos_tabla

class metodo_simpson:
    @staticmethod
    def calcular_simpson38(*args):
      
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
                resp = instancia_respuesta.responder_error("No se permiten caracteres especiales")
                return jsonify(resp), 400
            except Exception as e:
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400

            cantidad = len(args)
            if cantidad == 2:  # compuesto
                res = metodo_simpson.simpson38_compuesto(funcion, limites, variables, args[1], f_x)
                return jsonify(res), 200
            else:  # simple, tener en cuenta que solo tiene que ser integral unidimensional
                if len(variables) > 1:
                    resp = instancia_respuesta.responder_error("La integral debe ser unidimensional")
                    return jsonify(resp), 400
                resp = metodo_simpson.simpson38_simple(funcion, variables, limites, f_x)
                return jsonify(resp), 200

        except Exception as e:
            resp = instancia_respuesta.responder_error(f"Error interno en el servidor" )
            return jsonify(resp), 500

    
    @staticmethod
    def simpson38_simple(funcion, variables, limites, f_x):
        h = (limites[1]-limites[0]) / 3
        instancia_respuesta = respuesta_json()
        x0 = sp.N(funcion.subs(variables[0], limites[0]))
        x1 = sp.N(funcion.subs(variables[0], limites[0]+h))
        x2 = sp.N(funcion.subs(variables[0], limites[0]+(2*h)))
        x3 = sp.N(funcion.subs(variables[0], limites[1]))
        I = Simpson_38.simpson_simple(limites[0], limites[1], x0, x1, x2, x3)
        
        instancia_respuesta.agregar_titulo1("Simpson 3/8 Simple")
        fx1 = conversla_html.mathl_(f_x)
        instancia_respuesta.agregar_parrafo(f"Integral: {fx1}")
        instancia_respuesta.agregar_clave_valor("Respuesta: ", I)
        instancia_respuesta.agregar_titulo1("Formula")
        html_content = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mfenced><mrow><mo>(</mo><mi>b</mi><mo>-</mo><mi>a</mi><mo>)</mo></mrow></mfenced><mfenced open="[" close="]"><mfrac><mrow><mi>f</mi><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>+</mo><mn>3</mn><mi>f</mi><mo>(</mo><msub><mi>x</mi><mi>i</mi></msub><mo>)</mo><mo>+</mo><mn>3</mn><mi>f</mi><mfenced><mrow><msub><mi>x</mi><mn>2</mn></msub></mrow></mfenced><mo>+</mo><mi>f</mi><mo>(</mo><msub><mi>x</mi><mn>3</mn></msub><mo>)</mo></mrow><mn>8</mn></mfrac></mfenced></math>"""
        instancia_respuesta.agregar_parrafo(f"{html_content}")
        html_content = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mfenced><mrow><mo>(</mo><mrow><mi>{limites[1]}</mi><mo>-</mo><mi>{limites[0]}</mi></mrow><mo>)</mo></mrow></mfenced><mfenced open="[" close="]"><mfrac><mrow><mi>{x0}</mi><mo>+</mo><mi>{3*x1}</mi><mo>+</mo><mi>{3*x2}</mi><mo>+</mo><mi>{x3}</mi></mrow><mn>8</mn></mfrac></mfenced></math>"""
        instancia_respuesta.agregar_parrafo(f"{html_content}")
        instancia_respuesta.agregar_parrafo(f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mi>{I}</mi></math>""")
        instancia_respuesta.agregar_titulo1("Datos")
        instancia_respuesta.crear_tabla()
        instancia_respuesta.agregar_fila(["Xi", "f(Xi)"])
        instancia_respuesta.agregar_fila([limites[0], x0])
        instancia_respuesta.agregar_fila([limites[0]+h, x1])
        instancia_respuesta.agregar_fila([limites[0]+(2*h), x2])
        instancia_respuesta.agregar_fila([limites[1], x3])
        instancia_respuesta.agregar_tabla()
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return resp

    @staticmethod
    def simpson38_compuesto(funcion, limites, variables, intervalos, f_x):
        instancia_respuesta = respuesta_json()

        #Respuesta con json
        instancia_respuesta.agregar_titulo1("Simpson 3/8 Compuesto")
        fx1 = conversla_html.mathl_(f_x)
        instancia_respuesta.agregar_parrafo(f"Integral: {fx1}")
        instancia_respuesta.agregar_titulo1("Formula")
        html_content = """<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>I</mi><mo>=</mo><mfenced><mo>(</mo><mfrac><mrow><mi>b</mi><mo>-</mo><mi>a</mi></mrow><mrow><mn>8</mn><mi>n</mi></mrow></mfrac><mo>)</mo></mfenced><mfenced open="[" close="]"><mrow><mi>f</mi><mrow><mo>(</mo><mrow><msub><mi>x</mi><mn>0</mn></msub></mrow><mo>)</mo></mrow><mo>+</mo><mn>3</mn><munderover accent='false' accentunder='false'><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>n</mi></munderover><mi>f</mi><mrow><mo>(</mo><mrow><msub><mi>x</mi><mrow><mi>m</mi><mi>i</mi></mrow></msub></mrow><mo>)</mo></mrow><mo>+</mo><mn>2</mn><munderover accent='false' accentunder='false'><mo>&#x2211;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>n</mi><mo>-</mo><mn>1</mn></mrow></munderover><mi>f</mi><mrow><mo>(</mo><mrow><msub><mi>x</mi><mi>i</mi></msub></mrow><mo>)</mo></mrow><mo>+</mo><mi>f</mi><mrow><mo>(</mo><mrow><msub><mi>x</mi><mi>n</mi></msub></mrow><mo>)</mo></mrow></mrow></mfenced></math>"""
        instancia_respuesta.agregar_parrafo(f"{html_content}")
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
            h2 = (tabla_datos[1,0] - tabla_datos[0, 0]) / 3
           #Calculo de los subintervalos
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(["Xmi", "f(Xmi)"])
            valor_subint = tabla_datos[0, 0] + h2   
            for i in range(tabla_datos.size):
                if valor_subint > tabla_datos[-1, 0]-h2:
                    break
                else:
                    tabla_datos_subIntervalos.append([valor_subint, funcion.subs(variable, valor_subint).evalf()])
                    instancia_respuesta.agregar_fila(tabla_datos_subIntervalos[i])
                valor_subint += h2
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

            I = Simpson_38.simpson_compuesto(limites[count_a], limites[count_b], tabla_datos[0, 1], tabla_datos_subIntervalos, suma_intermedios, tabla_datos[-1, -1], intervalos)
            count_a += 2
            count_b += 2
            funcion = I
            fx1 = conversla_html.mathl_(I)
            instancia_respuesta.agregar_parrafo(f"Resultado: {fx1}")

        instancia_respuesta.agregar_clave_valor_segundo("Respuesta: ", I)
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return resp


class metodo_simpson38_tabla():
    @staticmethod 
    def calcular_simpson38_tabla(matrizPuntos, tipo):
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
                resp = metodo_simpson38_tabla.simpson38_simple_tabla(puntos_x, puntos_y)
                return resp
            else: # Compuesto
                resp = metodo_simpson38_tabla.simpson38_compuesto_tabla(puntos_x, puntos_y)
                return resp
        except Exception as e:
            resp = instancia_respuesta.responder_error(f"Error interno en el servidor" )
            return jsonify(resp), 500

    @staticmethod
    def simpson38_simple_tabla(puntos_x, puntos_y):
        instancia_respuesta = respuesta_json()

        if (len(puntos_x) - 1) % 3 != 0:
            resp = instancia_respuesta.responder_error("Los datos tabulados no se ajustan con Simpson 8/3 Simple; se necesitan datos adicionales.")
            return jsonify(resp),200
        #Calcular trapecio simple
        resultado_suma = 0 
        anterior=0
        actual=3
        if len(puntos_x) == 4:
            resultado = Simpson_38.simpson_simple(puntos_x[anterior], puntos_x[actual], puntos_y[anterior], puntos_y[anterior+1], puntos_y[anterior+2], puntos_y[anterior+3])
            resultado_suma = resultado
        else:
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(["Intervalo", "Puntos x", "Puntos f(x)", "Resultado"])
            for i in range(int(len(puntos_x)/3)):
                resultado = Simpson_38.simpson_simple(puntos_x[anterior], puntos_x[actual], puntos_y[anterior], puntos_y[anterior+1], puntos_y[anterior+2], puntos_y[anterior+3])
                instancia_respuesta.agregar_fila([i+1, puntos_x[anterior:actual+1], puntos_y[anterior:actual+1], resultado])
                anterior = actual
                actual += 3
                resultado_suma += resultado
            instancia_respuesta.agregar_tabla()
        instancia_respuesta.agregar_titulo1("Metodo Simpson 3/8")
        instancia_respuesta.agregar_clave_valor("Resultado: ", resultado_suma)
        h = (puntos_x[1] - puntos_x[0])
        instancia_respuesta.agregar_clave_valor("Ancho de intervalo (h): ", h)
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return jsonify(resp), 200        

    @staticmethod
    def simpson38_compuesto_tabla(puntos_x, puntos_y):
        instancia_respuesta = respuesta_json()
        if len(puntos_x) < 5:
            resp = instancia_respuesta.responder_error("Se necesitan por lo menos 5 datos tabulados para resolver por Simpson 3/8 Compuesto")
            return jsonify(resp), 400
        
        #Suma intermedios

        #Calcular intervalos
        n = (len(puntos_x)-1)
        h = (puntos_x[-1] - puntos_x[0]) / n
        suma_3i_2 = 0
        suma_3i_1 = 0
        suma_3i = 0

        for i in range(1, n):
            if i % 3 == 0:
                suma_3i += puntos_y[i]  # 2*f(x_{3i})
            elif i % 3 == 1: 
                suma_3i_2 += puntos_y[i]  # 3*f(x_{3i-2})
            else:
                suma_3i_1 += puntos_y[i]  # 3*f(x_{3i-1})+ 
        
        resultado = Simpson_38.simpson_compuesto_tabla(puntos_y[0], suma_3i_2, suma_3i_1, suma_3i, puntos_y[-1], h)
      
        instancia_respuesta.agregar_titulo1("Metodo Simpson 3/8 Compuesto")
        instancia_respuesta.agregar_clave_valor("Resultado: ", resultado)
        instancia_respuesta.agregar_clave_valor("Suma 3i_2: ", suma_3i_2)
        instancia_respuesta.agregar_clave_valor("Suma 3i_1: ", suma_3i_1)
        instancia_respuesta.agregar_clave_valor("Suma 3i: ", suma_3i)
        instancia_respuesta.agregar_clave_valor("Valor de Intervalos: ", n)
        instancia_respuesta.agregar_clave_valor("Valor de h: ", h)
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return jsonify(resp), 200
    
