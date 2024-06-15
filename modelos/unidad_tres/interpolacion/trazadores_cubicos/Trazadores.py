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
    return s_x, ecuaciones_evalauadas, solucion

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
    return s_x, ecuaciones_evalauadas, solucion

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
    return s_x, ecuaciones_evalauadas, solucion

class metodo_trazadores:
    def calcular_trazadores(json_data):
        try:
            x = sp.symbols("x")
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
            
            #variables         
            puntos_x = []
            puntos_y = []
            #validaciones
            activarerror = False
            mensajeerror = ""
            for i in range(len(matrizPuntos)):
                for j in range(len(matrizPuntos[i])):
                    try:
                        matrizPuntos[i][j] = int(matrizPuntos[i][j])
                    except ValueError:
                        try:
                            matrizPuntos[i][j] = float(matrizPuntos[i][j])
                        except ValueError:
                            if matrizPuntos[i][j] == "":
                                continue
                            mensajeerror = "No se pueden ingresar letras en los campos de puntos"
                            activarerror = True
                            break
                if activarerror:
                    break
            if not activarerror:
                if len(matrizPuntos) == 0:
                    mensajeerror = "No se ingresaron puntos"
                    activarerror = True
                elif len(matrizPuntos[0]) < 2:
                    mensajeerror = "Debe haber al menos 2 puntos en X"
                    activarerror = True
                elif len(matrizPuntos) == 1:
                    mensajeerror = "se deben ingresar los puntos en X y Y"
                    activarerror = True
                #Caso tipo 2 con puntos en X y Y
                elif len(matrizPuntos) == 2:
                    #comprobar que vengan la misma cantidad de puntos en X y Y
                    if len(matrizPuntos[0]) != len(matrizPuntos[1]):
                        mensajeerror = "Debe haber la misma cantidad de puntos en X y Y en 'Puntos', es decir los pares ordenados"
                        activarerror = True
                    else:
                        #recorrer los puntos
                        for i in range(len(matrizPuntos[0])):
                            #comprobar que no haya pares ordenados con valores vacios
                            if (matrizPuntos[0][i] == "") ^ (matrizPuntos[1][i] == ""):
                                mensajeerror = "No pueden haber pares ordenados con un valor vacio"
                                activarerror = True
                            #comprobar que los puntos que se guardaran no sean vacios
                            elif not (matrizPuntos[0][i] == "" or matrizPuntos[1][i] == ""):
                                puntos_x.append(matrizPuntos[0][i])
                                puntos_y.append(matrizPuntos[1][i])
                        if len(puntos_x) < 2 and not activarerror:
                            mensajeerror = "Debe haber al menos 2 puntos en X"
                            activarerror = True
                # Verificar que no hayan valores repetidos en los puntos X
                if len(puntos_x) != len(set(puntos_x)) and not activarerror:
                    mensajeerror = "No pueden haber valores repetidos en los puntos en X"
                    activarerror = True
            if activarerror:
                resp = instancia_respuesta.responder_error(mensajeerror)
                return jsonify(resp), 400

            try:
                grado = int(json_data["grado"])
            except Exception as e:
                resp = instancia_respuesta.responder_error("Error en grado ingresado" + str(e))
                return jsonify(resp), 400
            if grado < 0 or grado > 3:
                resp = instancia_respuesta.responder_error("El grado debe ser un numero entre 0 y 3")
                return jsonify(resp), 400
            
            instancia_respuesta.agregar_titulo1("Trazadores Cúbicos grado "+str(grado))
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(["Puntos en X", "Puntos en Y"])
            for i in range(len(puntos_x)):
                instancia_respuesta.agregar_fila([puntos_x[i], puntos_y[i]])
            matrizPuntos = [puntos_x, puntos_y]
            ecuaciones_evaluadas = []
            solucion_ecuaciones = []
            #el metodo de trazadores
            if grado == 0:
                instancia_respuesta.agregar_parrafo("El grado de los trazadores es 0")
                instancia_respuesta.agregar_parrafo("La tabla incial es:")
                instancia_respuesta.agregar_tabla()
                s_x = trazador_grado0(matrizPuntos)
            elif grado == 1:
                instancia_respuesta.agregar_parrafo("El grado de los trazadores es 1")
                instancia_respuesta.agregar_parrafo("La tabla incial es:")
                instancia_respuesta.agregar_tabla()
                s_x, ecuaciones_evaluadas, solucion_ecuaciones = trazador_grado1(matrizPuntos)
            elif grado == 2:
                instancia_respuesta.agregar_parrafo("El grado de los trazadores es 2")
                instancia_respuesta.agregar_parrafo("La tabla incial es:")
                instancia_respuesta.agregar_tabla()
                s_x, ecuaciones_evaluadas, solucion_ecuaciones = trazador_grado2(matrizPuntos)
            elif grado == 3:
                instancia_respuesta.agregar_parrafo("El grado de los trazadores es 3")
                instancia_respuesta.agregar_parrafo("La tabla incial es:")
                instancia_respuesta.agregar_tabla()
                s_x, ecuaciones_evaluadas, solucion_ecuaciones = trazador_grado3(matrizPuntos)
            else:
                resp = instancia_respuesta.responder_error("El grado no es valido")
                return jsonify(resp), 400
            if grado != 0:
                instancia_respuesta.agregar_parrafo("Las ecuaciones formadas son:")
                for i in ecuaciones_evaluadas:
                        instancia_respuesta.agregar_clave_valor("0 =",i)
                instancia_respuesta.agregar_titulo1("Solucion del sistema de ecuaciones")
                for i in solucion_ecuaciones:
                    instancia_respuesta.agregar_clave_valor(i, solucion_ecuaciones[i])
                instancia_respuesta.agregar_parrafo("Reemplazamos y obtenemos los trazadores")
            instancia_respuesta.agregar_titulo1("Resultado")
            instancia_respuesta.agregar_parrafo(f"Los trazadores de grado {grado} son:")
            for i in s_x:
                instancia_respuesta.agregar_clave_valor("S(x)=",i)
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200

        except Exception as e:
            resp = instancia_respuesta.responder_error("Error Interno del codigo del metodo de trazadores"+str(e))
            return jsonify(resp), 400

        
