import sympy as sp
from flask import jsonify
from .....extras.Funciones import errores, falsaPosicion, respuesta_json


class falsa_posicion():

    def calcular_falsa_posicion(json_data):
        x = sp.symbols('x')

        #instancio las respuest json
        instancia_respuesta = respuesta_json()

        #obtengo los valores del json
        try:
            f_x = sp.sympify(json_data["funcion"])
        except:
            return {"error":"Error en la funcion"}
        
        error_aceptable = float(json_data["tolerancia"])
        x1 = float(json_data["xi"])
        xu = float(json_data["xu"])
        xr = 0
        condicion = ""

        #execpciones comunes
        evaluar_x1 = f_x.subs(x,x1)
        evaluar_xu = f_x.subs(x,xu)
        if (evaluar_x1 * evaluar_xu) > 0:#no ahy un cambio de signo
            print("No hay un cambio de signo en los valores iniciales")
            return {"error":"No hay un cambio de signo en los valores iniciales"}

        instancia_respuesta.agregar_titulo1("Metodo de Falsa Posicion")
        instancia_respuesta.agregar_parrafo("Este metodo nos sirve para encontrar la raiz de una ecuacion, para ello se necesita una funcion f(x) continua en un intervalo [a,b] que contenga a la raiz.")
        instancia_respuesta.crear_tabla()
        instancia_respuesta.agregar_titulo1("Valores Iniciales")
        instancia_respuesta.agregar_parrafo(f"Funcion: {f_x}")
        instancia_respuesta.agregar_parrafo(f"Xi: {x1}")
        instancia_respuesta.agregar_parrafo(f"Xu: {xu}")
        instancia_respuesta.agregar_parrafo(f"Tolerancia: {error_aceptable}")
        instancia_respuesta.agregar_fila(['Iteracion','X1','Xu','Xr','f(Xr)','Condicion','Error'])
        instancia_respuesta.agregar_titulo1("El calculo de la raiz se hace por la siguiente formula: ")
        instancia_respuesta.agregar_clave_valor("Formula:","Xr = Xu - ( f(Xu) * (X1 - Xu) ) / ( f(X1) - f(Xu) )")
        instancia_respuesta.agregar_parrafo(f"Iteracion 1: Xr = {xu} - ( f({xu}) * ({x1} - {xu}) ) / ( f({x1}) - f({xu}) ) = {falsaPosicion.primera_aproximacion(f_x,x1,xu)}")
        while True:
            iteracion =1
            valor_anterior = xr
            xr = falsaPosicion.primera_aproximacion(f_x,x1,xu)
            #primera aproximacion
            evaluacion = falsaPosicion.multiplicacion_evaluadas(f_x,x1,xr)
            if evaluacion > 0:
                condicion=">0"
                x1 = xr
            elif evaluacion < 0:
                condicion="<0"
                xu = xr
            else:
                xr = xr
                xr = xr #ya encontre la raiz
                error_acumulado = 0
                instancia_respuesta.agregar_fila([iteracion,x1,xu,xr,evaluacion,condicion,error_acumulado])
                break

            if not iteracion == 1:
                #print(f"valor anterior {valor_anterior} valor actual {xr}")
                error_acumulado = errores.error_aproximado_porcentual(valor_anterior,xr)
                #print(error_acumulado)
                if error_acumulado < error_aceptable:
                    instancia_respuesta.agregar_fila([iteracion,x1,xu,xr,evaluacion,condicion,error_acumulado])
                    break
            instancia_respuesta.agregar_fila([iteracion,x1,xu,xr,evaluacion,condicion,error_acumulado])

        instancia_respuesta.agregar_titulo1("Resultados: ")
        instancia_respuesta.agregar_clave_valor("Iteraciones: ",iteracion)
        instancia_respuesta.agregar_clave_valor("Raiz: ",xr)
        instancia_respuesta.agregar_clave_valor("Error: ",error_acumulado)
        instancia_respuesta.agregar_tabla()
        res = instancia_respuesta.obtener_y_limpiar_respuesta()
        return res
