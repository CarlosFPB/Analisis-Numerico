import sympy as sp
from flask import jsonify
from modelos.extras.Funciones import respuesta_json,verificaciones

def trazador_grado0(matriz_puntos):
    x = sp.Symbol('x')
    n = len(matriz_puntos[0])
    #saco los intervalos de x y y
    intervalos_x = []
    for i in range(n-1):
        intervalos_x.append([matriz_puntos[0][i], matriz_puntos[0][i+1]])
    intervalos_y = []
    for i in range(n-1):
        intervalos_y.append([matriz_puntos[1][i], matriz_puntos[1][i+1]])
    #formulo la respuesta de s(x)
    s_x  = []
    for i in range(n-1):
        s_x.append(f"{intervalos_y[i][0]} ; {intervalos_x[i]}")
    return s_x

def trazador_grado1(matriz_puntos):
    x = sp.Symbol('x')
    n = len(matriz_puntos[0])
    intervalos_x = []
    for i in range(n-1):
        intervalos_x.append([matriz_puntos[0][i], matriz_puntos[0][i+1]])
    intervalos_y = []
    for i in range(n-1):
        intervalos_y.append([matriz_puntos[1][i], matriz_puntos[1][i+1]])
    ecuaciones = []
    #forma ax+b [x,x+1]
    for i in range(n-1):
        a = sp.Symbol(f'a{i}')
        b = sp.Symbol(f'b{i}')
        ecuaciones.append(a*x+b)
    ecuaciones_evalauadas = []
    for i in range(n-1):
        ecuaciones_evalauadas.append(ecuaciones[i].subs(x, intervalos_x[i][0]) - intervalos_y[i][0])
        ecuaciones_evalauadas.append(ecuaciones[i].subs(x, intervalos_x[i][1]) - intervalos_y[i][1])
    #resuelve el sistema de ecuaciones
    solucion = sp.solve(ecuaciones_evalauadas)
    #reemplaza los valores de a y b en las ecuaciones originales
    s_x  = []
    funcion, intervalo = 0, 0
    for i in range(n-1):
        funcion = sp.N(ecuaciones[i].subs(solucion))
        intervalo = intervalos_x[i]
        s_x.append(f"{funcion} ; {intervalo}")
    return s_x

def trazador_grado2(matriz_puntos):
    x = sp.Symbol('x')
    n = len(matriz_puntos[0])
    intervalos_x = []
    for i in range(n-1):
        intervalos_x.append([matriz_puntos[0][i], matriz_puntos[0][i+1]])
    intervalos_y = []
    for i in range(n-1):
        intervalos_y.append([matriz_puntos[1][i], matriz_puntos[1][i+1]])
    ecuaciones = []
    #forma ax^2+bx+c [x,x+1]
    for i in range(n-1):
        a = sp.Symbol(f'a{i}')
        b = sp.Symbol(f'b{i}')
        c = sp.Symbol(f'c{i}')
        ecuaciones.append(a*x**2+b*x+c)
    ecuaciones_evalauadas = []
    for i in range(n-1):
        ecuaciones_evalauadas.append(ecuaciones[i].subs(x, intervalos_x[i][0]) - intervalos_y[i][0])
        ecuaciones_evalauadas.append(ecuaciones[i].subs(x, intervalos_x[i][1]) - intervalos_y[i][1])
    #resuelve el sistema de ecuaciones
    #derivo las ecuaciones
    derivadas = []
    for i in range(n-1):
        derivadas.append(ecuaciones[i].diff(x))
    #evaluo las derivadas en los puntos que se repiten
    for i in range(n-2):
        primer_parte = derivadas[i].subs(x, intervalos_x[i][1])
        segunda_parte = derivadas[i+1].subs(x, intervalos_x[i][1])
        ecuaciones_evalauadas.append(primer_parte - segunda_parte)
    #resolver el sistema de ecuaciones
    solucion = sp.solve(ecuaciones_evalauadas)
    #reemplaza los valores de a y b en las ecuaciones originales
    #ya que la solucion nos da todo en terminos de c3
    #c3 = 0 grado de libertad para la interpolacion
    solucion[f'c{n-2}'] = 0
    s_x  = []
    funcion, intervalo = 0, 0
    for i in range(n-1):
        funcion = sp.N(ecuaciones[i].subs(solucion))
        intervalo = intervalos_x[i]
        s_x.append(f"{funcion} ; {intervalo}")
    return s_x

