import sympy as sp
from modelos.extras.Funciones import  respuesta_json

class metodo_lineal():
    def calcular_lineal(json_data):
        x = sp.symbols('x')
        f_x = sp.simplify(json_data['funcion'])
        grado = f_x.as_poly().degree()
        if(grado == 1):
            solucion = sp.solve(f_x, x)
            return #la respuesta del json
        else:
            #manejar excepciones
            return #loq sea que se quiera retornar