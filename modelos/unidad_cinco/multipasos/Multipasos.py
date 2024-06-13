import sympy as sp
from flask import jsonify
from modelos.extras.Formulas_multipasos import runge_kutta, adams_bashfort, adams_moulton
from modelos.extras.Funciones import verificaciones, respuesta_json


class metodo_multipasos():

    def calcular_multipasos(json_data):
        instancia_respuesta = respuesta_json()
        try:
            x = sp.symbols('x')
            y = sp.symbols('y')

            # Se obtienen los datos del json
            try:
                x0 = float(json_data['xinicial'])
                y0 = float(json_data['yinicial'])
                h = float(json_data['h'])
                x_buscado = float(json_data['xfinal'])
                if verificaciones.es_entero(json_data['pasos']):
                    pasos = int(json_data['pasos'])
                    if pasos != 2 and pasos != 4:
                        resp = instancia_respuesta.responder_error("El numero de pasos debe ser 2 o 4")
                        return jsonify(resp), 400
                else:
                    resp = instancia_respuesta.responder_error("El numero de pasos debe ser un entero (2 o 4)")
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
            except Exception as e:
                resp = instancia_respuesta.responder_error("Error en los datos: "+str(e))
                return jsonify(resp), 400
            
            

            # Se procede a aplicar rungen kutta
            #aplica para orden 2
            lista_x = []
            lista_y = []
            x0 = x0
            y0 = y0
            if pasos == 2:
                lista_x.append(x0)
                lista_y.append(y0)
                lista_x.append(round(x0 + h,10))
                lista_y.append(runge_kutta.orden_2(x0, y0, h, f_x)['yi_siguiente'])
                print(lista_x)
                #aplico adams bashfort
                lista_x, lista_y, y2 = adams_bashfort.orden_2(lista_x, lista_y, h, f_x)
                #evaluo si llege al x buscado con h tamaño de paso
                if x_buscado != lista_x[-1]:
                    resp = instancia_respuesta.responder_error("No se puede llegar al valor buscado con el tamanho de paso dado")
                    return jsonify(resp), 400
                #aplico adams moulton
                lista_x, lista_y, y2 = adams_moulton.orden_1(lista_x, lista_y, h, f_x)
                instancia_respuesta.agregar_parrafo(f"El valor de y en x = {x_buscado},{lista_x[-1]} es: {y2}")
                resp = instancia_respuesta.obtener_y_limpiar_respuesta()
                return jsonify(resp), 200

            elif pasos == 4:
                lista_x.append(x0)
                lista_y.append(y0)
                #llenar lista x hasta lo nesesario en este paso
                xs = x0
                for i in range(1, 4):
                    xs = round(xs + h, 8)
                    if xs == (x_buscado - h):
                        break
                    lista_x.append(xs)
                for i in range(0, 3):
                    lista_y.append(runge_kutta.orden_4(lista_x[i], lista_y[i], h, f_x)['yi_siguiente'])
                #aplico adams bashfort
                lista_x, lista_y, y4 = adams_bashfort.orden_4(lista_x, lista_y, h, f_x)
                if x_buscado != lista_x[-1]:
                    resp = instancia_respuesta.responder_error("No se puede llegar al valor buscado con el tamanho de paso dado")
                    return jsonify(resp), 400
                #aplico adams moulton
                lista_x, lista_y, y4 = adams_moulton.orden_3(lista_x, lista_y, h, f_x)
                instancia_respuesta.agregar_parrafo(f"El valor de y en x = {x_buscado},{lista_x[-1]} es: {y4}")
                resp = instancia_respuesta.obtener_y_limpiar_respuesta()
                return jsonify(resp), 200
            else:
                resp = instancia_respuesta.responder_error("El numero de pasos debe ser 2 o 4")
                return jsonify(resp), 400
            
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error en el metodo multipasos: "+str(e))
            return jsonify(resp), 500




        