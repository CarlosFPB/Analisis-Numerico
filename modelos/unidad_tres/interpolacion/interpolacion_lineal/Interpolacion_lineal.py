import sympy as sp
from modelos.extras.Funciones import respuesta_json, verificaciones
from flask import jsonify

class metodo_interpolacion_lineal():

    def interpolacion_lineal(matriz_puntos):
        x = sp.symbols('x')
        puntos_x = matriz_puntos[0]
        puntos_y = matriz_puntos[1]
        y = 0
        y = puntos_y[0] + (puntos_y[1] - puntos_y[0])/(puntos_x[1] - puntos_x[0])*(x - puntos_x[0])
        return y

    @staticmethod
    def calcular_interpolacion(json_data):
        instancia_respuesta = respuesta_json()
        #obtener los datos del json
        try:
            matriz_puntos = []
            matriz_puntos = json_data["matrizPuntos"]
            #verificar si la matriz de puntos es valida
            if not verificaciones.es_matriz(matriz_puntos):
                resp = instancia_respuesta.responder_error("La matriz de puntos no es valida")
                return jsonify(resp), 400
        except:
            resp = instancia_respuesta.responder_error("Error en los datos ingresados")
            return jsonify(resp), 400
        
        #verificar si la matriz de puntos esta vacia o tiene la cantidad nesesaria de datos
        if len(matriz_puntos) == 0:
            resp = instancia_respuesta.responder_error("No se ingresaron puntos")
            return jsonify(resp), 400
        elif len(matriz_puntos) == 1:
            resp = instancia_respuesta.responder_error("Faltan puntos en y")
            return jsonify(resp), 400
        elif len(matriz_puntos) == 2:
            #verificar que cuente con dos parejas de puntos
            if len(matriz_puntos[0]) ==2 and len(matriz_puntos[1]) == 2:
                #verificar que los puntos sean numeros
                if verificaciones.verificar_numeros_matriz(matriz_puntos):
                    #verificar si los puntos en x no se repiten
                    if not verificaciones.verificar_puntos_unicos(matriz_puntos[0]):
                        resp = instancia_respuesta.responder_error("Los puntos en x no deben repetirse")
                        return jsonify(resp), 400
                    #Calcular la interpolacion lineal poreso salimos de las verificaciones
                else:
                    resp = instancia_respuesta.responder_error("Los puntos deben ser numeros")
                    return jsonify(resp), 400
            else:
                resp = instancia_respuesta.responder_error("Los puntos deben ser el mismo numero de puntos en x y y y deben ser 2")
                return jsonify(resp), 400
        elif len(matriz_puntos) > 2:
            resp = instancia_respuesta.responder_error("No debe de haber mas de dos pares de puntos")
            return jsonify(resp), 400
        

        #calcular la interpolacion lineal sino ocurrio ningun error
        try:
            polinomio = metodo_interpolacion_lineal.interpolacion_lineal(matriz_puntos)
            instancia_respuesta.agregar_parrafo("El polinomio interpolante es: ")
            instancia_respuesta.agregar_parrafo(polinomio)
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error al calcular la interpolacion lineal "+str(e))
            return jsonify(resp), 400