import sympy as sp
import math
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
                    derivada = json_data["derivada"]
                    try:
                        derivada = int(derivada)
                        if derivada < 0:
                            resp = instancia_respuesta.responder_error("la derivada debe ser un numero positivo")
                            return jsonify(resp), 400
                    except:
                        resp = instancia_respuesta.responder_error("la derivada debe ser un numero entero")
                        return jsonify(resp), 400

                except:
                    resp = instancia_respuesta.responder_error("Error en la derivada ingresada")
                    return jsonify(resp), 400
            try:
                matrizPuntos = json_data["matrizPuntos"]
            except:
                resp = instancia_respuesta.responder_error("Error en los puntos ingresados")
                return jsonify(resp), 400
            
            

            #variables
                        
            puntos_x = []

            filas = []

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
            

            if not tipo == 1 and not tipo == 2:
                mensajeerror = "Error en el tipo ingresado deber se '1' o '2'"
                activarerror = True
            
            if tipo == 1 and not activarerror:
                if f_x == "":
                    mensajeerror = "Error en la funcion ingresada"
                    activarerror = True
                if derivada == "":
                    mensajeerror = "Error en la derivada ingresada"
                    activarerror = True

                
                if len(matrizPuntos) != 1:
                    mensajeerror = "Al ser de tipo 1 solo se deben de enviar los puntos en X"
                    activarerror = True
                elif len(set([p for p in matrizPuntos[0] if p])) != len([p for p in matrizPuntos[0] if p]):
                    mensajeerror = "No se pueden ingresar valores repetidos en los puntos"
                    activarerror = True

                else:
                    for i in range(len(matrizPuntos[0])):
                        if not matrizPuntos[0][i] == "":
                            puntos_x.append(matrizPuntos[0][i])
                    if len(puntos_x) == 0:
                        mensajeerror = "No se han ingresado puntos en X"
                        activarerror = True
                    else:
                        for i in puntos_x:
                            fila = []
                            fila.append(i)
                            fila.append(float(f_x.subs(x, i)))
                            funcion = f_x
                            for j in range(derivada):
                                funcion = sp.diff(funcion)
                                if funcion == 0:
                                    mensajeerror = "La derivada ingresada es mayor a la derivada de la funcion"
                                    activarerror = True
                                    break
                                fila.append(float(funcion.subs(x, i)))
                            filas.append(fila)
                
            
            
            elif tipo == 2 and not activarerror:
                if len(matrizPuntos) > 0:
                    for i in range(len(matrizPuntos)):
                        fila = []
                        for j in range(len(matrizPuntos[i])):
                            if type(matrizPuntos[i][j]) == int or type(matrizPuntos[i][j]) == float:
                                fila.append(matrizPuntos[i][j])
                            if not(j == len(matrizPuntos[i]) - 1):
                                if not type(matrizPuntos[i][j]) == int or type(matrizPuntos[i][j]) == float:
                                    break
                        filas.append(fila)
                        


            if activarerror:
                resp = instancia_respuesta.responder_error(mensajeerror)
                return jsonify(resp), 400
            else:

                #En este punto inicia el metodo de hermite
                instancia_respuesta.agregar_titulo1("Valores Iniciales")
                if tipo == 1:
                    instancia_respuesta.agregar_clave_valor("Funcion:", f_x)
                else:
                    instancia_respuesta.agregar_parrafo("La funcion original se desconoce")
                instancia_respuesta.agregar_parrafo("contamos con los siguientes datos:")
                instancia_respuesta.crear_tabla()
                titulo = ["x", "f(x)"]
                longitud = 0
                for i in filas:
                    if len(i) > longitud:
                        longitud = len(i)
                for i in range(2, longitud):
                    titulo.append("D<sup>" + str(i-1) + "</sup>y")
                instancia_respuesta.agregar_fila(titulo)
                for i in filas:
                    instancia_respuesta.agregar_fila(i)
                instancia_respuesta.agregar_tabla()
                




                #inicio del metodo
                instancia_respuesta.agregar_titulo1("Polinomio Interpolante de Hermite:") 
                matris = []
                for i in range(len(filas)):
                    for j in range(len(filas[i]) -1):
                        matris.append([filas[i][0], filas[i][1]])
                for i in range(1,len(matris)):
                    for j in range(i, len(matris)):
                        try:
                            valor = (matris[j][i] - matris[j-1][i]) / (matris[j][0] - matris[j-i][0])
                            matris[j].append(valor)
                        except:
                            buscar_fila = [x for x in filas if x[0] == matris[j][0]]
                            valor = buscar_fila[0][len(matris[j])] / math.factorial(i)
                            matris[j].append(valor)
                instancia_respuesta.agregar_parrafo("se calculan los coeficientes de la tabla de diferencias divididas")
                instancia_respuesta.crear_tabla()
                instancia_respuesta.agregar_fila(["x", "f(x)"])
                for i in matris:
                    instancia_respuesta.agregar_fila(i)
                instancia_respuesta.agregar_tabla()





                coeficientes = []
                for i in range(len(matris)):
                    coeficientes.append(matris[i][-1])
                    print("b", i, " = ", matris[i][i+1])
                print(coeficientes)

                instancia_respuesta.agregar_parrafo("Se obtienen los coeficientes del polinomio interpolante de Hermite")
                instancia_respuesta.agregar_clave_valor("Coeficientes:", str(coeficientes).replace("[", "").replace("]", ""))
                p_x = 0



                instancia_respuesta.agregar_parrafo("Se hace la suma de los productos de los coeficientes")
                texto = "p(x) = "
                print("\nProducto de Newton")
                for i in range(len(matris)):
                    producto = 1
                    for j in range(i):
                        producto *= (x - matris[j][0])
                    texto += str(matris[i][i+1]) + "*[" + str(producto) + "]"
                    if i < len(matris) - 1:
                        texto += " + "
                    p_x += matris[i][i+1] * producto
                instancia_respuesta.agregar_parrafo(texto)





                p_x = sp.simplify(p_x)
                instancia_respuesta.agregar_titulo1("Resultado")
                instancia_respuesta.agregar_parrafo("El polinomio interpolante de Hermite es:")
                instancia_respuesta.agregar_clave_valor("p(x):", p_x)
                
                p_x_decimal = sp.simplify(p_x.evalf())
                instancia_respuesta.agregar_clave_valor("p(x) decimal:", str(p_x_decimal))





                resp = instancia_respuesta.obtener_y_limpiar_respuesta()
                return jsonify(resp), 200
        except:
            resp = instancia_respuesta.responder_error("Error en el codigo interno del metodo de lagrange")
            return jsonify(resp), 400
        




