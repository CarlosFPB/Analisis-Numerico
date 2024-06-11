import sympy as sp
from modelos.extras.Funciones import  respuesta_json, verificaciones
from flask import jsonify
from modelos.extras.latex import conversla


class metodo_cuadratico():
    def calcular_cuadratico(json_data):
        try:
            x = sp.symbols('x')
            instancia_respuesta = respuesta_json()
            try:
                #Ecuaion de la funcion
                f_x = conversla.latex_(json_data["latex"])
                #Verificar si es polinomio
                if not verificaciones.es_polinomio(f_x):
                    resp = instancia_respuesta.responder_error("La función ingresada no es un polinomio")
                    return jsonify(resp), 400
                resultado = f_x.subs(x, 2)
                if resultado > 0:
                    pass
            except sp.SympifyError:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            except TypeError as e:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            
            
            grado = verificaciones.obtener_grado(f_x)
            if(grado == 2):
                instancia_respuesta.agregar_titulo1("Metodo Cuadratico")
                instancia_respuesta.agregar_parrafo("Este metodo nos sirve para encontrar la raiz de una ecuacion, para ello se necesita una funcion f(x) de grado 2 y usar formula cuadratica.")
                instancia_respuesta.agregar_titulo1("Valores Iniciales")
                instancia_respuesta.agregar_parrafo(f"Funcion: {f_x}")
                instancia_respuesta.agregar_titulo1("Usando la formula cuadratica")
                instancia_respuesta.agregar_parrafo("La formula cuadratica es: x = (-b ± √(b^2 - 4ac)) / 2a")
                instancia_respuesta.agregar_parrafo("Donde a, b y c son los coeficientes de la funcion cuadratica")
                coeficientes = verificaciones.obtener_coeficientes(f_x)
                a = coeficientes[0]
                b = coeficientes[1]
                c = coeficientes[2]
                instancia_respuesta.agregar_parrafo(f"Coeficientes: a = {a}, b = {b}, c = {c}")
                instancia_respuesta.agregar_titulo1("Calculando las raices")
                instancia_respuesta.agregar_parrafo(f"Sustituyendo : x = (-{b} ± √({b}^2 - 4*{a}*{c})) / 2*{a}")
                x1 = (-b + sp.sqrt(b**2 - 4*a*c)) / 2*a
                x2 = (-b - sp.sqrt(b**2 - 4*a*c)) / 2*a
                x1 = sp.N(x1)
                x2 = sp.N(x2)
                instancia_respuesta.agregar_clave_valor("Raiz 1:",f"x = {x1}")
                instancia_respuesta.agregar_clave_valor("Raiz 2:",f"x = {x2}")
                resp = instancia_respuesta.obtener_y_limpiar_respuesta()
                return jsonify(resp), 200
            else:
                #manejar excepciones
                resp = instancia_respuesta.responder_error("La funcion no es de grado 2, es de grado "+str(grado))
                return jsonify(resp), 400
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en el codigo interno del metodo\n"+str(e))
            return jsonify(resp), 500