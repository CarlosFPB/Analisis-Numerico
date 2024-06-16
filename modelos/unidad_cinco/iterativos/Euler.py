import sympy as sp
from flask import jsonify
from modelos.extras.Formulas_euler import euler
from modelos.extras.Funciones import verificaciones, respuesta_json
from modelos.extras.latex import conversla,conversla_html

class metodo_euler():

    @staticmethod
    def calcular_euler(json_data):
        x = sp.symbols('x')
        y = sp.symbols('y')
        instancia_respuesta = respuesta_json()
        try:
            x0 = float(json_data['x_inicial'])
            y0 = float(json_data['y_inicial'])
            h = float(json_data['h'])
            x_buscado = float(json_data['x_final'])
            metodo = json_data["tipo"]
            try:
                f_x =conversla.latex_(json_data["latex"])
                resultado = f_x.subs(x, 1).evalf()
                is_imaginary = resultado.is_imaginary

                if resultado.is_real and resultado > 0:
                    pass
                elif is_imaginary:
                    pass
            except sp.SympifyError as e:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                print(e)
                return jsonify(resp), 400
            except TypeError as e:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                print(e)
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
            # Generar lista_x en la dirección correcta
            while True:
                xs = round(xs + h, 8)
                lista_x.append(xs)
                if (h > 0 and xs >= x_buscado) or (h < 0 and xs <= x_buscado):
                    break
            
            # Verificar si se alcanzó exactamente el valor buscado
            if (h > 0 and x_buscado != lista_x[-1]) or (h < 0 and x_buscado != lista_x[-1]):
                resp = instancia_respuesta.responder_error("No se puede llegar al valor buscado con el tamaño de paso dado")
                return jsonify(resp), 400
            n = len(lista_x)
            ys = y0
            #registro valores iniciales
            instancia_respuesta.agregar_titulo1("Metodo de Euler")
            instancia_respuesta.agregar_parrafo("Datos iniciales: ")
            instancia_respuesta.agregar_clave_valor("Funcion: ", f_x)
            instancia_respuesta.agregar_parrafo("x0: "+str(x0))
            instancia_respuesta.agregar_parrafo("y0: "+str(y0))
            instancia_respuesta.agregar_parrafo("h: "+str(h))
            instancia_respuesta.agregar_parrafo("x final: "+str(x_buscado))
            #aqui se aplica el metodo seleccioando
            if metodo == "euler_mejorado":
                instancia_respuesta.agregar_titulo1("Aplicando metodo de Euler Mejorado")
                instancia_respuesta.agregar_parrafo("se calcula yraya con la formula: y_raya1 = y0 + h*f(x0, y0)")
                instancia_respuesta.agregar_parrafo("Se calcula el nuevo valor de x con la formula: x1 = x0 + h")
                instancia_respuesta.agregar_parrafo("se calcula el nuevo y con la formula: y1 = y0 + h/2*[(f(x0, y0) + f(x1, y_raya1)]")
                instancia_respuesta.agregar_parrafo("se repite el proceso hasta llegar al valor buscado")
                for i in range(0, n-1):
                    ys = euler.euler_mejorado(lista_x[i], ys, h, f_x)
                    lista_y.append(ys)
            elif metodo == "euler_hacia_atras":
                instancia_respuesta.agregar_titulo1("Aplicando metodo de Euler hacia atras")
                instancia_respuesta.agregar_parrafo("se calcula y_raya con la formula: y_raya = y0 + h*f(x0, y0)")
                instancia_respuesta.agregar_parrafo("Se calcula el nuevo valor de x con la formula: x1 = x0 + h")
                instancia_respuesta.agregar_parrafo("se calcula el nuevo y con la formula: y1 = y0 + h*f(x1, y_raya)")
                instancia_respuesta.agregar_parrafo("se repite el proceso hasta llegar al valor buscado")
                for i in range(0, n-1):
                    ys = euler.euler_hacia_atras(lista_x[i], ys, h, f_x)
                    lista_y.append(ys)
            elif metodo == "euler_hacia_adelante":
                instancia_respuesta.agregar_titulo1("Aplicando metodo de Euler hacia adelante")
                instancia_respuesta.agregar_parrafo("se calcula el nuevo y con la formula: y1 = y0 + h*f(x0, y0)")
                instancia_respuesta.agregar_parrafo("Se calcula el nuevo valor de x con la formula: x1 = x0 + h")
                instancia_respuesta.agregar_parrafo("se repite el proceso hasta llegar al valor buscado")
                for i in range(0, n-1):
                    ys = euler.euler_hacia_adelante(lista_x[i], ys, h, f_x)
                    lista_y.append(ys)
            elif metodo == "euler_centrada":
                instancia_respuesta.agregar_titulo1("Aplicando metodo de Euler centrado")
                instancia_respuesta.agregar_parrafo("se calcula el nuevo y con la formula: y1 = y0 + h*f(x0, y0)")
                instancia_respuesta.agregar_parrafo("Se calcula el nuevo valor de x con la formula: x1 = x0 + h")
                instancia_respuesta.agregar_parrafo("se repite el proceso hasta llegar al valor buscado")
                for i in range(0, n-1):
                    ys = euler.euler_centrada(lista_x[i], ys, h, f_x)
                    lista_y.append(ys)
            else:
                resp = instancia_respuesta.responder_error("Metodo no valido\nLos metodos validos son: euler_mejorado, euler_hacia_atras, euler_hacia_adelante, euler_centrada")
                return jsonify(resp), 400
            
            #se registra la respuesta
            instancia_respuesta.agregar_titulo1("Resultados: ")
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(["x", "valor de x", "y", "valor de y"])
            for i in range(0, n):
                instancia_respuesta.agregar_fila([f"x{i}", f"{lista_x[i]}", f"y{i}", f"{lista_y[i]}"])
            instancia_respuesta.agregar_tabla()
            instancia_respuesta.agregar_clave_valor("Respuesta final: ", f"y({x_buscado}) = {lista_y[-1]}")
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en los datos: "+str(e))
            return jsonify(resp), 400
        
    