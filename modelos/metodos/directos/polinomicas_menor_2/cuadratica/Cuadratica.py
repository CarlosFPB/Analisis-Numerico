import sympy as sp
from modelos.extras.Funciones import  respuesta_json

class metodo_cuadratico():
    def calcular_cuadratico(json_data):
        x = sp.symbols('x')
        f_x = sp.simplify(json_data['funcion'])
        grado = f_x.as_poly().degree()
        if(grado == 2):
            solucion = sp.solve(f_x, x)
            return respuesta_json(solucion)
        else:
            return respuesta_json("La función no es cuadrática")