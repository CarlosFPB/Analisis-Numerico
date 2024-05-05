import  sympy as sp
import numpy as np
from .....Extras.funciones import errores, respuesta_json


class metodo_horner():


    def calcular_Horner(json_data):

        # Definir símbolos
        x = sp.symbols('x')

        # Ecuación a dividir (dividendo)
        f_x_crudo = json_data["funcion"]
        x0_crudo = json_data["xi"]
        tolerancia_crudo = json_data["tolerancia"]
        f_x = sp.sympify(f_x_crudo)
        x0 = float(x0_crudo)
        error_aceptado = float(tolerancia_crudo)

        tabla_final = []
        f_x0 = x - x0 #- para cambiar signo
        iteracion = 0
        tabla_final.append(["Iteracion","X0","R","S","Xi","Ea%"])
        while True:
            iteracion += 1
            # 1 div sintetica
            cociente, residuo = sp.div(f_x, f_x0)
            R = residuo
            #2 divicion
            cociente2, residuo2 = sp.div(cociente, f_x0)
            S = residuo2
            x_calculado = x0 - (R/S)
            error_acomulado = errores.error_aproximado_porcentual(x0, x_calculado)
            print(f"Iteración: {iteracion} error: {error_acomulado.evalf()} error aceptado: {error_aceptado}")
            tabla_final.append([iteracion,format(x0),format(R),format(S),format(x_calculado),format(error_acomulado)])
            if error_acomulado < error_aceptado:
                break
            f_x0 = x - x_calculado #- para que cambie el signo 
            x0 = x_calculado

        print(f"La raíz es: {x_calculado}")
