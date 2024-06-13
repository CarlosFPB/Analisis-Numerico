import sympy as sp
from flask import jsonify
from modelos.extras.Funciones import verificaciones, respuesta_json

class metodo_taylor:

    @staticmethod
    def derivar_en_xy(EDO, grado):
        x = sp.Symbol("x") 
        y = sp.Function("y")(x)
        funcion = EDO.subs(y, y)
        derivadas = []
        derivadas.append(EDO)
        for i in range(1, grado):
            funcion = funcion.diff().subs(y.diff(), EDO)
            derivadas.append(funcion)
        return derivadas

    @staticmethod
    def formular_taylor(xi, yi, h, yprima, grado):
        x = sp.Symbol("x")
        y = sp.Function("y")(x)
        derivadas = []
        yi_siguiente = 0
        if grado == 0:
            yi_siguiente = yi
            return yi_siguiente
        if grado == 1:
            derivadas.append(yprima)
        else:
            derivadas = metodo_taylor.derivar_en_xy(yprima, grado)
        #formulando respuesta
        for i in range(0 ,grado+1):
            if i == 0:
                yi_siguiente += yi
            else:
                yi_siguiente += (h**i)/sp.factorial(i)*derivadas[i-1].subs({x:xi, y:yi})
        yi_siguiente = sp.N(yi_siguiente)
        return yi_siguiente
        
    @staticmethod
    def calcular_taylor(json_data):
        x= sp.symbols('x')
        y= sp.Function('y')(x)
        instancia_respuesta = respuesta_json()
        # Se obtienen los datos del json
        try:
            x0 = float(json_data['xinicial'])
            y0 = float(json_data['yinicial'])
            h = float(json_data['h'])
            x_buscado = float(json_data['xfinal'])
            if verificaciones.es_entero(json_data['grado']):
                grado = int(json_data['grado'])
                if grado < 0:
                    resp = instancia_respuesta.responder_error("El grado debe ser mayor o igual a 0")
                    return jsonify(resp), 400
            else:
                resp = instancia_respuesta.responder_error("El grado debe ser un valor entero mayor o igual a 0")
                return jsonify(resp), 400
            try:
                f_x = sp.sympify(json_data['funcion'])
                rs = f_x.subs({x: x0, y: y0})
                if rs > 0:
                    pass
            except sp.SympifyError:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                return jsonify(resp), 400
            except Exception as e:
                resp = instancia_respuesta.responder_error("Error en la funcion ingresada "+str(e))
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
            #se aplica el metodo de Taylor
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
            #aplicacion del metodo de taylor
            for i in range(0, n-1):
                lista_y.append(metodo_taylor.formular_taylor(lista_x[i], lista_y[i], h, f_x, grado))

            instancia_respuesta.agregar_parrafo("Los valores de x son: ")
            instancia_respuesta.agregar_parrafo(str(lista_x))
            instancia_respuesta.agregar_parrafo("Los valores de y son: ")
            instancia_respuesta.agregar_parrafo(str(lista_y))
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error Interno del codigo: "+str(e))
            return jsonify(resp), 400


