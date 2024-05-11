from modelos.extras.Funciones import respuesta_json
from flask import jsonify


class metodo_lagrange:

    def calcular_lagrange(json_data):
        try:

            instancia_respuesta = respuesta_json()
            try:
                #el aprametro es la clave del dato que queres
                funcion = json_data['funcion']
            except:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            
            #aqui va tu codigo para lagrange


        except:
            resp = instancia_respuesta.responder_error("Error en el codigo interno del metodo de lagrange")
            return jsonify(resp), 400





