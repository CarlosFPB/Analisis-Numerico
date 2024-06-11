import sympy as sp
from modelos.extras.Funciones import verificaciones, respuesta_json
from flask import jsonify
from modelos.extras.Derivadas import Diferenciacion
from modelos.unidad_cuatro.diferenciacion.derivadas.Diferenciacion import metodos_diferenciacion

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

        #evaluar errores en derivada
        instancia_respuesta = respuesta_json()

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
        tabla = []
        hs = [h]

        try:
            for i in range(1, nivel):
                h = h/2
                hs.append(h)
            for i in range(1, nivel+1):
                if i == 1:#estamos en primer nivel
                    tabla.append([])
                    for j in range(0, nivel):
                        response, status_code = metodos_diferenciacion.calcular_derivada(json_data)
                        if status_code == 200:
                            data = response.get_json()  # Obtener el contenido JSON de la respuesta
                            derivada_evaluada = float(data["respuesta"])
                            tabla[0].append(derivada_evaluada)
                        else:
                            resp = instancia_respuesta.responder_error("Error en la derivada")
                            return jsonify(resp), 400
                elif i == 2:
                    tabla.append([])
                    for j in range(0, nivel-1):#estamos en nivel dos desde su formula
                        response, status_code = metodos_diferenciacion.calcular_derivada(json_data)
                        if status_code == 200:
                            data = response.get_json()  # Obtener el contenido JSON de la respuesta
                            derivada_evaluada = float(data["respuesta"])
                            tabla[1].append(derivada_evaluada)
                        else:
                            resp = instancia_respuesta.responder_error("Error en la derivada")
                            return jsonify(resp), 400
                else:#nivel 3 para delante
                    tabla.append([])
                    for j in range(0, nivel-(i-1)):
                        response, status_code = metodos_diferenciacion.calcular_derivada(json_data)
                        if status_code == 200:
                            data = response.get_json()  # Obtener el contenido JSON de la respuesta
                            derivada_evaluada = float(data["respuesta"])
                            tabla[i-1].append(derivada_evaluada)
                        else:
                            resp = instancia_respuesta.responder_error("Error en la derivada")
                            return jsonify(resp), 400
        except Exception as e:
            resp = instancia_respuesta.responder_error(f"Error en el calculo de richardson\n {str(e)}")
            return jsonify(resp), 400
        #sino ahy errores
        instancia_respuesta.crear_tabla
        for tabla_nivel in tabla:
            instancia_respuesta.agregar_fila(tabla_nivel)
        instancia_respuesta.agregar_parrafo(f"Respuesta : {tabla[-1][0]}")
        instancia_respuesta.obtener_tabla()
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return jsonify(resp), 200