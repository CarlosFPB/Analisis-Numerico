import  sympy as sp
import numpy as np
from .....extras.Funciones import errores, secante, respuesta_json


class metodo_secante():
    
    def calcular_secante(json_data):
        x = sp.symbols("x")

        #obteniendo los valores del json
        f_x = sp.sympify(json_data["funcion"])
        x_anterior = float(json_data["x0"])
        x_actual = float(json_data["x1"])
        x_calculada = 0

        error_aceptado = float(json_data["tolerancia"])
        error_acomulado = 100
        iteracion = 0

        #Encabezados
        print("{:<12s}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}".
                format("Iteracion","X0","X1","F(x0)","F(x1)","Xr","Ea%"))

        while True:
            iteracion += 1
            f_x_evaluada_anterior = f_x.subs(x, x_anterior)
            f_x_evaluada_actual = f_x.subs(x, x_actual)
            x_calculada = secante.aproximacion(f_x_evaluada_anterior,f_x_evaluada_actual,x_anterior,x_actual)
            error_acomulado = errores.error_aproximado_porcentual(x_actual,x_calculada)
            print("{:<12d}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}".
                format(iteracion,format(x_anterior),format(x_actual),format(f_x_evaluada_anterior),format(f_x_evaluada_actual),format(x_calculada),format(error_acomulado)))
            x_anterior = x_actual
            x_actual = x_calculada
            if(error_acomulado < error_aceptado):
                break
            
        print("La raiz aproximada es: ", x_actual)





