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
    def formular_taylor(xi, yi, h, yprima, grado, derivadas):
        x = sp.Symbol("x")
        y = sp.Function("y")(x)
        derivadas = derivadas
        yi_siguiente = 0
        if grado == 0:
            yi_siguiente = yi
            return yi_siguiente
        #formulando respuesta
        for i in range(0 ,grado+1):
            if i == 0:
                yi_siguiente += yi
            else:
                yi_siguiente += (h**i)/sp.factorial(i)*derivadas[i-1].subs({x:xi, y:yi})
        yi_siguiente = sp.N(yi_siguiente)
        return yi_siguiente
    
    def formular_taylor_string(xi, yi, yprima, grado, derivadas):
        x = sp.Symbol("x")
        y = sp.Function("y")(x)
        formula = ""
        if grado == 0:
            formula = "yk+1 = yk"
            return formula
        if grado == 1:
            formula = "yk+1 = yk + h* y'(xk, yk)"
            return formula
        else:
            formula = "yk+1 = yk"
            for i in range(1, grado+1):
                formula += f" + h^{i}/{i}! * {derivadas[i-1]}"
        return formula
        
    @staticmethod
    def calcular_taylor(json_data):
        x= sp.symbols('x')
        y= sp.Function('y')(x)
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
            #aplicacion del metodo de taylor
            instancia_respuesta.agregar_titulo1("Metodo de Taylor")
            instancia_respuesta.agregar_parrafo("Datos iniciales: ")
            instancia_respuesta.agregar_clave_valor("Funcion: ", f_x)
            instancia_respuesta.agregar_parrafo("x0: "+str(x0))
            instancia_respuesta.agregar_parrafo("y0: "+str(y0))
            instancia_respuesta.agregar_parrafo("h: "+str(h))
            instancia_respuesta.agregar_parrafo("x final: "+str(x_buscado))
            instancia_respuesta.agregar_parrafo("Grado: "+str(grado))

            instancia_respuesta.agregar_parrafo("La formula aplicada se calcula hasta la derivada de grado "+str(grado)+" de la funcion y' = f(x, y)")
            #obtengo derivadas y formulo la formula de taylor
            derivadas = metodo_taylor.derivar_en_xy(f_x, grado)
            instancia_respuesta.agregar_titulo1(f"Formula de grado {grado}:")  
            formulaS = metodo_taylor.formular_taylor_string(x0, y0, f_x, grado, derivadas)
            instancia_respuesta.agregar_parrafo(formulaS)
            instancia_respuesta.agregar_parrafo("Se repite hasta llegar al x final con un paso h")

            for i in range(0, n-1):
                lista_y.append(metodo_taylor.formular_taylor(lista_x[i], lista_y[i], h, f_x, grado, derivadas))
            
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
            resp = instancia_respuesta.responder_error("Error Interno del codigo: "+str(e))
            return jsonify(resp), 400


