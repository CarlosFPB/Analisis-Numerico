import sympy as sp
from modelos.extras.Funciones import  respuesta_json
from flask import jsonify

class metodo_lineal():

    def calcular_lineal(json_data):
        x = sp.symbols('x')
        instancia_respuesta = respuesta_json()
        try:
            f_x = sp.sympify(json_data["funcion"])
        except:
            return jsonify({"error":"Error en la funcion"})
    
        grado = f_x.as_poly().degree()
        if(grado == 1):
            instancia_respuesta.agregar_titulo1("Metodo de Lineal")
            instancia_respuesta.agregar_parrafo("Este metodo nos sirve para encontrar la raiz de una ecuacion, para ello se necesita una funcion f(x) de grado 1 y despejar x.")
            instancia_respuesta.agregar_titulo1("Valores Iniciales")
            instancia_respuesta.agregar_parrafo(f"Funcion: {f_x}")
            instancia_respuesta.agregar_titulo1("Despejando la funcion nos queda")
            instancia_respuesta.agregar_clave_valor("Despeje:","x = f(x)")
            solucion = sp.solve(f_x, x)
            instancia_respuesta.agregar_parrafo(f"Despeje: x = {solucion[0]}")
            respuesta = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(respuesta)
        else:
            #manejar excepciones
            return jsonify({"error":"La funcion no es de grado 1"})