def trazador_grado3(matriz_puntos):
    x = sp.Symbol('x')
    n = len(matriz_puntos[0])
    intervalos_x = []
    for i in range(n-1):
        intervalos_x.append([matriz_puntos[0][i], matriz_puntos[0][i+1]])
    intervalos_y = []
    for i in range(n-1):
        intervalos_y.append([matriz_puntos[1][i], matriz_puntos[1][i+1]])
    ecuaciones = []
    #forma ax^3+bx^2+cx+d [x,x+1]
    for i in range(n-1):
        a = sp.Symbol(f'a{i}')
        b = sp.Symbol(f'b{i}')
        c = sp.Symbol(f'c{i}')
        d = sp.Symbol(f'd{i}')
        ecuaciones.append(a*x**3+b*x**2+c*x+d)
    ecuaciones_evalauadas = []
    for i in range(n-1):
        ecuaciones_evalauadas.append(ecuaciones[i].subs(x, intervalos_x[i][0]) - intervalos_y[i][0])
        ecuaciones_evalauadas.append(ecuaciones[i].subs(x, intervalos_x[i][1]) - intervalos_y[i][1])
    #resuelve el sistema de ecuaciones
    #derivo las ecuaciones intermedias osea las q repite
    derivadas = []
    segundas_derivadas = []
    for i in range(n-1):
        derivadas.append(ecuaciones[i].diff(x))
        segundas_derivadas.append(derivadas[-1].diff(x))
    #evaluo las primeras derivadas en los puntos que se repiten
    for i in range(n-2):
        primer_parte = derivadas[i].subs(x, intervalos_x[i][1])
        segunda_parte = derivadas[i+1].subs(x, intervalos_x[i][1])
        ecuaciones_evalauadas.append(primer_parte - segunda_parte)
    #evaluo las segundas derivadas en los puntos que se repiten
    for i in range(n-2):
        primer_parte = segundas_derivadas[i].subs(x, intervalos_x[i][1])
        segunda_parte = segundas_derivadas[i+1].subs(x, intervalos_x[i][1])
        ecuaciones_evalauadas.append(primer_parte - segunda_parte)

    #grado de libertad s''(x0) = 0 y s''(xn) = 0
    ecuaciones_evalauadas.append(segundas_derivadas[0].subs(x, intervalos_x[0][0]))
    ecuaciones_evalauadas.append(segundas_derivadas[-1].subs(x, intervalos_x[-1][1]))
    #resolver el sistema de ecuaciones
    solucion = sp.solve(ecuaciones_evalauadas)
    #reemplaza los valores de a y b en las ecuaciones originales
    s_x  = []
    funcion, intervalo = 0, 0
    for i in range(n-1):
        funcion = sp.N(ecuaciones[i].subs(solucion))
        intervalo = intervalos_x[i]
        s_x.append(f"{funcion} ; {intervalo}")
    return s_x

class metodo_trazadores:
    def calcular_trazadores(json_data):
        try:
            x = sp.symbols("x")
            instancia_respuesta = respuesta_json()
            matriz_puntos = []
            try:
                matriz_puntos = json_data["matrizPuntos"]
                #verificar si la matriz de puntos es valida
                if not verificaciones.es_matriz(matriz_puntos):
                    resp = instancia_respuesta.responder_error("La matriz de puntos no es valida")
                    return jsonify(resp), 400
            except:
                resp = instancia_respuesta.responder_error("Error en los datos ingresados")
                return jsonify(resp), 400
            
            #verificar si la matriz de puntos esta vacia o tiene la cantidad nesesaria de datos
            if len(matriz_puntos) == 0:
                resp = instancia_respuesta.responder_error("No se ingresaron puntos")
                return jsonify(resp), 400
            elif len(matriz_puntos) == 1:
                resp = instancia_respuesta.responder_error("Faltan puntos en y")
                return jsonify(resp), 400
            elif len(matriz_puntos) == 2:
                #verificar que cuente con dos parejas de puntos
                if len(matriz_puntos[0]) ==2 and len(matriz_puntos[1]) == 2:
                    #verificar que los puntos sean numeros
                    if verificaciones.verificar_numeros_matriz(matriz_puntos):
                        #verificar si los puntos en x no se repiten
                        if not verificaciones.verificar_puntos_unicos(matriz_puntos[0]):
                            resp = instancia_respuesta.responder_error("Los puntos en x no deben repetirse")
                            return jsonify(resp), 400
                        #Calcular la interpolacion lineal poreso salimos de las verificaciones
                    else:
                        resp = instancia_respuesta.responder_error("Los puntos deben ser numeros")
                        return jsonify(resp), 400
                else:
                    resp = instancia_respuesta.responder_error("Los puntos deben ser el mismo numero de puntos en x y y y deben ser 2")
                    return jsonify(resp), 400
            elif len(matriz_puntos) > 2:
                resp = instancia_respuesta.responder_error("No debe de haber mas de dos pares de puntos")
                return jsonify(resp), 400
            try:
                grado = int(json_data["grado"])
            except Exception as e:
                resp = instancia_respuesta.responder_error("Error en grado ingresado" + str(e))
                return jsonify(resp), 400
            if grado < 0 or grado > 3:
                resp = instancia_respuesta.responder_error("El grado debe ser un numero entre 0 y 3")
                return jsonify(resp), 400


            matrizPuntos = matriz_puntos
            puntos_x = matriz_puntos[0]
            puntos_y = matriz_puntos[1]
            #el metodo de trazadores
            #no se como tratar los datos si es funcion
            print(matrizPuntos)
            print(puntos_x, puntos_y)
            if grado == 0:
                instancia_respuesta.agregar_parrafo("El grado de los trazadores es 0")
                s_x = trazador_grado0(matrizPuntos)
            elif grado == 1:
                instancia_respuesta.agregar_parrafo("El grado de los trazadores es 1")
                s_x = trazador_grado1(matrizPuntos)
            elif grado == 2:
                instancia_respuesta.agregar_parrafo("El grado de los trazadores es 2")
                s_x = trazador_grado2(matrizPuntos)
            elif grado == 3:
                instancia_respuesta.agregar_parrafo("El grado de los trazadores es 3")
                s_x = trazador_grado3(matrizPuntos)
            else:
                resp = instancia_respuesta.responder_error("El grado no es valido")
                return jsonify(resp), 400
            instancia_respuesta.agregar_parrafo("Los trazadores son:")
            for i in s_x:
                instancia_respuesta.agregar_parrafo(i)
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200

        except:
            resp = instancia_respuesta.responder_error("Error Interno del codigo del metodo de trazadores")
            return jsonify(resp), 400

        
