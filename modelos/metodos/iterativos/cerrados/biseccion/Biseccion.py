import sympy as sp
from flask import jsonify
from modelos.extras.Funciones import errores, biseccion, respuesta_json

class medoto_biseccion():

    @staticmethod
    def calcular_biseccion(json_data):
        x = sp.symbols('x')

        #obtengo los valores del json
        f_x = sp.sympify(json_data["funcion"])
            
        error_aceptable = float(json_data["tolerancia"])
        x1 = float(json_data["xi"])
        xu = float(json_data["xu"])
        xr = 0

        #instancio las respuest json
        instancia_respuesta = respuesta_json()

        condicion = ""
        iteracion =0
        xr = 0
        valor_anterior = xr
        error_acumulado = 100

        instancia_respuesta.agregar_titulo1("Metodo de Biseccion")
        instancia_respuesta.agregar_parrafo("Este metodo nos sirve para encontrar la raiz de una ecuacion, para ello se necesita una funcion f(x) continua en un intervalo [a,b] que contenga a la raiz.")
        instancia_respuesta.crear_tabla()
        instancia_respuesta.agregar_fila(['Iteracion','X1','Xu','Xr','f(Xr)','Condicion','Error'])
        while True:
            #primera aproximacion
            iteracion +=1
            xr = biseccion.primera_aproximacion(x1,xu)
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
            instancia_respuesta.agregar_fila([iteracion,x1,xu,xr,evaluacion,condicion,error_acumulado])
            valor_anterior = xr

        instancia_respuesta.agregar_tabla()
        #print("La raiz de la ecuacion es: ",xr)
        #print("En la iteracion #", iteracion)
        #print(f"Con un error de: {error_acumulado}%")
        res = instancia_respuesta.obtener_y_limpiar_respuesta()
        return jsonify(res)

