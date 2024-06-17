import sympy as sp
from flask import jsonify
from modelos.extras.Formulas_multipasos import runge_kutta
from modelos.extras.Funciones import verificaciones, respuesta_json
from modelos.extras.latex import conversla,conversla_html

class metodo_runge_kutta():

    def calcular_metodo_runge_kutta(json_data):
        x = sp.symbols('x')
        y = sp.symbols('y')
        instancia_respuesta = respuesta_json()
        # Se obtienen los datos del json
        try:
            x0 = float(json_data['x_inicial'])
            y0 = float(json_data['y_inicial'])
            h = float(json_data['h'])
            if h == 0:
                resp = instancia_respuesta.responder_error("El tamaño de paso debe ser diferente de 0")
                return jsonify(resp), 400
            x_buscado = float(json_data['x_final'])
            if verificaciones.es_entero(json_data['orden']):
                orden = int(json_data['orden'])
                if orden <2 or orden > 4:
                    resp = instancia_respuesta.responder_error("El orden debe ser 2, 3 o 4")
                    return jsonify(resp), 400
            else:
                resp = instancia_respuesta.responder_error("El numero de orden debe ser un entero entre (2 y 4)")
                return jsonify(resp), 400
            
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
            #se aplica el metodo de runge kutta
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
            #registro valores iniciales
            instancia_respuesta.agregar_titulo1("Metodo de Runge Kutta")
            instancia_respuesta.agregar_parrafo("Datos iniciales: ")
            instancia_respuesta.agregar_clave_valor("Funcion: ", f_x)
            instancia_respuesta.agregar_parrafo("x0: "+str(x0))
            instancia_respuesta.agregar_parrafo("y0: "+str(y0))
            instancia_respuesta.agregar_parrafo("h: "+str(h))
            instancia_respuesta.agregar_parrafo("x final: "+str(x_buscado))
            if orden == 2:
                instancia_respuesta.agregar_titulo1("Calculos de orden: 2")
                instancia_respuesta.agregar_parrafo("Se calcula k1 con la formula: k1 = f(x0, y0)")
                instancia_respuesta.agregar_parrafo("Se calcula k2 con la formula: k2 = f(x0 + h, y0 + h*k1)")
                instancia_respuesta.agregar_parrafo("Se calcula y1 con la formula: y1 = y0 + (1/2)*h*(k1 + k2)")
                instancia_respuesta.agregar_parrafo("Se calculo el nuevo valor de x2 y repite el proceso hasta llegar al valor de x buscado")
                for i in range(0, n-1):
                    lista_y.append(runge_kutta.orden_2(lista_x[i], lista_y[i], h, f_x)['yi_siguiente'])
            elif orden == 3:
                instancia_respuesta.agregar_titulo1("Calculos de orden: 3")
                instancia_respuesta.agregar_parrafo("Se calcula k1 con la formula: k1 = f(x0, y0)")
                instancia_respuesta.agregar_parrafo("Se calcula k2 con la formula: k2 = f(x0 + h/2, y0 + (h/2)*k1)")
                instancia_respuesta.agregar_parrafo("Se calcula k3 con la formula: k3 = f(x0 + h, y0 - h*k1 + 2*h*k2)")
                instancia_respuesta.agregar_parrafo("Se calcula y1 con la formula: y1 = y0 + (1/6)*h*(k1 + 4*k2 + k3)")
                instancia_respuesta.agregar_parrafo("Se calcula el nuevo valor de x2 y repite el proceso hasta llegar al valor de x buscado")
                for i in range(0, n-1):
                    lista_y.append(runge_kutta.orden_3(lista_x[i], lista_y[i], h, f_x)['yi_siguiente'])
            elif orden == 4:
                instancia_respuesta.agregar_titulo1("Calculos de orden: 4")
                instancia_respuesta.agregar_parrafo("Se calcula k1 con la formula: k1 = f(x0, y0)")
                instancia_respuesta.agregar_parrafo("Se calcula k2 con la formula: k2 = f(x0 + h/2, y0 + h/2*k1)")
                instancia_respuesta.agregar_parrafo("Se calcula k3 con la formula: k3 = f(x0 + h/2, y0 + h/2*k2)")
                instancia_respuesta.agregar_parrafo("Se calcula k4 con la formula: k4 = f(x0 + h, y0 + h*k3)")
                instancia_respuesta.agregar_parrafo("Se calcula y1 con la formula: y1 = y0 + (h/6)*(k1 + 2*k2 + 2*k3 + k4)")
                instancia_respuesta.agregar_parrafo("Se calculo el nuevo valor de x2 y repite el proceso hasta llegar al valor de x buscado")
                for i in range(0, n-1):
                    lista_y.append(runge_kutta.orden_4(lista_x[i], lista_y[i], h, f_x)['yi_siguiente'])


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
            resp = instancia_respuesta.responder_error("Error en el metodo de Runge Kutta: "+str(e))
            return jsonify(resp), 400
        
        