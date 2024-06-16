import sympy as sp
from flask import jsonify
from modelos.extras.Funciones import verificaciones, respuesta_json
from modelos.extras.Derivadas import Diferenciacion

class metodos_diferenciacion():

    #parametros
    #"metodo"    #string con el nombre del metodo
    #"orden"       #int con el orden de la derivada entre 1 y 4, el de 5 y 3 puntos no nesesita orden es 1 automatico
    #"version"      #int con la version del metodo entre 1 y 2 y 5 puntos 5 versiones
    #"h"               #float con el valor de h mayor a 0
    #"xi"              #float con el valor de xi cualquier numero
    #"funcion"      #string con la funcion a derivar

    def calcular_derivada(json_data):
        x = sp.symbols('x')
        instancia_respuesta = respuesta_json()
        try:
            f_x = sp.simplify(json_data["funcion"])
            rs = f_x.subs(x, 2)
            if rs > 0:
                pass
            #verificar que sea grado mayor a 0 si es polinomica
            if verificaciones.obtener_grado(f_x) != None:#es porq es polinomica sino lo es no importa el grado
                if verificaciones.obtener_grado(f_x) < 1:
                    resp = instancia_respuesta.responder_error("La funcion es una constante")
                    return jsonify(resp), 400
        except sp.SympifyError:
            resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
            return jsonify(resp), 400
        except TypeError as e:
            resp = instancia_respuesta.responder_error("Error en la funcion ingresada")
            return jsonify(resp), 400
        
        #Verificar los valores iniciales
        try:
            metodo = json_data["metodo"]
            orden = int(json_data["orden"])
            version = int(json_data["version"])
            h = float(json_data["h"])
            xi = float(json_data["xi"])
        except ValueError as e:
            resp = instancia_respuesta.responder_error(f"Error en los valores iniciales\n {str(e)}")
            return jsonify(resp), 400
        
        #evaluar errores en parametros
        if h <= 0:
            resp = instancia_respuesta.responder_error("El valor de h debe ser mayor a 0")
            return jsonify(resp), 400
        if metodo != "adelante" and metodo != "central" and metodo != "atras" and metodo != "cinco_puntos" and metodo != "tres_puntos":
            resp = instancia_respuesta.responder_error("El metodo debe ser adelante, central, atras, cinco_puntos o tres_puntos")
            return jsonify(resp), 400
        if orden < 1 or orden > 4 and metodo != "cinco_puntos" and metodo != "tres_puntos":
            resp = instancia_respuesta.responder_error("El orden de la derivada debe ser entre 1 y 4")
            return jsonify(resp), 400
        if metodo == "cinco_puntos" and version < 1 and version > 5:
            resp = instancia_respuesta.responder_error("La version del metodo cinco_puntos debe ser entre 1 y 5")
            return jsonify(resp), 400
        elif version < 1 or version > 2 and metodo != "cinco_puntos":
            resp = instancia_respuesta.responder_error("La version del metodo debe ser entre 1 y 2")
            return jsonify(resp), 400

        #calcular la derivada
        try:
            instancia_respuesta.agregar_titulo1("Diferenciación numérica")
            instancia_respuesta.agregar_parrafo("Se calculará la derivada de la función")
            instancia_respuesta.agregar_parrafo(str(f_x))
            instancia_respuesta.agregar_parrafo("En el punto xi = "+str(xi))
            instancia_respuesta.agregar_parrafo("Con h = "+str(h))

            #instancia de las derivadas
            m_derivada = Diferenciacion()
            if metodo == "adelante":
                instancia_respuesta.agregar_titulo1("Usando el metodo de diferenciación hacia adelante")
                if version == 1:
                    if orden == 1:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la primera derivada")
                        instancia_respuesta.agregar_parrafo("f'(x) = (f(x+h) - f(x))/h")
                        derivada = m_derivada.finita_hacia_delante.primera_derivada_v1(f_x, xi, h)
                    elif orden == 2:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la segunda derivada")
                        instancia_respuesta.agregar_parrafo("f''(x) = (f(x+2h) - 2f(x+h) + f(x))/h^2")
                        derivada = m_derivada.finita_hacia_delante.segunda_derivada_v1(f_x, xi, h)
                    elif orden == 3:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la tercera derivada")
                        instancia_respuesta.agregar_parrafo("f'''(x) = (f(x+3h) - 3f(x+2h) + 3f(x+h) - f(x))/h^3")
                        derivada = m_derivada.finita_hacia_delante.tercer_derivada_v1(f_x, xi, h)
                    elif orden == 4:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la cuarta derivada")
                        instancia_respuesta.agregar_parrafo("f''''(x) = (f(x+4h) - 4f(x+3h) + 6f(x+2h) - 4f(x+h) + f(x))/h^4")
                        derivada = m_derivada.finita_hacia_delante.cuarta_derivada_v1(f_x, xi, h)
                elif version == 2:
                    if orden == 1:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la primera derivada")
                        instancia_respuesta.agregar_parrafo("f'(x) = (-f(x+2h) + 4f(x+h) - 3f(x))/2h")
                        derivada = m_derivada.finita_hacia_delante.primera_derivada_v2(f_x, xi, h)
                    elif orden == 2:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la segunda derivada")
                        instancia_respuesta.agregar_parrafo("f''(x) = (2f(x+2h) - 5f(x+h) + 4f(x) - f(x-h))/h^2")
                        derivada = m_derivada.finita_hacia_delante.segunda_derivada_v2(f_x, xi, h)
                    elif orden == 3:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la tercera derivada")
                        instancia_respuesta.agregar_parrafo("f'''(x) = (-f(x+3h) + 8f(x+2h) - 13f(x+h) + 13f(x) - 5f(x-h))/2h^3")
                        derivada = m_derivada.finita_hacia_delante.tercer_derivada_v2(f_x, xi, h)
                    elif orden == 4:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la cuarta derivada")
                        instancia_respuesta.agregar_parrafo("f''''(x) = (3f(x+2h) - 14f(x+h) + 26f(x) - 24f(x-h) + 11f(x-2h) - 2f(x-3h))/h^4")
                        derivada = m_derivada.finita_hacia_delante.cuarta_derivada_v2(f_x, xi, h)
            elif metodo == "central":
                instancia_respuesta.agregar_titulo1("Usando el metodo de diferenciación central")
                if version == 1:
                    if orden == 1:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la primera derivada")
                        instancia_respuesta.agregar_parrafo("f'(x) = (f(x+h) - f(x-h))/2h")
                        derivada = m_derivada.finita_central.primera_derivada_v1(f_x, xi, h)
                    elif orden == 2:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la segunda derivada")
                        instancia_respuesta.agregar_parrafo("f''(x) = (f(x+h) - 2f(x) + f(x-h))/h^2")
                        derivada = m_derivada.finita_central.segunda_derivada_v1(f_x, xi, h)
                    elif orden == 3:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la tercera derivada")
                        instancia_respuesta.agregar_parrafo("f'''(x) = (f(x+2h) - 2f(x+h) + 2f(x-h) - f(x-2h))/2h^3")
                        derivada = m_derivada.finita_central.tercer_derivada_v1(f_x, xi, h)
                    elif orden == 4:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la cuarta derivada")
                        instancia_respuesta.agregar_parrafo("f''''(x) = (f(x+2h) - 4f(x+h) + 6f(x) - 4f(x-h) + f(x-2h))/h^4")
                        derivada = m_derivada.finita_central.cuarta_derivada_v1(f_x, xi, h)
                elif version == 2:
                    if orden == 1:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la primera derivada")
                        instancia_respuesta.agregar_parrafo("f'(x) = (f(x+2h) - f(x-2h))/4h")
                        derivada = m_derivada.finita_central.primera_derivada_v2(f_x, xi, h)
                    elif orden == 2:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la segunda derivada")
                        instancia_respuesta.agregar_parrafo("f''(x) = (f(x+2h) - 2f(x+h) + 2f(x-h) - f(x-2h))/4h^2")
                        derivada = m_derivada.finita_central.segunda_derivada_v2(f_x, xi, h)
                    elif orden == 3:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la tercera derivada")
                        instancia_respuesta.agregar_parrafo("f'''(x) = (f(x+3h) - 3f(x+2h) + 3f(x-h) - f(x-3h))/8h^3")
                        derivada = m_derivada.finita_central.tercer_derivada_v2(f_x, xi, h)
                    elif orden == 4:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la cuarta derivada")
                        instancia_respuesta.agregar_parrafo("f''''(x) = (f(x+2h) - 4f(x+h) + 6f(x) - 4f(x-h) + f(x-2h))/h^4")
                        derivada = m_derivada.finita_central.cuarta_derivada_v2(f_x, xi, h)
            elif metodo == "atras":
                instancia_respuesta.agregar_titulo1("Usando el metodo de diferenciación hacia atras")
                if version == 1:
                    if orden == 1:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la primera derivada")
                        instancia_respuesta.agregar_parrafo("f'(x) = (f(x) - f(x-h))/h")
                        derivada = m_derivada.finita_hacia_atras.primera_derivada_v1(f_x, xi, h)
                    elif orden == 2:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la segunda derivada")
                        instancia_respuesta.agregar_parrafo("f''(x) = (f(x) - 2f(x-h) + f(x-2h))/h^2")
                        derivada = m_derivada.finita_hacia_atras.segunda_derivada_v1(f_x, xi, h)
                    elif orden == 3:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la tercera derivada")
                        instancia_respuesta.agregar_parrafo("f'''(x) = (f(x) - 3f(x-h) + 3f(x-2h) - f(x-3h))/h^3")
                        derivada = m_derivada.finita_hacia_atras.tercer_derivada_v1(f_x, xi, h)
                    elif orden == 4:
                        instancia_respuesta.agregar_parrafo("Usando la version 1 de la cuarta derivada")
                        instancia_respuesta.agregar_parrafo("f''''(x) = (f(x) - 4f(x-h) + 6f(x-2h) - 4f(x-3h) + f(x-4h))/h^4")
                        derivada = m_derivada.finita_hacia_atras.cuarta_derivada_v1(f_x, xi, h)
                elif version == 2:
                    if orden == 1:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la primera derivada")
                        instancia_respuesta.agregar_parrafo("f'(x) = (3f(x) - 4f(x-h) + f(x-2h))/2h")
                        derivada = m_derivada.finita_hacia_atras.primera_derivada_v2(f_x, xi, h)
                    elif orden == 2:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la segunda derivada")
                        instancia_respuesta.agregar_parrafo("f''(x) = (2f(x) - 5f(x-h) + 4f(x-2h) - f(x-3h))/h^2")
                        derivada = m_derivada.finita_hacia_atras.segunda_derivada_v2(f_x, xi, h)
                    elif orden == 3:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la tercera derivada")
                        instancia_respuesta.agregar_parrafo("f'''(x) = (5f(x) - 18f(x-h) + 24f(x-2h) - 14f(x-3h) + 3f(x-4h))/2h^3")
                        derivada = m_derivada.finita_hacia_atras.tercer_derivada_v2(f_x, xi, h)
                    elif orden == 4:
                        instancia_respuesta.agregar_parrafo("Usando la version 2 de la cuarta derivada")
                        instancia_respuesta.agregar_parrafo("f''''(x) = (11f(x) - 56f(x-h) + 114f(x-2h) - 104f(x-3h) + 35f(x-4h) - 6f(x-5h))/h^4")
                        derivada = m_derivada.finita_hacia_atras.cuarta_derivada_v2(f_x, xi, h)
            elif metodo == "cinco_puntos":
                instancia_respuesta.agregar_titulo1("Usando el metodo de diferenciación cinco puntos")
                if version == 1:
                    instancia_respuesta.agregar_parrafo("Usando la version 1 de la primera derivada")
                    instancia_respuesta.agregar_parrafo("f'(x) = (-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h))/12h")
                    derivada = m_derivada.finita_cinco_puntos.primera_derivada_v1(f_x, xi, h)
                elif version == 2:
                    instancia_respuesta.agregar_parrafo("Usando la version 2 de la primera derivada")
                    instancia_respuesta.agregar_parrafo("f'(x) = (f(x+2h) - 8f(x+h) + 8f(x-h) - f(x-2h))/12h")
                    derivada = m_derivada.finita_cinco_puntos.primera_derivada_v2(f_x, xi, h)
                elif version == 3:
                    instancia_respuesta.agregar_parrafo("Usando la version 3 de la primera derivada")
                    instancia_respuesta.agregar_parrafo("f'(x) = (-f(x+3h) + 9f(x+2h) - 45f(x+h) + 45f(x-h) - 9f(x-2h) + f(x-3h))/60h")
                    derivada = m_derivada.finita_cinco_puntos.primera_derivada_v3(f_x, xi, h)
                elif version == 4:
                    instancia_respuesta.agregar_parrafo("Usando la version 4 de la primera derivada")
                    instancia_respuesta.agregar_parrafo("f'(x) = (-f(x+3h) + 12f(x+2h) - 39f(x+h) + 56f(x) - 39f(x-h) + 12f(x-2h) - f(x-3h))/6h")
                    derivada = m_derivada.finita_cinco_puntos.primera_derivada_v4(f_x, xi, h)
                elif version == 5:
                    instancia_respuesta.agregar_parrafo("Usando la version 5 de la primera derivada")
                    instancia_respuesta.agregar_parrafo("f'(x) = (f(x+3h) - 9f(x+2h) + 45f(x+h) - 45f(x-h) + 9f(x-2h) - f(x-3h))/60h")
                    derivada = m_derivada.finita_cinco_puntos.primera_derivada_v5(f_x, xi, h)
            elif metodo == "tres_puntos":
                instancia_respuesta.agregar_titulo1("Usando el metodo de diferenciación tres puntos")
                if version == 1:
                    instancia_respuesta.agregar_parrafo("Usando la version 1 de la primera derivada")
                    instancia_respuesta.agregar_parrafo("f'(x) = (f(x+h) - f(x-h))/2h")
                    derivada = m_derivada.finita_tres_puntos.primera_derivada_v1(f_x, xi, h)
                elif version == 2:
                    instancia_respuesta.agregar_parrafo("Usando la version 2 de la primera derivada")
                    instancia_respuesta.agregar_parrafo("f'(x) = (-f(x+2h) + 4f(x+h) - 3f(x))/2h")
                    derivada = m_derivada.finita_tres_puntos.primera_derivada_v2(f_x, xi, h)

            #detallar respuestas
            instancia_respuesta.agregar_titulo1("Resultado")
            instancia_respuesta.agregar_parrafo("La derivada de la función es:")
            instancia_respuesta.agregar_clave_valor("Derivada:", derivada)

            try:
                clear = json_data.get("clear", False)
                clearD = json_data.get("clearD", False)
            except:
                clear = clearD = False
            #verifica si viene de richardson con clearD
            if clear or clearD:
                resp = instancia_respuesta.responder_solo_respuesta(derivada)
                return jsonify(resp), 200
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            #responder normalmente
            return jsonify(resp), 200

        except Exception as e:
            resp = instancia_respuesta.responder_error("Error al calcular la derivada"+str(e))
            return jsonify(resp), 400