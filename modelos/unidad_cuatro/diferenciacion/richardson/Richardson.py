import sympy as sp
from modelos.extras.Funciones import verificaciones, respuesta_json
from flask import jsonify
from modelos.extras.Derivadas import Diferenciacion
from modelos.unidad_cuatro.diferenciacion.derivadas.Diferenciacion import metodos_diferenciacion
from modelos.extras.latex import conversla

class metodo_richardson():

    
    def agregar_clearD(json_data):
        # Add the "clearD" key with value "True" or update it to "True" if it is "False"
        if "clearD" not in json_data or json_data["clearD"] == "False":
            json_data["clearD"] = "True"
        return json_data
    
    def nivel_dos(dh2, dh1):
        resultado = (4/3)*dh2 - (1/3)*dh1
        resultado = sp.N(resultado)
        return resultado

    def nivel_mayorq3(Dk2,Dk1,nivel):
        if nivel >=3:
            k = nivel - 1
            numerador = (4**k)*Dk2 - Dk1
            denominador = 4**k - 1
            resultado = numerador/denominador
            resultado = sp.N(resultado)
            return resultado
        return None

    def calcular_richardson(json_data):
        x = sp.symbols('x')
        #evaluar errores en derivada
        instancia_respuesta = respuesta_json()

        try:
            f_x =conversla.latex_(json_data["latex"])
            resultado = f_x.subs(x, 1)
            if  resultado > 0:
                pass
        except sp.SympifyError as e:
            resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
            print(e)
            return jsonify(resp), 400
        except TypeError as e:
            resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
            print(e)
            return jsonify(resp), 400
        #verificar que sea grado mayor a 0 si es polinomica
        if verificaciones.obtener_grado(f_x) != None:#es porq es polinomica sino lo es no importa el grado
            if verificaciones.obtener_grado(f_x) < 1:
                resp = instancia_respuesta.responder_error("La funcion es una constante")
                return jsonify(resp), 400

        try:
            json_data = metodo_richardson.agregar_clearD(json_data)
            response, status_code = metodos_diferenciacion.calcular_derivada(json_data)
            #si obtubo un 400 ahy algun error y trae su error sino se prosigue a richardson
            if status_code == 400:
                return response, status_code
        except TypeError as e:
            resp = instancia_respuesta.responder_error("Error en los datos de la derivada")
            return jsonify(resp), 400
        except Exception as e:
            resp = instancia_respuesta.responder_error(f"Error en la derivada\n {str(e)}")
            return jsonify(resp), 400
        
        try:
            nivel = int(json_data["nivel"])
        except ValueError as e:
            resp = instancia_respuesta.responder_error(f"Error en el nivel\n {str(e)}")
            return jsonify(resp), 400
        except KeyError as e:
            resp = instancia_respuesta.responder_error(f"Error en el nivel\n {str(e)}")
            return jsonify(resp), 400
        except Exception as e:
            resp = instancia_respuesta.responder_error(f"Error en el nivel\n {str(e)}")
            return jsonify(resp), 400
        
        if not nivel > 1:
            resp = instancia_respuesta.responder_error("El nivel debe ser mayor a 1")
            return jsonify(resp), 400
        
        h = float(json_data["h"])
        tablaR = []
        hs = [h]

        try:
            instancia_respuesta.agregar_titulo1("Metodo de Richardson")
            instancia_respuesta.agregar_parrafo(f"Se calculara la '{json_data["orden"]}' derivada de la funcion ingresada mediante el metodo de Richardson")
            instancia_respuesta.agregar_clave_valor("Funcion ingresada: ", f_x)
            instancia_respuesta.agregar_parrafo("Con h = "+str(h))
            instancia_respuesta.agregar_parrafo("Nivel = "+str(nivel))
            instancia_respuesta.agregar_parrafo(f"Utilizando la formula del metodo de diferencia finita: {json_data['metodo']}")
            instancia_respuesta.agregar_parrafo("Evaluando la derivada en el punto xi = "+str(json_data["xi"]))

            for i in range(1, nivel):
                h = h/2
                hs.append(h)
            for i in range(1, nivel+1):
                if i == 1:#estamos en primer nivel
                    tablaR.append([])
                    for j in range(0, nivel):
                        json_data["h"] = hs[j]
                        response, status_code = metodos_diferenciacion.calcular_derivada(json_data)
                        if status_code == 200:
                            data = response.get_json()  # Obtener el contenido JSON de la respuesta
                            derivada_evaluada = float(data["respuesta"])
                            tablaR[0].append(derivada_evaluada)
                        else:
                            resp = instancia_respuesta.responder_error("Error en la derivada")
                            return jsonify(resp), 400
                elif i == 2:
                    tablaR.append([])
                    for j in range(0, nivel-1):#estamos en nivel dos desde su formula
                        derivada_evaluada = metodo_richardson.nivel_dos(tablaR[0][j+1], tablaR[0][j])
                        tablaR[1].append(derivada_evaluada)
                else:#nivel 3 para delante
                    tablaR.append([])
                    for j in range(0, nivel-(i-1)):
                        indice1 = (i-2)
                        derivada_evaluada = metodo_richardson.nivel_mayorq3(tablaR[indice1][j+1], tablaR[indice1][j], i)
                        tablaR[i-1].append(derivada_evaluada)
            #sino ahy errores
            instancia_respuesta.crear_tabla()
            for tabla_nivel in tablaR:
                instancia_respuesta.agregar_fila(tabla_nivel)
            instancia_respuesta.agregar_titulo1("Tabla de Richardson")
            instancia_respuesta.agregar_clave_valor("Respuesta de la derivada por richardson es:x", tablaR[-1][-1])
            instancia_respuesta.agregar_tabla_derivada()
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = instancia_respuesta.responder_error(f"Error en el calculo de richardson\n {str(e)}")
            return jsonify(resp), 400
        