from flask import jsonify
import sympy as sp
import numpy as np
from ....extras.Funciones import respuesta_json, verificaciones
from ....extras.Integrales import verificacion_puntos_tabla


class metodo_multiple_tabla():
    @staticmethod 
    def calcular_multiple_tabla(json_data):
        try:
            instancia_respuesta = respuesta_json()
            try:
                matrizPuntos = json_data["matrizPuntos"]
                #verificar si la matriz de puntos es valida
                if not verificaciones.es_matriz(matrizPuntos):
                    resp = instancia_respuesta.responder_error("La matriz de puntos no es valida")
                    return jsonify(resp), 400
            except:
                resp = instancia_respuesta.responder_error("Error en los datos ingresados")
                return jsonify(resp), 400
            

            #Parsear tabla y comprobar errores
            tabla_matriz = verificacion_puntos_tabla.verificar_tabla(matrizPuntos)

            if isinstance(tabla_matriz, str):
                #Caso error
                resp  = instancia_respuesta.responder_error(tabla_matriz)
                return jsonify(resp), 400
            else: 
                puntos_x, puntos_y = tabla_matriz

           
            #Verificar si los puntos x tiene el mismo valor de h, abarca enteros y decimales
           # incremento = float(puntos_x[1] - puntos_x[0])
            #for i in range(len(puntos_x)-1):
             #   if round(puntos_x[i+1] - puntos_x[i], 10) != incremento:
              #      resp = instancia_respuesta.responder_error(f"Se encontro diferente ancho en un punto de x (el punto{puntos_x[i+1]} con el punto {puntos_x[i]})")
               #     return jsonify(resp), 400

            def aplicar_trapecio_simple(indices, puntos_x, puntos_y):
                x0, x1 = puntos_x[indices[0]], puntos_x[indices[1]]
                y0, y1 = puntos_y[indices[0]], puntos_y[indices[1]]
                h = x1 - x0
                return (h / 2) * (y0 + y1)

            def aplicar_simpson_1_3(indices, puntos_x, puntos_y):
                x0, x1, x2 = puntos_x[indices[0]], puntos_x[indices[1]], puntos_x[indices[2]]
                y0, y1, y2 = puntos_y[indices[0]], puntos_y[indices[1]], puntos_y[indices[2]]
                h = (x2 - x0) / 2
                return (h / 3) * (y0 + 4 * y1 + y2)

            def aplicar_simpson_3_8(indices, puntos_x, puntos_y):
                x0, x1, x2, x3 = puntos_x[indices[0]], puntos_x[indices[1]], puntos_x[indices[2]], puntos_x[indices[3]]
                y0, y1, y2, y3 = puntos_y[indices[0]], puntos_y[indices[1]], puntos_y[indices[2]], puntos_y[indices[3]]
                h = (x3 - x0) / 3
                return (3 * h / 8) * (y0 + 3 * y1 + 3 * y2 + y3)

            n = len(puntos_x)
            i = 0
            resultado = 0
            intervalos = []
            instancia_respuesta.agregar_titulo1("Metodo de la tabla multiple")
            while i < n - 1:
                j = i
                h = puntos_x[j + 1] - puntos_x[j]
                indices = [j]
                
                while j < n - 1 and puntos_x[j + 1] - puntos_x[j] == h:
                    j += 1
                    indices.append(j)
                
                m = len(indices) - 1
                
                while m >= 3:
                    if m >= 3:
                        resultado += aplicar_simpson_3_8(indices[:4], puntos_x, puntos_y)
                        instancia_respuesta.agregar_parrafo(f"Intervalos, ([{puntos_x[indices[0]]}, {puntos_x[indices[3]]}], Simpson 3/8 Simple)")
                        indices = indices[3:]
                        m -= 3
                
                while m >= 2:
                    if m >= 2:
                        resultado += aplicar_simpson_1_3(indices[:3], puntos_x, puntos_y)
                        instancia_respuesta.agregar_parrafo(f"Intervalos, ([{puntos_x[indices[0]]}, {puntos_x[indices[2]]}], Simpson 1/3 Simple)")
                        indices = indices[2:]
                        m -= 2
                
                if len(indices) > 1:
                    for k in range(1, len(indices)):
                        resultado += aplicar_trapecio_simple(indices[k-1:k+1], puntos_x, puntos_y)
                        instancia_respuesta.agregar_parrafo(f"Intervalos, ([{puntos_x[indices[k-1]]}, {puntos_x[indices[k]]}], Trapecio Simple)")
                
                i = indices[-1]

            instancia_respuesta.agregar_clave_valor("Resultado", resultado)
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = instancia_respuesta.responder_error(f"Error interno en el servidor" )
            return jsonify(resp), 500
