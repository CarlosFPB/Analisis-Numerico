
import sympy as sp
from Extras.funciones import *


x = sp.symbols('x')
f_x = sp.E**-x - x


error_aceptable = errores.error_de_tolerancia(3)
x1 = 0
xu = 1
xr = 0
valor_real = 0.56714

condicion = ""
iteracion =1
xr = biseccion.primera_aproximacion(x1,xu)
valor_anterior = xr
while True:
    
    #primera aproximacion
    evaluacion = biseccion.multiplicacion_evaluadas(f_x,x1,xr)
    if evaluacion > 0:
        x1 = xr
        condicion=">0"
    elif evaluacion < 0:
        xu = xr
        condicion="<0"
    else:
        condicion="=0"
        break

    if not iteracion == 1:
        #print(f"valor anterior {valor_anterior} valor actual {xr}")
        error_acumulado = errores.error_aproximado_porcentual(valor_anterior,xr)
        #print(error_acumulado)
        if error_acumulado < error_aceptable:
            break
    
    iteracion +=1
    valor_anterior = xr
    xr = biseccion.primera_aproximacion(x1,xu)  




print("La raiz de la ecuacion es: ",xr)
print("En la iteracion #", iteracion)
print(f"Con un error de: {error_acumulado}%")

