import sympy as sp
from modelos.extras.Funciones import  respuesta_json
from flask import jsonify

class metodo_lineal():

    def calcular_lineal(json_data):
        x = sp.symbols('x')
        try:
            f_x = sp.sympify(json_data["funcion"])
        except:
            return jsonify({"error":"Error en la funcion"})
        
        grado = f_x.as_poly().degree()
        if(grado == 1):
            solucion = sp.solve(f_x, x)
            return jsonify({"solucion":solucion})
        else:
            #manejar excepciones
            return jsonify({"error":"La funcion no es de grado 1"})