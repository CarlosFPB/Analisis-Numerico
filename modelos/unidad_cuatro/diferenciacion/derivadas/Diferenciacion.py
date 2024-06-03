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
            #instancia de las derivadas
            m_derivada = Diferenciacion()
            if metodo == "adelante":
                if version == 1:
                    if orden == 1:
                        derivada = m_derivada.finita_hacia_delante.primera_derivada_v1(f_x, xi, h)
                    elif orden == 2:
                        derivada = m_derivada.finita_hacia_delante.segunda_derivada_v1(f_x, xi, h)
                    elif orden == 3:
                        derivada = m_derivada.finita_hacia_delante.tercer_derivada_v1(f_x, xi, h)
                    elif orden == 4:
                        derivada = m_derivada.finita_hacia_delante.cuarta_derivada_v1(f_x, xi, h)
                elif version == 2:
                    if orden == 1:
                        derivada = m_derivada.finita_hacia_delante.primera_derivada_v2(f_x, xi, h)
                    elif orden == 2:
                        derivada = m_derivada.finita_hacia_delante.segunda_derivada_v2(f_x, xi, h)
                    elif orden == 3:
                        derivada = m_derivada.finita_hacia_delante.tercer_derivada_v2(f_x, xi, h)
                    elif orden == 4:
                        derivada = m_derivada.finita_hacia_delante.cuarta_derivada_v2(f_x, xi, h)
            elif metodo == "central":
                if version == 1:
                    if orden == 1:
                        derivada = m_derivada.finita_central.primera_derivada_v1(f_x, xi, h)
                    elif orden == 2:
                        derivada = m_derivada.finita_central.segunda_derivada_v1(f_x, xi, h)
                    elif orden == 3:
                        derivada = m_derivada.finita_central.tercer_derivada_v1(f_x, xi, h)
                    elif orden == 4:
                        derivada = m_derivada.finita_central.cuarta_derivada_v1(f_x, xi, h)
                elif version == 2:
                    if orden == 1:
                        derivada = m_derivada.finita_central.primera_derivada_v2(f_x, xi, h)
                    elif orden == 2:
                        derivada = m_derivada.finita_central.segunda_derivada_v2(f_x, xi, h)
                    elif orden == 3:
                        derivada = m_derivada.finita_central.tercer_derivada_v2(f_x, xi, h)
                    elif orden == 4:
                        derivada = m_derivada.finita_central.cuarta_derivada_v2(f_x, xi, h)
            elif metodo == "atras":
                if version == 1:
                    if orden == 1:
                        derivada = m_derivada.finita_hacia_atras.primera_derivada_v1(f_x, xi, h)
                    elif orden == 2:
                        derivada = m_derivada.finita_hacia_atras.segunda_derivada_v1(f_x, xi, h)
                    elif orden == 3:
                        derivada = m_derivada.finita_hacia_atras.tercer_derivada_v1(f_x, xi, h)
                    elif orden == 4:
                        derivada = m_derivada.finita_hacia_atras.cuarta_derivada_v1(f_x, xi, h)
                elif version == 2:
                    if orden == 1:
                        derivada = m_derivada.finita_hacia_atras.primera_derivada_v2(f_x, xi, h)
                    elif orden == 2:
                        derivada = m_derivada.finita_hacia_atras.segunda_derivada_v2(f_x, xi, h)
                    elif orden == 3:
                        derivada = m_derivada.finita_hacia_atras.tercer_derivada_v2(f_x, xi, h)
                    elif orden == 4:
                        derivada = m_derivada.finita_hacia_atras.cuarta_derivada_v2(f_x, xi, h)
            elif metodo == "cinco_puntos":
                if version == 1:
                    derivada = m_derivada.finita_cinco_puntos.primera_derivada_v1(f_x, xi, h)
                elif version == 2:
                    derivada = m_derivada.finita_cinco_puntos.primera_derivada_v2(f_x, xi, h)
                elif version == 3:
                    derivada = m_derivada.finita_cinco_puntos.primera_derivada_v3(f_x, xi, h)
                elif version == 4:
                    derivada = m_derivada.finita_cinco_puntos.primera_derivada_v4(f_x, xi, h)
                elif version == 5:
                    derivada = m_derivada.finita_cinco_puntos.primera_derivada_v5(f_x, xi, h)
            elif metodo == "tres_puntos":
                if version == 1:
                    derivada = m_derivada.finita_tres_puntos.primera_derivada_v1(f_x, xi, h)
                elif version == 2:
                    derivada = m_derivada.finita_tres_puntos.primera_derivada_v2(f_x, xi, h)

            instancia_respuesta.agregar_parrafo("La derivada es")
            instancia_respuesta.agregar_parrafo(derivada)
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()

            try:
                clear = json_data.get("clear", False)
                clearD = json_data.get("clearD", False)
            except:
                clear = clearD = False
            #verifica si viene de richardson con clearD
            if clear or clearD:
                resp = instancia_respuesta.responder_solo_respuesta(derivada)
                return jsonify(resp), 200
            #responder normalmente
            return jsonify(resp), 200

        except Exception as e:
            resp = instancia_respuesta.responder_error("Error al calcular la derivada"+str(e))
            return jsonify(resp), 400