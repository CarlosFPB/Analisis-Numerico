import numpy as np
import sympy as sp
from flask import jsonify
from ......extras.Funciones import errores, respuesta_json, verificaciones, commprobaciones_json
from modelos.extras.latex import conversla,conversla_html

class metodo_bairstow():
        
        
    @staticmethod
    def agregar_titulo(iteracion, mensaje, instancia_respuesta):
        if iteracion == 1:
            instancia_respuesta.agregar_parrafo(mensaje)
        return instancia_respuesta

    @staticmethod
    def agregar_parrafo(iteracion, mensaje, instancia_respuesta):
        if iteracion == 1:
            instancia_respuesta.agregar_parrafo(mensaje)
        return instancia_respuesta
    
    @staticmethod
    def agregar_clave_valor(iteracion, clave, valor, instancia_respuesta):
        if iteracion == 1:
            instancia_respuesta.agregar_clave_valor(clave, valor)
        return instancia_respuesta

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
        #Verificar la funcion obtenida
        #Verificar la funcion obtenida
        try:
            #Verificar la funcion obtenida
            response, status_code = commprobaciones_json.comprobar_funcionX_latex(json_data, instancia_respuesta)
            if status_code != 200:
                resp = response
                return resp, 400
            f_x = response
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error al obtener la función ingresada: "+str(e))
            return jsonify(resp), 400
            
        try:
            #validar que sea grado mayor a 3 y polinomica
            if verificaciones.obtener_grado(f_x) != None:#es porq es polinomica
                if verificaciones.obtener_grado(f_x) <3:
                    resp = instancia_respuesta.responder_error("La función debe ser polinomica de grado 3 o mayor")
                    return jsonify(resp), 400
            else:#no es polinomica por ende ni tiene grado mayor a 3
                resp = instancia_respuesta.responder_error("La función debe ser polinomica de grado 3 o mayor")
                return jsonify(resp), 400
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
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
        
        try:
            #empezamos con el metodo de bairstow
            x_aproximada = []
            iteracion = 0
            instancia_respuesta.agregar_titulo1("Metodo de Bairstow")
            instancia_respuesta.agregar_parrafo("Los datos ingresados son los siguientes:")
            instancia_respuesta.agregar_parrafo("Funcion: " + str(f_x))
            instancia_respuesta.agregar_parrafo("Tolerancia: " + str(error_aceptado))
            instancia_respuesta.agregar_parrafo("r0: " + str(r0))
            instancia_respuesta.agregar_parrafo("s0: " + str(s0))
            instancia_respuesta.agregar_titulo1("Se calculan los coeficientes de b y c")
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
                ite = len(coeficientes_b)
                for b in coeficientes_b:
                    metodo_bairstow.agregar_clave_valor(iteracion, f"b{ite}" , str(b), instancia_respuesta)
                    ite -= 1

                #calcular valores de c
                coeficientes_c = []
                for i in range(len(coeficientes_b) - 1):
                    if i == 0:
                        coeficientes_c.append(coeficientes_b[i])
                    elif i == 1:
                        coeficientes_c.append(coeficientes_b[i] + r0*coeficientes_c[0])
                    else:
                        coeficientes_c.append(coeficientes_b[i] + r0*coeficientes_c[i-1] + s0*coeficientes_c[i-2])

                ite = len(coeficientes_c)
                for c in coeficientes_c:
                    metodo_bairstow.agregar_clave_valor(iteracion, f"c{ite}" , str(c), instancia_respuesta)
                    ite -= 1

                # determinar delta r y delta s
                dr, ds = sp.symbols('dr ds')
                ecuacion1 = coeficientes_c[-2] * dr + coeficientes_c[-3] * ds + coeficientes_b[-2]
                ecuacion2 = coeficientes_c[-1] * dr + coeficientes_c[-2] * ds + coeficientes_b[-1]
                if ecuacion1 == 0 and ecuacion2 == 0:
                    solucion = {dr: 0, ds: 0}
                else:
                    solucion = sp.solve([ecuacion1, ecuacion2], (dr, ds))
                if len(solucion) == 0:
                    solucion = {dr: 0, ds: 0}
                solucion[dr] = sp.N(solucion[dr])
                solucion[ds] = sp.N(solucion[ds])
                metodo_bairstow.agregar_titulo(iteracion, "Se calculan los valores de dr y ds", instancia_respuesta)
                metodo_bairstow.agregar_clave_valor(iteracion, "dr", str(solucion[dr]), instancia_respuesta)
                metodo_bairstow.agregar_clave_valor(iteracion, "ds", str(solucion[ds]), instancia_respuesta)
                #cambiar r y s
                r0 = r0 + solucion[dr]
                s0 = s0 + solucion[ds]
                r0 = sp.N(r0)
                s0 = sp.N(s0)
                metodo_bairstow.agregar_titulo(iteracion, "Se calculan los nuevos valores de r y s", instancia_respuesta)
                metodo_bairstow.agregar_clave_valor(iteracion, "r", str(r0), instancia_respuesta)
                metodo_bairstow.agregar_clave_valor(iteracion, "s", str(s0), instancia_respuesta)
                #comprobar error
                if r0 == 0 and s0 == 0:
                    resp = instancia_respuesta.responder_error("Error r0 y s0 = 0 ahy divicion entre 0 por lo tanto el metodo no puede continuar")
                    return jsonify(resp), 400
                if r0 == 0:
                    error_r = abs(solucion[dr])*100
                    resp = instancia_respuesta.responder_error("Error r0 = 0 ahy divicion entre 0 por lo tanto el metodo no puede continuar")
                    return jsonify(resp), 400
                else:
                    error_r = abs(solucion[dr] / r0)*100
                if s0 == 0:
                    error_s = abs(solucion[ds])
                    resp = instancia_respuesta.responder_error("Error s0 = 0 ahy divicion entre 0 por lo tanto el metodo no puede continuar")
                    return jsonify(resp), 400
                else: 
                    error_s = abs(solucion[ds] / s0) 
                metodo_bairstow.agregar_titulo(iteracion, "Se calculan los errores relativos", instancia_respuesta)
                metodo_bairstow.agregar_clave_valor(iteracion, "error_r", str(error_r), instancia_respuesta)
                metodo_bairstow.agregar_clave_valor(iteracion, "error_s", str(error_s), instancia_respuesta)
                metodo_bairstow.agregar_parrafo(iteracion, "Se comprueba si los errores son menores a la tolerancia sino lo es se vuleve a iterar", instancia_respuesta)
                if error_r < error_aceptado and error_s < error_aceptado:
                    metodo_bairstow.agregar_titulo(iteracion,"Los errores son menores a la tolerancia se procede a calcular las raices iniciales", instancia_respuesta)
                    x_aproximada.append((r0 + sp.sqrt((r0**2) + (4 * s0))) / 2)
                    x_aproximada.append((r0 - sp.sqrt((r0**2) + (4 * s0))) / 2)
                    metodo_bairstow.agregar_parrafo(iteracion, "La formula de las raices iniciales es la siguiente: ", instancia_respuesta)
                    metodo_bairstow.agregar_parrafo(iteracion, "x1 = (r0 + sqrt(r0^2 + 4 * s0)) / 2", instancia_respuesta)
                    metodo_bairstow.agregar_parrafo(iteracion, "x2 = (r0 - sqrt(r0^2 + 4 * s0)) / 2", instancia_respuesta)
                    metodo_bairstow.agregar_parrafo(iteracion, "Los valores de x son: ", instancia_respuesta)
                    for i in range(len(x_aproximada)):
                        metodo_bairstow.agregar_parrafo(iteracion, "x"+str(i+1) + " = " + str(x_aproximada[i]), instancia_respuesta)
                    
                    #dividir polinomio
                    divisor = (x - x_aproximada[-1]) * (x - x_aproximada[-2])
                    cociente, residuo = sp.div(f_x, divisor)
                    metodo_bairstow.agregar_titulo(iteracion, f"Se procede a dividir el polinomio entre {divisor}", instancia_respuesta)
                    condicion = cociente.as_poly(x).degree()
                    metodo_bairstow.agregar_titulo(iteracion, "Se comprueba el grado del polinomio", instancia_respuesta)
                    if condicion >= 3:
                        #volvemos plicar bairstow
                        f_x = cociente

                        metodo_bairstow.agregar_titulo(iteracion, "Se vuelve a aplicar el metodo de bairstow porque el polinomio es mayor o igual a 3", instancia_respuesta)
                    elif condicion == 2:
                        #aplicar formula cuadratica
                        coefficientes = verificaciones.obtener_coeficientes(cociente)
                        a = coefficientes[0]
                        b = coefficientes[1]
                        c = coefficientes[2]
                        x_aproximada.append((-b + (sp.sqrt((b**2) - (4 * a * c)))) / (2 * a))
                        x_aproximada.append((-b - (sp.sqrt((b**2) - (4 * a * c)))) / (2 * a))
                        metodo_bairstow.agregar_titulo(iteracion, "Grado igual a 2, Se aplica la formula cuadratica para obtener las raices restantes", instancia_respuesta)
                        break
                    elif condicion == 1:
                        #aplicar formula lineal
                        metodo_bairstow.agregar_titulo(iteracion, f"Grado igual a 1, Se aplica la formula x = -s0/r0 para obtener la raiz restante", instancia_respuesta)
                        x_aproximada.append((-s0 / r0))
                        break
                    else:
                        break
                        #terminar
                if iteracion > 300:
                    resp = instancia_respuesta.responder_error("El metodo sobrepaso la cantidad de iteraciones permitidas")
                    return jsonify(resp), 400
                
            #retornar los resultados
            instancia_respuesta.agregar_titulo1("Los resultados obtenidos son los siguientes:")
            instancia_respuesta.agregar_parrafo("Los valores de x son: ")
            for i in range(len(x_aproximada)):
                instancia_respuesta.agregar_clave_valor("x"+str(i+1) + " = ", str(x_aproximada[i]))
            instancia_respuesta.agregar_parrafo("Numero de iteraciones: " + str(iteracion))
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en el codigo interno del metodo de bairstow" + str(e))
            return jsonify(resp), 400

 
