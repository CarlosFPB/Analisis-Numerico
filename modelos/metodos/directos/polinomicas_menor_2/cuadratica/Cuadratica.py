import sympy as sp
from modelos.extras.Funciones import  respuesta_json
from flask import jsonify

class metodo_cuadratico():
    def calcular_cuadratico(json_data):
        try:
            x = sp.symbols('x')
            instancia_respuesta = respuesta_json()
            try:
                f_x = sp.sympify(json_data["funcion"])
            except:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            grado = f_x.as_poly().degree()
            if(grado == 2):
                instancia_respuesta.agregar_titulo1("Metodo Cuadratico")
                instancia_respuesta.agregar_parrafo("Este metodo nos sirve para encontrar la raiz de una ecuacion, para ello se necesita una funcion f(x) de grado 2 y usar formula cuadratica.")
                instancia_respuesta.agregar_titulo1("Valores Iniciales")
                instancia_respuesta.agregar_parrafo(f"Funcion: {f_x}")
                instancia_respuesta.agregar_titulo1("Usando la formula cuadratica")
                instancia_respuesta.agregar_parrafo("La formula cuadratica es: x = (-b ± √(b^2 - 4ac)) / 2a")
                instancia_respuesta.agregar_parrafo("Donde a, b y c son los coeficientes de la funcion cuadratica")
                polinomio = f_x.as_poly(x)
                grado = polinomio.degree()
                coeficientes = [polinomio.coeff_monomial(x**i) for i in range(grado, -1, -1)]#aunq haya 0
                a = coeficientes[0]
                b = coeficientes[1]
                c = coeficientes[2]
                instancia_respuesta.agregar_parrafo(f"Coeficientes: a = {a}, b = {b}, c = {c}")
                instancia_respuesta.agregar_titulo1("Calculando las raices")
                instancia_respuesta.agregar_parrafo(f"Sustituyendo : x = (-{b} ± √({b}^2 - 4*{a}*{c})) / 2*{a}")
                resp = (-b + sp.sqrt(b**2 - 4*a*c)) / 2*a
                resp2 = (-b - sp.sqrt(b**2 - 4*a*c)) / 2*a
                instancia_respuesta.agregar_clave_valor("Raiz 1:",f"x = {resp}")
                instancia_respuesta.agregar_clave_valor("Raiz 2:",f"x = {resp2}")
                respuesta = instancia_respuesta.obtener_y_limpiar_respuesta()
                return jsonify(respuesta), 200
            else:
                #manejar excepciones
                resp = instancia_respuesta.responder_error("La funcion no es de grado 2, es de grado "+str(grado))
                return jsonify(resp), 400
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en el codigo interno del metodo\n"+str(e))
            return jsonify(resp), 500