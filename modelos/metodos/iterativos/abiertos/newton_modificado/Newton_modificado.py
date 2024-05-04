from flask import jsonify
import  sympy as sp
import numpy as np
from .....Extras.funciones import errores, newton_modificado, respuesta_json

class metodo_newton_modificado():
    @staticmethod
    def calcular_newton_modificado(json_data):
        x = sp.symbols("x")
        #obteniendo los valores del json
        f_x = sp.sympify(json_data["funcion"])
        f_prima = sp.diff(f_x)
        f_prima_prima = sp.diff(f_prima)

        x_actual = float(json_data["xi"])
        x_anterior = 0

        error_aceptado = float(json_data["tolerancia"])
        error_acomulado = 100
        iteracion = 0

        #instanciar respuesta json
        instancia_respuesta = respuesta_json()

        instancia_respuesta.agregar_titulo1("Newton Modificado")
        instancia_respuesta.agregar_parrafo("asdas")
        instancia_respuesta.crear_tabla()
        instancia_respuesta.agregar_fila(['Iteracion', 'X0', 'F(x0)', 'F\'(x0)', 'F\'\'(x0)', 'Xi', 'Error'])

        #Encabezados
        #print("{:<12s}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}".
         #       format("Iteracion","X0","F(x0)","F'(x0)","F''(x0)","Xi","Ea%"))
        while True:
            iteracion += 1
            f_prima_evaluada = f_prima.subs(x, x_actual)
            f_x_evaluada = f_x.subs(x, x_actual)
            f_prima_prima_evaluada = f_prima_prima.subs(x, x_actual)
            x_anterior = x_actual
            x_actual = newton_modificado.aproximacion(f_x_evaluada, f_prima_evaluada,f_prima_prima_evaluada, x_anterior)
            error_acomulado = errores.error_aproximado_porcentual(x_anterior,x_actual)
            
            instancia_respuesta.agregar_fila([iteracion, x_anterior, f_x_evaluada, f_prima_evaluada, f_prima_prima_evaluada, x_actual, error_acomulado])
            #print("{:<12d}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}{:<25s}".
             #   format(iteracion,format(x_anterior),format(f_x_evaluada),format(f_prima_evaluada),format(f_prima_prima_evaluada),format(x_actual),format(error_acomulado)))
            if(error_acomulado < error_aceptado):
                break
            
            #evaluar el criterio de convergencia
            f_prima_evaluada = f_prima.subs(x, x_actual)
            f_prima_prima_evaluada = f_prima_prima.subs(x, x_actual)
            f_x_evaluada = f_x.subs(x, x_actual)
            criterio = abs((f_prima_evaluada*f_prima_prima_evaluada)/(f_prima_evaluada**2))
            if criterio > 1:
                print("El criterio de convergencia no se cumple")
                break
            
        #print("La raiz aproximada es: ", x_actual)
        instancia_respuesta.agregar_tabla()
        res = instancia_respuesta.obtener_y_limpiar_respuesta()
        return jsonify(res)




