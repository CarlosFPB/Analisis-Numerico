
from flask import jsonify
from ...extras.Funciones import respuesta_json
from ...unidad_cuatro.Integracion.Trapecio import Trapecio
from ...unidad_cuatro.Integracion.Simpson.Simpson1 import Simpson1_3
from ...unidad_cuatro.Integracion.Simpson.Simpson2 import Simpson3_8
from ...unidad_cuatro.Integracion.Trapecio.Trapecio import metodo_trapecio_tabla
from ...unidad_cuatro.Integracion.Simpson.Simpson1.Simpson1_3 import metodo_simpson13_tabla
from ...unidad_cuatro.Integracion.Simpson.Simpson2.Simpson3_8 import metodo_simpson38_tabla
class integracion_():
    @staticmethod
    def calcular_integracion(json_data):
        try:
            instancia_respuesta = respuesta_json()
            if json_data["modo"] == 1:
                # Obtengo los valores del json Verifcar tipo
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
                else:#Metodos simple
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
            else:#Metodo tabla Metodo 2
                #verificar el metodo
                    if json_data["metodo"] == "Trapecio":                   #matriz         Metodo
                        resp = metodo_trapecio_tabla.calcular_trapecio_tabla(json_data["matrizPuntos"], json_data["tipo"])
                        return resp
                    elif json_data["metodo"] == "Simpson 1/3":
                        resp = metodo_simpson13_tabla.calcular_simpson13_tabla(json_data["matrizPuntos"], json_data["tipo"])
                        return resp
                    else: #Metodo Simpson3/8
                        resp = metodo_simpson38_tabla.calcular_simpson38_tabla(json_data["matrizPuntos"], json_data["tipo"])
                        return resp
        except Exception as e:
            resp = instancia_respuesta.responder_error(f"Error interno del codigo\n {str(e)}")
            return jsonify(resp), 500
