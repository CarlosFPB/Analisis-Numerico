import sympy as sp
from flask import jsonify
from ......extras.Funciones import errores, falsaPosicion, respuesta_json, verificaciones
from modelos.extras.latex import conversla
from modelos.extras.latex import conversla,conversla_html



class metodo_falsa_posicion():

   
        def calcular_falsa_posicion(json_data):
            try:
                x = sp.symbols('x')
                #instancio las respuest json
                instancia_respuesta = respuesta_json()

                #Verificar la funcion obtenida
                try:
                    #Ecuaion de la funcion
                    f_x =conversla.latex_(json_data["latex"])
                    f_x = sp.sympify(f_x)

                    resultado = f_x.subs(x, 1).evalf()
                    is_imaginary = resultado.is_imaginary

                    if resultado.is_real and resultado > 0:
                        pass
                    elif is_imaginary:
                        pass

                except sp.SympifyError:
                    resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                    return jsonify(resp), 400
                except TypeError as e:
                    resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                    return jsonify(resp), 400
                
                #verificar que sea grado mayor a 0
                if verificaciones.obtener_grado(f_x) != None:#es porq es polinomica sino no importa el grado
                    if verificaciones.obtener_grado(f_x) < 1:
                        resp = instancia_respuesta.responder_error("La función debe ser de grado 1 o mayor")
                        return jsonify(resp), 400
                
                #Verificar los valores iniciales
                try:
                    error_aceptable = float(json_data["tolerancia"])
                    x1 = float(json_data["xi"])
                    xu = float(json_data["xu"])
                except ValueError as e:
                    resp = instancia_respuesta.responder_error("Error en los valores iniciales\n"+str(e))
                    return jsonify(resp), 400
                
                xr = 0
                condicion = ""
                iteracion = 0

                #execpciones comunes
                evaluar_x1 = f_x.subs(x,x1)
                evaluar_xu = f_x.subs(x,xu)
                if (evaluar_x1 * evaluar_xu) > 0:#no ahy un cambio de signo
                #print("No hay un cambio de signo en los valores iniciales")
                    resp = instancia_respuesta.responder_error("No se encontró cambio de signo en los valores iniciales por ende no hay raíz en el intervalo dado")
                    return jsonify(resp), 400

                instancia_respuesta.agregar_titulo1("Metodo de Falsa Posicion")
                instancia_respuesta.agregar_parrafo("Este metodo nos sirve para encontrar la raiz de una ecuacion, para ello se necesita una funcion f(x) continua en un intervalo [a,b] que contenga a la raiz.")
                instancia_respuesta.crear_tabla()
                instancia_respuesta.agregar_titulo1("Valores Iniciales")
                fx1 = conversla_html.mathl_(f_x)
                instancia_respuesta.agregar_parrafo(f"Funcion: {fx1}")
                instancia_respuesta.agregar_clave_valor("Xi: ", x1)
                instancia_respuesta.agregar_clave_valor(f"Xu: ", xu)
                instancia_respuesta.agregar_clave_valor(f"Tolerancia: ", error_aceptable)
                instancia_respuesta.agregar_fila(['Iteracion','X1','Xu','Xr','f(Xr)','Condicion','Error'])
                instancia_respuesta.agregar_titulo1("El calculo de la raiz se hace por la siguiente formula: ")
                hmtl_conten = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mi>X</mi><mi>r</mi><mo>=</mo><mi>X</mi><mi>u</mi><mo>&#x2212;</mo><mfrac><mrow><mi>f</mi><mo form="prefix" stretchy="false">(</mo><mi>X</mi><mi>u</mi><mo form="postfix" stretchy="false">)</mo><mo form="prefix" stretchy="false">(</mo><mi>X</mi><mi>i</mi><mo>&#x2212;</mo><mi>X</mi><mi>u</mi><mo form="postfix" stretchy="false">)</mo></mrow><mrow><mi>f</mi><mo form="prefix" stretchy="false">(</mo><mi>X</mi><mi>i</mi><mo form="postfix" stretchy="false">)</mo><mo>&#x2212;</mo><mi>f</mi><mo form="prefix" stretchy="false">(</mo><mi>X</mi><mi>u</mi><mo form="postfix" stretchy="false">)</mo></mrow></mfrac></mrow></math>
"""
                instancia_respuesta.agregar_parrafo(f"Formula: {hmtl_conten}" )
                hmtl_conten = f"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>X</mi><mi>r</mi><mo>=</mo><mi>{xu}</mi><mo>&#x2212;</mo><mfrac><mrow><mi>f</mi><mo form="prefix" stretchy="false">(</mo><mi>{xu}</mi><mo form="postfix" stretchy="false">)</mo><mo form="prefix" stretchy="false">(</mo><mi>{x1}</mi><mo>&#x2212;</mo><mi>{xu}</mi><mo form="postfix" stretchy="false">)</mo></mrow><mrow><mi>f</mi><mo form="prefix" stretchy="false">(</mo><mi>{x1}</mi><mo form="postfix" stretchy="false">)</mo><mo>&#x2212;</mo><mi>f</mi><mo form="prefix" stretchy="false">(</mo><mi>{xu}</mi><mo form="postfix" stretchy="false">)</mo></mrow></mfrac></math>"""
                instancia_respuesta.agregar_parrafo(f"Iteracion 1: {hmtl_conten} = {falsaPosicion.primera_aproximacion(f_x,x1,xu)}")
                while True:
                    iteracion += 1
                    error_acumulado = 0
                    valor_anterior = xr
                    xr = falsaPosicion.primera_aproximacion(f_x,x1,xu)
                    xr = sp.N(xr)
                    #primera aproximacion
                    evaluacion = falsaPosicion.multiplicacion_evaluadas(f_x,x1,xr)
                    if evaluacion > 0:
                        condicion=">0"
                        x1 = xr
                    elif evaluacion < 0:
                        condicion="<0"
                        xu = xr
                    else:
                        xr = xr #ya encontre la raiz
                        error_acumulado = 0
                        instancia_respuesta.agregar_fila([iteracion,x1,xu,xr,evaluacion,condicion,error_acumulado])
                        break

                    if not iteracion == 1:
                        error_acumulado = errores.error_aproximado_porcentual(valor_anterior,xr)
                        error_acumulado = sp.N(error_acumulado)
                        if error_acumulado < error_aceptable:
                            instancia_respuesta.agregar_fila([iteracion,x1,xu,xr,evaluacion,condicion,error_acumulado])
                            break
                    instancia_respuesta.agregar_fila([iteracion,x1,xu,xr,evaluacion,condicion,error_acumulado])

                instancia_respuesta.agregar_titulo1("Resultados: ")
                instancia_respuesta.agregar_clave_valor("Iteraciones: ",iteracion)
                instancia_respuesta.agregar_clave_valor("Raiz: ",xr)
                instancia_respuesta.agregar_clave_valor("Error: ",error_acumulado)
                instancia_respuesta.agregar_tabla()
                resp = instancia_respuesta.obtener_y_limpiar_respuesta()
                return jsonify(resp), 200

            except Exception as e:
                resp = instancia_respuesta.responder_error("Error interno del codigo\n"+str(e))
                return jsonify(resp), 500
        
