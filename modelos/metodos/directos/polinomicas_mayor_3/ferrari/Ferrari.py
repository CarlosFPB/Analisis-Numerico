import sympy as sp
import math
from flask import jsonify
from modelos.extras.Funciones import errores, respuesta_json, verificaciones
class metodo_ferrari:    
    
     
    @staticmethod
    def calcular_ferrari(json_data):
        
        try:    
            
            x = sp.symbols('x')
            respuesta = respuesta_json()     
            
            try:
                
                #obtener los valores del json
                f_x_crudo = sp.simplify(json_data["funcion"])

                #Veificar si es polinomio
                if not verificaciones.es_polinomio(f_x_crudo):
                    resp = respuesta.responder_error("La función ingresada no es un polinomio")
                    return jsonify(resp), 400
                
                #Verificar si tiene exponente 4
                if verificaciones.obtener_grado(f_x_crudo) != 4:
                    resp = respuesta.responder_error("La función ingresada no es de grado 4")
                    return jsonify(resp), 400
                
                f_x = f_x_crudo/f_x_crudo.as_poly(x).coeffs()[0]#para convertir en 0 el coeficiente de x^4
                resultado = f_x_crudo.subs(x, 2)
                if resultado > 0:
                    pass
            except sp.SympifyError:
                resp = respuesta.responder_error("Error en la función ingresada")
                return jsonify(resp), 400
            except TypeError as e:
                resp = respuesta.responder_error("Error en la función ingresada")
                return jsonify(resp), 400
           
            respuesta.agregar_titulo1("Metodo de Ferrari")
            respuesta.agregar_parrafo("Este metodo Obtendra las raices de una funcion de grado 4")
            respuesta.agregar_parrafo("Funcion: "+str(f_x_crudo))
            respuesta.agregar_parrafo("Funcion simplificada: "+str(f_x))

            #obtiene los coeficientes de la funcion de forma descendente
            coefficientes = verificaciones.obtener_coeficientes(f_x)
            a = coefficientes[1]
            b = coefficientes[2]
            c = coefficientes[3]
            d = coefficientes[4]

            #coeficientes del polinomio
            respuesta.agregar_titulo1("Coeficientes: ")
            respuesta.agregar_parrafo("a = "+str(a))
            respuesta.agregar_parrafo("b = "+str(b))
            respuesta.agregar_parrafo("c = "+str(c))
            respuesta.agregar_parrafo("d = "+str(d))

            #calcular p y q y r
            P = (8*b - 3*a**2)/8
            Q = (a**3 - 4*a*b + 8*c)/8
            R = (-3*a**4 + 256*d - 64*a*c + 16*a**2*b)/256

            respuesta.agregar_titulo1("Calculamos P, Q y R")
            respuesta.agregar_parrafo("P = "+str(P))
            respuesta.agregar_parrafo("Q = "+str(Q))
            respuesta.agregar_parrafo("R = "+str(R))


            #contruimos la cubica
            y = sp.symbols('y')
            cubica = sp.simplify(y**3 - (P/2)*y**2 - R*y + (4*P*R - Q**2)/8)

            respuesta.agregar_titulo1("Construimos la cubica para tartaglia")
            respuesta.agregar_parrafo("Cubica: "+str(cubica))

            #encontramos a b c de tartaglia
            #encontrar los coeficientes inlcuido los coeficientes 0
            polinomio = cubica.as_poly(y)
            grado = verificaciones.obtener_grado(cubica)
            coeficientesTartaglia = verificaciones.obtener_coeficientes(cubica)
            aT = coeficientesTartaglia[1]
            bT = coeficientesTartaglia[2]
            cT = coeficientesTartaglia[3]

            #coeficientes de tartaglia
            respuesta.agregar_titulo1("Coeficientes de la cubica de tartaglia")
            respuesta.agregar_parrafo("aT = "+str(aT))
            respuesta.agregar_parrafo("bT = "+str(bT))
            respuesta.agregar_parrafo("cT = "+str(cT))

            #calculamos p y q de tartaglia y delta
            pT = (3*bT-aT**2)/3
            qT = (2*aT**3 - 9*aT*bT + 27*cT)/27
            deltaT = (qT/2)**2 + (pT/3)**3

            respuesta.agregar_titulo1("Calculamos p, q y delta de tartaglia")
            respuesta.agregar_parrafo("pT = "+str(pT))
            respuesta.agregar_parrafo("qT = "+str(qT))

            #obtener 1 raiz real
            if deltaT == 0:
                if pT==0 and qT==0:
                    #tiene raiz triple
                    xreal = (-aT/3)
                if pT*qT != 0:
                    xreal = ((-4*pT**2)/(9*qT)) - (aT/3)

            elif deltaT > 0:
                #calculamos u y v
                u = math.cbrt(-qT/2 + sp.sqrt(deltaT))
                v = math.cbrt(-qT/2 - sp.sqrt(deltaT))
                #obtenemos las raices
                xreal = u + v - (aT/3) #raiz real

            elif deltaT < 0:
                #calculamos angulo
                k = 0
                angulo = sp.acos((-qT/2)/sp.sqrt(-(pT/3)**3))
                xreal = (2*sp.sqrt(-pT/3))*sp.cos((angulo+2*k*sp.pi)/3) - (aT/3)

            respuesta.agregar_parrafo("La raiz real de tartaglia es: "+str(xreal))

            #reescribimos
            U = xreal.evalf()
            P = P
            Q = Q
            a = a

            respuesta.agregar_titulo1("Reescribimos las variables")
            respuesta.agregar_parrafo("U = "+str(U))
            respuesta.agregar_parrafo("P = "+str(P))
            respuesta.agregar_parrafo("Q = "+str(Q))
            respuesta.agregar_parrafo("a = "+str(a))

            #encontramos V
            VF = sp.sqrt(2 * U - P)
            W = -(Q/(2*VF))

            respuesta.agregar_titulo1("Encontramos V y W")
            respuesta.agregar_parrafo("V = "+str(VF))
            respuesta.agregar_parrafo("W = "+str(W))

            #encontramos las raices
            x1 = (VF + sp.sqrt(VF**2 -4*(U - W)))/2 - (a/4)
            x2 = (VF - sp.sqrt(VF**2 -4*(U - W)))/2 - (a/4)
            x3 = (-VF + sp.sqrt(VF**2 -4*(U + W)))/2 - (a/4)
            x4 = (-VF - sp.sqrt(VF**2 -4*(U + W)))/2 - (a/4)
            
            #convertir a su valor numerico
            x1 = sp.N(x1)
            x2 = sp.N(x2)
            x3 = sp.N(x3)
            x4 = sp.N(x4)

            respuesta.agregar_titulo1("Calculamos las raices")
            respuesta.agregar_clave_valor("x1", x1)
            respuesta.agregar_clave_valor("x2", x2)
            respuesta.agregar_clave_valor("x3", x3)
            respuesta.agregar_clave_valor("x4", x4)
            res = respuesta.obtener_y_limpiar_respuesta()
            return jsonify(res)
        
        except Exception as e:
            resp = respuesta.responder_error("Error interno del codigo\n"+str(e)), 500
            return jsonify(resp), 500
