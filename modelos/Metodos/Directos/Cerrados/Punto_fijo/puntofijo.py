import  sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from .....extras.funciones import errores, falsaPosicion, respuesta_json

x = sp.symbols("x")
# f(x) = x**2 - 10*x + 7 ---> g(x) = (x**2 + 7)/10
f_x = x**2 - 10*x + 7
g_x = (x**2 + 7)/10
g_prima = sp.diff(g_x)

error_aceptado = errores.error_de_tolerancia(4)
x_actual = 5
x_anterior = 0

iteracion = 0
#Encabezados
print("{:<12s}{:<25s}{:<25s}{:<25s}{:<25s}".
        format("Iteracion","X","g(x0)","g'(x0)","Ea%"))
while True:
    iteracion += 1
    g_prima_evaluada = float(g_prima.subs(x, x_actual))
    g_x_evaluada = float(g_x.subs(x, x_actual))
    x_anterior = x_actual
    x_actual = g_x_evaluada
    error_acomulado = errores.error_aproximado_porcentual(x_anterior,x_actual)
    print("{:<12d}{:<25s}{:<25s}{:<25s}{:<25s}".
          format(iteracion,format(x_anterior),format(g_x_evaluada),format(g_prima_evaluada),format(error_acomulado)))
    if(error_acomulado < error_aceptado):
        break
    elif g_prima_evaluada > 1:
        print("El metodo no converge")
        break
    
print("La raiz aproximada es: ", x_actual)

