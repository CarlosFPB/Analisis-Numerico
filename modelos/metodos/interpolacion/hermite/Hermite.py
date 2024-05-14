import sympy as sp
from modelos.extras.Funciones import respuesta_json
from flask import jsonify


class metodo_hermite:

    @staticmethod
    def calcular_hermite(json_data):
        try:
            x = sp.symbols("x")
            f_x = ""
            instancia_respuesta = respuesta_json()
            try:
                tipo = json_data["tipo"]
            except:
                resp = instancia_respuesta.responder_error("Error en el argumento 'tipo'")
            if tipo == 1:
                try:
                    f_x = sp.sympify(json_data["funcion"])
                except:
                    resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                    return jsonify(resp), 400
            try:
                matrizPuntos = json_data["matrizPuntos"]
            except:
                resp = instancia_respuesta.responder_error("Error en los puntos ingresados")
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
                elif len(matrizPuntos) > 2:
                    mensajeerror = "en 'Puntos' debe haber 1 lista con los puntos en X y aparte una funcion o 2 filas con los puntos en X y Y"
                    activarerror = True
                elif len(matrizPuntos[0]) < 2:
                    mensajeerror = "Debe haber al menos 2 puntos en X"
                    activarerror = True
                elif tipo == 1 and len(matrizPuntos) == 2:
                    mensajeerror = "Si se ingresa una funcion, no se deben ingresar puntos en Y"
                    activarerror = True
                elif tipo == 2 and len(matrizPuntos) == 1:
                    mensajeerror = "Si es de tipo 2, se deben ingresar los puntos en X y Y"
                    activarerror = True
                #Caso tipo 2 con puntos en X y Y
                elif tipo == 2 and len(matrizPuntos) == 2:
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
                #Caso tipo 1 con funcion y valores solo en X
                elif tipo == 1 and len(matrizPuntos) == 1:
                    for i in range(len(matrizPuntos[0])):
                        if not matrizPuntos[0][i] == "":
                            puntos_x.append(matrizPuntos[0][i])
                    if len(puntos_x) < 2:
                            mensajeerror = "Debe haber al menos 2 puntos en X"
                            activarerror = True
                    else:
                        puntos_y = [f_x.subs(x, i) for i in puntos_x]
                # Verificar que no hayan valores repetidos en los puntos X
                if len(puntos_x) != len(set(puntos_x)) and not activarerror:
                    mensajeerror = "No pueden haber valores repetidos en los puntos en X"
                    activarerror = True
            

            if activarerror:
                resp = instancia_respuesta.responder_error(mensajeerror)
                return jsonify(resp), 400
            else:

                #En este punto inicia el metodo de lagrange
                instancia_respuesta.agregar_titulo1("Valores Iniciales")
                if tipo == 1:
                    instancia_respuesta.agregar_clave_valor("Funcion:", f_x)
                    instancia_respuesta.agregar_clave_valor("Puntos X:", str(puntos_x).replace("'", ""))
                    instancia_respuesta.agregar_clave_valor("Puntos Y:", str(puntos_y).replace("'", ""))
                else:
                    instancia_respuesta.agregar_parrafo("La funcion original se desconoce")
                    instancia_respuesta.agregar_clave_valor("Puntos X:", str(puntos_x).replace("'", ""))
                    instancia_respuesta.agregar_clave_valor("Puntos Y:", str(puntos_y).replace("'", ""))

                
                #inicio del metodo
                     
                def calcular_diferencia(xinicial, xfinal):
                    if xinicial == xfinal:
                        valor = puntos_y[xinicial]
                        texto = "<math><mn>" + str(puntos_y[xinicial]) + "</mn></math>"
                        return [valor, texto]
                    else:
                        valor = (calcular_diferencia(xinicial + 1, xfinal)[0] - calcular_diferencia(xinicial, xfinal - 1)[0]) / (
                            puntos_x[xfinal] - puntos_x[xinicial]
                        )
                        texto = "<math><mfrac><mrow><mn>"+ calcular_diferencia(xinicial + 1, xfinal)[1] +"</mn><mo>-</mo><mn>"+calcular_diferencia(xinicial, xfinal - 1)[1]+"</mn></mrow><mrow><mn>"+str(puntos_x[xfinal])+"</mn><mo>-</mo><mn>"+str(puntos_x[xinicial])+"</mn></mrow></mfrac></math>"
                        return [valor, texto]
                    

                coeficientes = [calcular_diferencia(0, i) for i in range(len(puntos_x))]
                instancia_respuesta.agregar_titulo1("Polinomio de Interpolacion de Newton")

                for i in range(len(coeficientes)):
                    texto = "b" + str(i)+": <math>" + coeficientes[i][1] + "</math>"
                    if i != 0:
                        texto += "<math><mo> = </mo><mo></mo><mn>"+str(coeficientes[i][0])+"</mn></math>"
                    instancia_respuesta.agregar_parrafo(texto)



                p_x = 0
                texto = ""
                for i in range(len(coeficientes)):
                    producto = 1
                    for j in range(i):
                        producto *= x - puntos_x[j]
                    texto += str(coeficientes[i][0]) + " * [" + str(producto) + "]"
                    if i != len(coeficientes) - 1:
                        texto += " + "
                    p_x += coeficientes[i][0] * producto

                instancia_respuesta.agregar_parrafo("se hace la suma de los productos de los coeficientes con los productos de los factores")
                instancia_respuesta.agregar_clave_valor("p(x): ", texto)

                instancia_respuesta.agregar_titulo1("Resultado")
                instancia_respuesta.agregar_parrafo("Se simplifica la expresion obtenida:")
                instancia_respuesta.agregar_clave_valor("p(x): ", sp.simplify(p_x))

                p_x_decimal = sp.simplify(p_x.evalf())
                instancia_respuesta.agregar_clave_valor("p(x) decimal:", str(p_x_decimal))



                resp = instancia_respuesta.obtener_y_limpiar_respuesta()
                return jsonify(resp), 200
        except:
            resp = instancia_respuesta.responder_error("Error en el codigo interno del metodo de lagrange")
            return jsonify(resp), 400
        




