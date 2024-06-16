import sympy as sp
import math
from modelos.extras.Funciones import respuesta_json, verificaciones
from flask import jsonify
from modelos.extras.latex import conversla

class metodo_tartaglia:
    
    def calcular_tartaglia(json_data):
        try:
            x = sp.symbols('x')
            x1 = 0
            x2 = 0
            x3 = 0
            #istanciar la respuesta
            respuesta = respuesta_json()

            #Verificar la funcion obtenida
            try:
                #Ecuaion de la funcion
                f_x_crudo = conversla.latex_(json_data["latex"])
                f_x_crudo = sp.expand(f_x_crudo)#para que se vea bien la funcion
                #Verificar si es polinomio
                if not verificaciones.es_polinomio(f_x_crudo):
                    resp = respuesta.responder_error("La función ingresada no es un polinomio")
                    return jsonify(resp), 400
                resultado = f_x_crudo.subs(x, 2)
                if resultado > 0:
                    pass
            except sp.SympifyError:
                resp = respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            except TypeError as e:
                resp = respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            
            f_x = f_x_crudo/f_x_crudo.as_poly(x).coeffs()[0]
            respuesta.agregar_titulo1("Método de Tartaglia")
            respuesta.agregar_parrafo("Se busca encontrar las raíces de la ecuación polinómica de grado 3: ")

            #encontrar los coeficientes inlcuido los coeficientes 0
            grado = verificaciones.obtener_grado(f_x)
            #evaluo el grado antes de avanzar
            if grado != 3:
                resp = respuesta.responder_error("El polinomio debe ser de grado 3 y este es de grado "+str(grado))
                return jsonify(resp), 400
            coeficientes = verificaciones.obtener_coeficientes(f_x)
            a = coeficientes[1]
            b = coeficientes[2]
            c = coeficientes[3]

            respuesta.agregar_titulo1("coeficientes de la funcion")
            respuesta.agregar_parrafo("a = " + str(a))
            respuesta.agregar_parrafo("b = " + str(b))
            respuesta.agregar_parrafo("c = " + str(c))

            #calculamos p y q
            p = (3*b-a**2)/3
            q = (2*a**3 - 9*a*b + 27*c)/27

            respuesta.agregar_titulo1("Calculo de p y q")
            funcion_str = "p = (3*b-a^2)/3"
            respuesta.agregar_parrafo(funcion_str)
            respuesta.agregar_parrafo("p = " + str(p))
            funcion_str = "q = (2*a^3 - 9*a*b + 27*c)/27"
            respuesta.agregar_parrafo(funcion_str)
            respuesta.agregar_parrafo("q = " + str(q))

            #discriminante
            delta = (q/2)**2 + (p/3)**3
            
            respuesta.agregar_titulo1("Calculo del discriminante")
            respuesta.agregar_parrafo("delta = (q/2)^2 + (p/3)^3")
            respuesta.agregar_parrafo("delta = " + str(delta))
            respuesta.agregar_titulo1("Calculamos las raices")
            #obtener las raices
            if delta == 0:
                if p==0 and q==0:
                    #tiene raiz triple
                    x1 = x2 = x3 = (-a/3)
                    respuesta.agregar_titulo1(" p = q = 0")
                    respuesta.agregar_parrafo("Raiz triple")
                    respuesta.agregar_parrafo("x1 = x2 = x3 = -a/3")
                if p*q != 0:
                    x1 = x2 = (-(3*q)/(2*p)) - (a/3) #raiz doble
                    x3 = ((-4*p**2)/(9*q)) - (a/3)
                    respuesta.agregar_titulo1(" p*q != 0")
                    respuesta.agregar_parrafo("Raiz doble")
                    respuesta.agregar_parrafo("x1 = x2 = (-(3*q)/(2*p)) - (a/3)")
                    respuesta.agregar_parrafo("x3 = ((-4*p^2)/(9*q)) - (a/3)")

            elif delta > 0:
                #calculamos u y v
                u = math.cbrt(-q/2 + sp.sqrt(delta))
                v = math.cbrt(-q/2 - sp.sqrt(delta))
                #obtenemos las raices
                x1 = u + v - (a/3) #raiz real
                x2 = -(u+v)/2 - (a/3) + (u-v)*sp.sqrt(3)/2j #raices imaginarias
                x3 = -(u+v)/2 - (a/3) - (u-v)*sp.sqrt(3)/2j
                respuesta.agregar_titulo1("delta > 0")
                respuesta.agregar_parrafo("Calculamos u y v")
                respuesta.agregar_parrafo("u = cbrt(-q/2 + sqrt(delta))")
                respuesta.agregar_parrafo("v = cbrt(-q/2 - sqrt(delta))")
                respuesta.agregar_parrafo("Raiz real")
                respuesta.agregar_parrafo("x1 = u + v - (a/3)")
                respuesta.agregar_parrafo("Raices imaginarias")
                respuesta.agregar_parrafo("x2 = -(u+v)/2 - (a/3) + (u-v)*sqrt(3)/2j")
                respuesta.agregar_parrafo("x3 = -(u+v)/2 - (a/3) - (u-v)*sqrt(3)/2j")

            elif delta < 0:
                #calculamos angulo
                k = 0
                angulo = sp.acos((-q/2)/sp.sqrt(-(p/3)**3))
                x1 = (2*math.sqrt(-p/3))*sp.cos((angulo+2*k*sp.pi)/3) - (a/3)
                k = 1
                x2 = (2*math.sqrt(-p/3))*sp.cos((angulo+2*k*sp.pi)/3) - (a/3)
                k = 2
                x3 = (2*math.sqrt(-p/3))*sp.cos((angulo+2*k*sp.pi)/3) - (a/3)
                respuesta.agregar_titulo1("delta < 0")
                respuesta.agregar_parrafo("Calculamos el angulo")
                respuesta.agregar_parrafo("angulo = acos((-q/2)/sqrt(-(p/3)^3)")
                respuesta.agregar_parrafo("Raices")
                respuesta.agregar_parrafo("x1 = (2*sqrt(-p/3))*cos((angulo+2*k*pi)/3) - (a/3)")
                respuesta.agregar_parrafo("x2 = (2*sqrt(-p/3))*cos((angulo+2*k*pi)/3) - (a/3)")
                respuesta.agregar_parrafo("x3 = (2*sqrt(-p/3))*cos((angulo+2*k*pi)/3) - (a/3)")

            #convertir sus valores nuemricos
            x1 = sp.N(x1)
            x2 = sp.N(x2)
            x3 = sp.N(x3)

            respuesta.agregar_titulo1("Respuesta: ")
            respuesta.agregar_clave_valor("x1= ", x1)
            respuesta.agregar_clave_valor("x2= ", x2)
            respuesta.agregar_clave_valor("x3= ", x3)
            resp = respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = respuesta.responder_error("Error en el codigo interno\n"+str(e))
            return jsonify(resp), 500

