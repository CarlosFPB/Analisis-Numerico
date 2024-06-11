import sympy as sp
from flask import jsonify
from modelos.extras.Formulas_euler import euler
from modelos.extras.Funciones import verificaciones, respuesta_json

class metodo_euler():

    @staticmethod
    def calcular_euler(json_data):
        x = sp.symbols('x')
        y = sp.symbols('y')
        instancia_respuesta = respuesta_json()
        try:
            x0 = float(json_data['x0'])
            y0 = float(json_data['y0'])
            h = float(json_data['h'])
            x_buscado = float(json_data['x_buscado'])
            metodo = json_data["metodo"]
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
            #se aplica el metodo de euler segund el metodo seleccionado
            #se agregan los datos iniciales
            lista_x.append(x0)
            lista_y.append(y0)
            #llenar lista x hasta el x buscado
            xs = x0
            while True:
                xs = round(xs + h, 8)
                lista_x.append(xs)
                if xs >= (x_buscado):
                    break
            if x_buscado != lista_x[-1]:
                resp = instancia_respuesta.responder_error("No se puede llegar al valor buscado con el tamanho de paso dado")
                return jsonify(resp), 400
            n = len(lista_x)
            ys = y0
            #aqui se selecciona el metodo a utilizar
            if metodo == "euler_mejorado":
                for i in range(0, n-1):
                    ys = euler.euler_mejorado(lista_x[i], ys, h, f_x)
                    lista_y.append(ys)
            elif metodo == "euler_hacia_atras":
                for i in range(0, n-1):
                    ys = euler.euler_hacia_atras(lista_x[i], ys, h, f_x)
                    lista_y.append(ys)
            elif metodo == "euler_hacia_adelante":
                for i in range(0, n-1):
                    ys = euler.euler_hacia_adelante(lista_x[i], ys, h, f_x)
                    lista_y.append(ys)
            elif metodo == "euler_centrada":
                for i in range(0, n-1):
                    ys = euler.euler_centrada(lista_x[i], ys, h, f_x)
                    lista_y.append(ys)
            else:
                resp = instancia_respuesta.responder_error("Metodo no valido\nLos metodos validos son: euler_mejorado, euler_hacia_atras, euler_hacia_adelante, euler_centrada")
                return jsonify(resp), 400

            instancia_respuesta.agregar_parrafo("Los valores de x son: "+str(lista_x))
            instancia_respuesta.agregar_parrafo("Los valores de y son: "+str(lista_y))
            instancia_respuesta.agregar_parrafo(f"Respuesta de x: {x_buscado} y: {lista_y[-1]}")
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en los datos: "+str(e))
            return jsonify(resp), 400
        
    