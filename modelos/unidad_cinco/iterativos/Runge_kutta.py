import sympy as sp
from flask import jsonify
from modelos.extras.Formulas_multipasos import runge_kutta
from modelos.extras.Funciones import verificaciones, respuesta_json

class metodo_runge_kutta():

    def calcular_metodo_runge_kutta(json_data):
        x = sp.symbols('x')
        y = sp.symbols('y')
        instancia_respuesta = respuesta_json()
        # Se obtienen los datos del json
        try:
            x0 = float(json_data['xinicial'])
            y0 = float(json_data['yinicial'])
            h = float(json_data['h'])
            x_buscado = float(json_data['xfinal'])
            if verificaciones.es_entero(json_data['orden']):
                orden = int(json_data['orden'])
                if orden <2 or orden > 4:
                    resp = instancia_respuesta.responder_error("El orden debe ser 2, 3 o 4")
                    return jsonify(resp), 400
            else:
                resp = instancia_respuesta.responder_error("El numero de orden debe ser un entero entre (2 y 4)")
                return jsonify(resp), 400
            try:
                f_x = sp.simplify(json_data["funcion"])
                rs = f_x.subs(x, 2).subs(y, 3)
                if rs > 0:
                    pass
            except sp.SympifyError:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            except Exception as e:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
        except ValueError as e:
            resp = instancia_respuesta.responder_error(f"Error de conversión de datos {e}")
            return jsonify(resp), 400
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en los datos: "+str(e))
            return jsonify(resp), 400

        try:
            lista_x = []
            lista_y = []
            #se aplica el metodo de runge kutta
            #se agregan los datos iniciales
            lista_x.append(x0)
            lista_y.append(y0)
            #llenar lista x hasta el x buscado
            xs = x0
            while True:
                xs = round(xs + h, 8)
                lista_x.append(xs)
                print(xs, x_buscado)
                if xs >= (x_buscado):
                    break
            if x_buscado != lista_x[-1]:
                resp = instancia_respuesta.responder_error("No se puede llegar al valor buscado con el tamanho de paso dado")
                return jsonify(resp), 400
            n = len(lista_x)
            if orden == 2:
                for i in range(0, n-1):
                    lista_y.append(runge_kutta.orden_2(lista_x[i], lista_y[i], h, f_x)['yi_siguiente'])
            elif orden == 3:
                for i in range(0, n-1):
                    lista_y.append(runge_kutta.orden_3(lista_x[i], lista_y[i], h, f_x)['yi_siguiente'])
            elif orden == 4:
                for i in range(0, n-1):
                    lista_y.append(runge_kutta.orden_4(lista_x[i], lista_y[i], h, f_x)['yi_siguiente'])

            instancia_respuesta.agregar_parrafo("Los valores de y son: "+str(lista_y))
            instancia_respuesta.agregar_clave_valor(f"el valor de x buscado es: {x_buscado},{lista_x[-1]}", f"el valor de y buscado es: {lista_y[-1]}")
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en el metodo de Runge Kutta: "+str(e))
            return jsonify(resp), 400
        
        