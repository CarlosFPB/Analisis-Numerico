import  sympy as sp
import numpy as np
from .....extras.Funciones import errores, respuesta_json



class metodo_horner():

    def calcular_Horner(json_data):

        try:
            # Definir símbolos
            x = sp.symbols('x')

            # Ecuación a dividir (dividendo)
            f_x_crudo = json_data["funcion"]
            x0_crudo = json_data["x0"]
            tolerancia_crudo = json_data["tolerancia"]
            #instarciar respuesta
            instancia_respuesta = respuesta_json()
            try:
                f_x = sp.sympify(f_x_crudo)
            except:
                res = instancia_respuesta.responder_error("Error en la funcion ingresada, Ingrese una funcion valida")
                return res, 500
        
            x0 = float(x0_crudo)
            error_aceptado = float(tolerancia_crudo)

            f_x0 = x - x0 #- para cambiar signo
            iteracion = 0
            instancia_respuesta.agregar_titulo1("Metodo de Horner")
            instancia_respuesta.agregar_parrafo(f"Funcion ingresada: {f_x}")
            instancia_respuesta.agregar_parrafo(f"X0: {x0}")
            instancia_respuesta.agregar_parrafo(f"Tolerancia: {error_aceptado}")
            #instancia_respuesta.agregar_fila(["Iteracion","X0","R","S","Xi","Ea%"])
            instancia_respuesta.agregar_parrafo("Se realiza la division sintetica de la funcion ingresada, para obtener el residuo y el cociente")
            
            polinomio = f_x.as_poly(x)
            grado = polinomio.degree()
            coeficientes = [polinomio.coeff_monomial(x**i) for i in range(grado, -1, -1)]
            divsion_sinterica1 = metodo_horner.calcular_divsion_sinterica(coeficientes, x0)
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(divsion_sinterica1[0])
            instancia_respuesta.agregar_fila(divsion_sinterica1[1])
            instancia_respuesta.agregar_fila(divsion_sinterica1[2])
            R = divsion_sinterica1[-1].pop()
            instancia_respuesta.agregar_tabla()
            instancia_respuesta.agregar_parrafo(f"R = {R}")
            instancia_respuesta.crear_tabla()
            divsion_sinterica2 = metodo_horner.calcular_divsion_sinterica(divsion_sinterica1[-1], x0)
            instancia_respuesta.agregar_fila(divsion_sinterica2[0])
            instancia_respuesta.agregar_fila(divsion_sinterica2[1])
            instancia_respuesta.agregar_fila(divsion_sinterica2[2])
            instancia_respuesta.agregar_tabla()
            S = divsion_sinterica2[-1].pop()
            instancia_respuesta.agregar_parrafo(f"S = {S}")
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(["Iteracion","X0","R","S","Xi","Ea%"])
            instancia_respuesta.agregar_titulo1("Teneindo S y R, la nueva x se calcula con la formula xi = x0 - (R/S)")
            instancia_respuesta.agregar_parrafo(f"xi = {x0} - ({R}/{S})")
            x_calculado = x0 - (R/S)
            instancia_respuesta.agregar_clave_valor("xi",x_calculado)
            instancia_respuesta.agregar_parrafo("Se evalua el error aproximado y se vuelve a iterar hasta que el error sea menor a la tolerancia")
            instancia_respuesta.agregar_titulo1("Resultados")
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
                instancia_respuesta.agregar_fila([iteracion, x0, R, S, x_calculado, error_acomulado.evalf()])
                if error_acomulado < error_aceptado:
                    break
                f_x0 = x - x_calculado #- para que cambie el signo 
                x0 = x_calculado

            instancia_respuesta.agregar_tabla()
            instancia_respuesta.agregar_clave_valor("Raiz",x_calculado)
            instancia_respuesta.agregar_parrafo(f"Numero de iteraciones: {iteracion}")
            res = instancia_respuesta.obtener_y_limpiar_respuesta()
            return res, 200
        
        except:
            res = instancia_respuesta.responder_error("Error inesperado, por favor verifique los datos ingresados")
            return res, 500
        
    def calcular_divsion_sinterica(coeficientes, divisor):
        divicion_sintetica = []
        divicion_sintetica.append(coeficientes) #Agregamos los coeficientes originales
        divicion_sintetica.append([0]*len(coeficientes)) #Agregamos los coeficientes de la divicion
        divicion_sintetica.append([0]*len(coeficientes)) #Agregamos los coeficientes de la suma
        #incialmente estos dos ultimos todos son 0 para luego ser reemplazados
        for i in range(len(coeficientes)):
            termino = divicion_sintetica[0][i]
            coeficiente = divicion_sintetica[2][i-1] * divisor
            divicion_sintetica[1][i] = float(coeficiente)
            resultado = float(termino + coeficiente)
            divicion_sintetica[2][i] = resultado
            if i == len(coeficientes) - 1:
                #al finalizar todo el proceso retorna el arreglo (matris) con la division sintetica tal cual
                return divicion_sintetica
        
