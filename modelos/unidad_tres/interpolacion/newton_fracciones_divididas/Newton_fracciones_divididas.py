import sympy as sp
from modelos.extras.Funciones import respuesta_json
from flask import jsonify
from modelos.extras.latex import conversla


class metodo_newton_fracciones_divididas:

    @staticmethod
    def calcular_newton_fracciones_divididas(json_data):
        try:
            x = sp.symbols("x")
            f_x = ""
            instancia_respuesta = respuesta_json()
            try:
                tipo = json_data["tipo"]
            except:
                resp = instancia_respuesta.responder_error("Error en el argumento 'tipo'")
            if tipo == 1:
                #obtengo la funcion de json
                #obtengo la funcion de json
                try:
                    f_x = conversla.latex_(json_data["funcion"])
                    resultado = f_x.subs(x, 1)
                    if  resultado > 0:
                        pass
                except sp.SympifyError as e:
                    resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                    return jsonify(resp), 400
                except TypeError as e:
                    resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
                    return jsonify(resp), 400
                except Exception as e:
                    resp = instancia_respuesta.responder_error("Error en el codigo interno de la funcion ingresada")
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
                
                instancia_respuesta.agregar_titulo1("Polinomio de Interpolacion de Newton")
                instancia_respuesta.agregar_parrafo("Se obtiene el polinomio de interpolacion de Newton mediante el metodo de fracciones divididas")
                matris = []                
                for i in range(len(puntos_x)):
                    matris.append([puntos_x[i], puntos_y[i]])
                

                instancia_respuesta.crear_tabla();
                for i in range(1,len(matris)):
                    for j in range(i , len(matris)):
                        valor = (matris[j][i] - matris[j-1][i]) / (matris[j][0] - matris[j-i][0])
                        matris[j].append(valor)
                instancia_respuesta.agregar_fila(["x", "f(x)"])
                for i in range(len(matris)):
                    instancia_respuesta.agregar_fila(matris[i])
                instancia_respuesta.agregar_tabla()

                for i in range(len(matris)):
                    print("b", i, " = ", matris[i][i+1])

                coeficientes = [matris[i][i+1] for i in range(len(matris))]
                instancia_respuesta.agregar_clave_valor("Coeficientes: ", str(coeficientes))


                
                p_x = 0
                texto = ""
                for i in range(len(puntos_x)):
                    producto = 1
                    for j in range(i):
                        producto *= x - puntos_x[j]
                    texto += str(matris[i][i+1]) + " * [" + str(producto) + "]"
                    if i != len(puntos_x) - 1:
                        texto += " + "
                    p_x += matris[i][i+1] * producto

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
        
"""



"""
