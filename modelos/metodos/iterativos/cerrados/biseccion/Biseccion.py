import sympy as sp
from flask import jsonify
from modelos.extras.Funciones import errores, biseccion, respuesta_json
class medoto_biseccion():

    @staticmethod
    def calcular_biseccion(json_data):
        try:
            x = sp.symbols('x')
            #instancio las respuest json
            instancia_respuesta = respuesta_json()

            #obtengo los valores del json
            try:
                f_x = sp.sympify(json_data["funcion"])
            except:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
                
            error_aceptable = float(json_data["tolerancia"])
            x1 = float(json_data["xi"])
            xu = float(json_data["xu"])
            xr = 0

            #execpciones comunes
            evaluar_x1 = f_x.subs(x,x1)
            evaluar_xu = f_x.subs(x,xu)
            if (evaluar_x1 * evaluar_xu) > 0:#no ahy un cambio de signo
                resp = instancia_respuesta.responder_error("No hay un cambio de signo en los valores iniciales")
                return jsonify(resp), 400
            
        

            condicion = ""
            iteracion =0
            xr = 0
            valor_anterior = xr
            error_acumulado = 100

            instancia_respuesta.crear_tabla()

            instancia_respuesta.agregar_titulo1("Valores Iniciales")
            instancia_respuesta.agregar_clave_valor("Funcion:",f_x)
            instancia_respuesta.agregar_clave_valor("Xi:",x1)
            instancia_respuesta.agregar_clave_valor("Xu:",xu)
            instancia_respuesta.agregar_clave_valor("Tolerancia:",error_aceptable)


            instancia_respuesta.agregar_fila(['Iteracion','X1','Xu','Xr','f(Xr)','Condicion','Error'])
            instancia_respuesta.agregar_titulo1("El calculo de la raiz se hace por la siguiente formula: ")
            instancia_respuesta.agregar_parrafo("Formula: Xr = (X1 + Xu) / 2")
            instancia_respuesta.agregar_parrafo(f"Iteracion 1: Xr = ( {x1} + {xu} ) / 2 = {biseccion.primera_aproximacion(x1,xu)}")
            instancia_respuesta.agregar_parrafo(f"Evaluar f(Xr) = {f_x.subs(x,biseccion.primera_aproximacion(x1,xu))}")
            while True:
                #primera aproximacion
                iteracion +=1
                valor_anterior = xr
                xr = biseccion.primera_aproximacion(x1,xu)
                evaluacion = biseccion.multiplicacion_evaluadas(f_x,x1,xr)
                if evaluacion > 0:
                    x1 = xr
                    condicion=">0"
                elif evaluacion < 0:
                    xu = xr
                    condicion="<0"
                else:
                    xr = xr #esta es la raiz
                    condicion="=0"
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

            instancia_respuesta.agregar_titulo1("Resultados")
            instancia_respuesta.agregar_clave_valor("Iteraciones:", iteracion)
            instancia_respuesta.agregar_clave_valor("Raiz:",xr)
            instancia_respuesta.agregar_clave_valor("Error:",error_acumulado)
            instancia_respuesta.agregar_tabla()
            #print("La raiz de la ecuacion es: ",xr)
            #print("En la iteracion #", iteracion)
            #print(f"Con un error de: {error_acumulado}%")
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except TypeError as e:
            resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
            return jsonify(resp), 400
        
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error interno del codigo\n"+str(e)), 500
            return jsonify(resp), 500

