import traceback

from flask import jsonify
from ...extras.Funciones import respuesta_json
from ...unidad_cuatro.Integracion.Trapecio import Trapecio

class integracion_():
    @staticmethod
    def calcular_integracion(json_data):
        try:
            instancia_respuesta = respuesta_json()
            # Obtengo los valores del json
            if json_data["tipo"] == "Compuesto":
                integral = json_data["latex"]
                intervalos = json_data["intervalos"]
                if json_data["metodo"] == "Trapecio":
                    resp = Trapecio.metodo_trapecio.calcular_trapecio(integral, intervalos)
                    return resp
                elif json_data["metodo"] == "Simpson 1/3":
                    # Metodo simpson 1/3
                    print("Simpson 1/3 method")
                else:
                    # Metodo simpson 1/8
                    print("Simpson 3/8 method")
            else:#Trapecio simple
                integral = json_data["latex"]
                if json_data["metodo"] == "Trapecio":
                    # Metodo trapecio simple
                    resp = Trapecio.metodo_trapecio.calcular_trapecio(integral)
                    return resp
                elif json_data["metodo"] == "Simpson 1/3":
                    # Metodo simpson 1/3
                    print("Simpson 1/3 method")
                else:
                    # Metodo simpson 1/8
                    print("Simpson 3/8 method")
        except Exception as e:
            traceback.print_exc()
            resp = instancia_respuesta.responder_error(f"Error interno del codigo\n {str(e)}")
            return jsonify(resp), 500
