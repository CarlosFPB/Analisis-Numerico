import sympy as sp
from .....extras.Funciones import errores, falsaPosicion, respuesta_json


class falsa_posicion():

    def calcular_falsa_posicion(json_data):
        x = sp.symbols('x')

        #instancio las respuest json
        instancia_respuesta = respuesta_json()

        #obtengo los valores del json
        f_x = sp.sympify(json_data["funcion"])
        error_aceptable = float(json_data["tolerancia"])
        x1 = float(json_data["xi"])
        xu = float(json_data["xu"])
        xr = 0

        while True:
            iteracion =1
            valor_anterior = xr
            xr = falsaPosicion.primera_aproximacion(f_x,x1,xu)
            #primera aproximacion
            evaluacion = falsaPosicion.multiplicacion_evaluadas(f_x,x1,xr)
            if evaluacion > 0:
                x1 = xr
            elif evaluacion < 0:
                xu = xr
            else:
                break

            if not iteracion == 1:
                #print(f"valor anterior {valor_anterior} valor actual {xr}")
                error_acumulado = errores.error_aproximado_porcentual(valor_anterior,xr)
                #print(error_acumulado)
                if error_acumulado < error_aceptable:
                    break
                




        print("La raiz de la ecuacion es: ",xr)
        print("En la iteracion #", iteracion)
        print(f"Con un error de: {error_acumulado}%")
