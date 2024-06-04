import numpy as np
import sympy as sp
from flask import jsonify
from ......extras.Funciones import errores, respuesta_json, verificaciones


class metodo_bairstow():

    def format(number):
        return str(float(number))

    #funcion encargada de realizar la divicion sintetica
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
            

    def calcular_bairstow(json_data):
        x = sp.symbols("x")
        instancia_respuesta = respuesta_json()
        #Verificar la funcion obtenida
        try:
            #Ecuaion de la funcion
            f_x = sp.sympify(json_data["funcion"])
            resultado = f_x.subs(x, 2)
            if resultado > 0:
                pass
        except sp.SympifyError:
            resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
            return jsonify(resp), 400
        except TypeError as e:
            resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
            return jsonify(resp), 400
            
        #validar que sea grado mayor a 3 y polinomica
        if verificaciones.obtener_grado(f_x) != None:#es porq es polinomica
            if verificaciones.obtener_grado(f_x) <3:
                resp = instancia_respuesta.responder_error("La función debe ser polinomica de grado 3 o mayor")
                return jsonify(resp), 400
        else:#no es polinomica por ende ni tiene grado mayor a 3
            resp = instancia_respuesta.responder_error("La función debe ser polinomica de grado 3 o mayor")
            return jsonify(resp), 400
                   
        try:
            error_aceptado = float(json_data["tolerancia"])
            r0 = float(json_data["r0"])
            s0 = float(json_data["s0"])
        except ValueError as e:
            resp = instancia_respuesta.responder_error("Error en los datos ingresados" + str(e))
            return jsonify(resp), 400
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en los datos ingresados" + str(e))
            return jsonify(resp), 400
        
        #empezamos con el metodo de bairstow
        x_aproximada = []
        iteracion = 0
        while True:
            iteracion += 1
            coeficientes = verificaciones.obtener_coeficientes(f_x)
            coeficiente_grado_mayor = coeficientes[0]
            if coeficiente_grado_mayor != 1:
                f_x = f_x/coeficiente_grado_mayor
                coeficientes = verificaciones.obtener_coeficientes(f_x)
            #calcualr valores de b
            coeficientes_b = []
            for i in range(len(coeficientes)):
                if i == 0:
                    coeficientes_b.append(coeficientes[i])
                elif i == 1:
                    coeficientes_b.append(coeficientes[i] + r0*coeficientes_b[0])
                else:
                    coeficientes_b.append(coeficientes[i] + r0*coeficientes_b[i-1] + s0*coeficientes_b[i-2])
            #calcular valores de c
            coeficientes_c = []
            for i in range(len(coeficientes_b) - 1):
                if i == 0:
                    coeficientes_c.append(coeficientes_b[i])
                elif i == 1:
                    coeficientes_c.append(coeficientes_b[i] + r0*coeficientes_c[0])
                else:
                    coeficientes_c.append(coeficientes_b[i] + r0*coeficientes_c[i-1] + s0*coeficientes_c[i-2])
            # determinar delta r y delta s
            dr, ds = sp.symbols('dr ds')
            ecuacion1 = coeficientes_c[-2] * dr + coeficientes_c[-3] * ds + coeficientes_b[-2]
            ecuacion2 = coeficientes_c[-1] * dr + coeficientes_c[-2] * ds + coeficientes_b[-1]
            solucion = sp.solve([ecuacion1, ecuacion2], (dr, ds))
            #cambiar r y s
            r0 = r0 + solucion[dr]
            s0 = s0 + solucion[ds]
            #comprobar error
            error_r = abs(solucion[dr] / r0) 
            error_s = abs(solucion[ds] / s0) 
            if error_r < error_aceptado and error_s < error_aceptado:
                r0 = sp.N(r0)
                s0 = sp.N(s0)
                x_aproximada.append((r0 + sp.sqrt((r0**2) + (4 * s0))) / 2)
                x_aproximada.append((r0 - sp.sqrt((r0**2) + (4 * s0))) / 2)
                #dividir polinomio
                cociente, residuo = sp.div(f_x, (x - x_aproximada[-1]) * (x - x_aproximada[-2]))
                condicion = cociente.as_poly(x).degree()
                if condicion >= 3:
                    #volvemos plicar bairstow
                    print("Volver a aplicar bairstow")
                elif condicion == 2:
                    #aplicar formula cuadratica
                    coefficientes = sp.Poly(cociente).coeffs()
                    a = coefficientes[0]
                    b = coefficientes[1]
                    c = coefficientes[2]
                    x_aproximada.append((-b + (sp.sqrt((b**2) - (4 * a * c)))) / (2 * a))
                    x_aproximada.append((-b - (sp.sqrt((b**2) - (4 * a * c)))) / (2 * a))
                    break
                elif condicion == 1:
                    #aplicar formula lineal
                    x_aproximada.append((-s0 / r0))
                    break
                else:
                    break
                    #terminar
            if iteracion > 100:
                resp = instancia_respuesta.responder_error("El metodo no converge")
                return jsonify(resp), 400
            #sino volver a 
            
        #retornar los resultados
        instancia_respuesta.agregar_titulo("Metodo de Bairstow itreacion #" + str(iteracion))
        instancia_respuesta.agregar_parrafo("Los resultados obtenidos son los siguientes:")
        instancia_respuesta.agregar_parrafo("Los valores de x son: ")
        for i in range(len(x_aproximada)):
            instancia_respuesta.agregar_parrafo("x"+str(i+1) + " = " + str(x_aproximada[i]))
        resp = instancia_respuesta.obtener_y_limpiar_respuesta()
        return jsonify(resp), 200


 
