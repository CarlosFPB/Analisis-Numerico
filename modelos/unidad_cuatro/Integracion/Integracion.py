
from flask import jsonify
from ...extras.Funciones import respuesta_json
from ...unidad_cuatro.Integracion.Trapecio import Trapecio
from ...unidad_cuatro.Integracion.Simpson.Simpson1 import Simpson1_3
from ...unidad_cuatro.Integracion.Simpson.Simpson2 import Simpson3_8

class integracion_():
    @staticmethod
    def calcular_integracion(json_data):
        try:
            instancia_respuesta = respuesta_json()
            # Obtengo los valores del json
            if json_data["tipo"] == "Compuesto":
                integral = json_data["latex"]
                intervalos = int(json_data["intervalos"])
                if json_data["metodo"] == "Trapecio":
                    resp = Trapecio.metodo_trapecio.calcular_trapecio(integral, intervalos)
                    return resp
                elif json_data["metodo"] == "Simpson 1/3":
                    # Metodo simpson 1/3
                    resp = Simpson1_3.metodo_simpson.calcular_simpson13(integral, intervalos)
                    return resp
                    print("Simpson 1/3 method")
                else:
                    # Metodo simpson 1/8
                    resp = Simpson3_8.metodo_simpson.calcular_simpson38(integral, intervalos)
                    return resp
                    print("Simpson 3/8 method")
            else:#Trapecio simple
                integral = json_data["latex"]
                if json_data["metodo"] == "Trapecio":
                    # Metodo trapecio simple
                    resp = Trapecio.metodo_trapecio.calcular_trapecio(integral)
                    return resp
                elif json_data["metodo"] == "Simpson 1/3":
                    resp = Simpson1_3.metodo_simpson.calcular_simpson13(integral)
                    return resp
                    # Metodo simpson 1/3
                else:
                    resp = Simpson3_8.metodo_simpson.calcular_simpson38(integral)
                    return resp
                    # Metodo simpson 1/8
                    print("Simpson 3/8 method")
        except Exception as e:
            resp = instancia_respuesta.responder_error(f"Error interno del codigo\n {str(e)}")
            return jsonify(resp), 500
