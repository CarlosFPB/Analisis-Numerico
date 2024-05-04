import  sympy as sp
import numpy as np
from .....Extras.funciones import errores, respuesta_json

class metodo_muller():


    def calcular_Muller(json_data):
        # Definir símbolos
        x = sp.symbols('x')
        
        # obtengo los valores del json
        f_x_crudo = json_data["funcion"]
        x0_crudo = json_data["X0"]
        x1_crudo = json_data["X1"]
        x2_crudo = json_data["X2"]
        tolerancia_crudo = json_data["tolerancia"]
        f_x = sp.sympify(f_x_crudo)
        x0 = float(x0_crudo)
        x1 = float(x1_crudo)
        x2 = float(x2_crudo)
        error_aceptado = float(tolerancia_crudo)

 
        iteracion = 0
        tabla_final = []
        tabla_final.append(["Iteracion","X0","X1","X2","Raiz","Ea%"])

        while True:
            iteracion +=1
            #calcular evaluadas
            f_x0 = f_x.subs(x, x0)
            f_x1 = f_x.subs(x, x1)
            f_x2 = f_x.subs(x, x2)

            #calcular h0 y h1
            h0 = x1 - x0
            h1 = x2 - x1

            #calcular delta0 y delta1
            delta0 = (f_x1 - f_x0) / h0
            delta1 = (f_x2 - f_x1) / h1

            #calcular a, b, c
            a = (delta1 - delta0) / (h1 + h0)
            b = a * h1 + delta1
            c = f_x2

            #calcular D
            D = (sp.sqrt(b**2 - 4*a*c))

            if abs(b + D) > abs(b - D):
                x_calculado = x2 + ((-2*c)/(b + D)) #en la diapositiva de la ingeniera sale b**2 chapra no
            else:
                x_calculado = x2 + ((-2*c)/(b - D))# con b**2 tarda muchas iteraciones


            #Error acomulado
            error_acomulado = errores.error_aproximado_porcentual(x2,x_calculado)
            tabla_final.append([iteracion,format(x0),format(x1),format(x2),format(x_calculado),format(error_acomulado)])
            #comparacion 
            print("Iteracion: ",iteracion)
            #ahy error cuando el metodo tiene un error muy grande rompe el codigo ya q no puede vealuar la comparacion
            if error_acomulado < error_aceptado:
                break
            #sino cambiar valores
            x0 = x1
            x1 = x2
            x2 = x_calculado

        print(f"La raíz es: {x_calculado}")