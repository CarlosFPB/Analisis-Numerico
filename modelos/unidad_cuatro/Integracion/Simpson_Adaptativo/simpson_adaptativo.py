from flask import jsonify
import sympy as sp
from ....extras.Funciones import respuesta_json
from ....extras.latex import conversla, conversla_html
from ....extras.Integrales import integr_obtener

class simpson_adaptativo():
    @staticmethod
    def calcular_simpson_adaptativo(json_data):
        instancia_respuesta = respuesta_json()
        
        try:
            # Obtener integral
            try:
                f_x = conversla.latex_(json_data["latex"])
                epsilon = float(json_data["tolerancia"])
            except (sp.SympifyError, TypeError):
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400
            except KeyError:
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400
            except:
                resp = instancia_respuesta.responder_error("No se ingreso una integral")
                return jsonify(resp), 400
           
            try:
                funcion, variables, limites = integr_obtener.integr_Obtener(f_x)
            except ValueError as e:
                resp = instancia_respuesta.responder_error("La integral tiene que ser definida (contener limites)")
                return jsonify(resp), 400
            except NameError as e:
                resp = instancia_respuesta.responder_error("La integral no se ingreso correctamente o se introdujo un caracter especial")
                return jsonify(resp), 400
            except Exception as e:
                resp = instancia_respuesta.responder_error("Error en la integral ingresada")
                return jsonify(resp), 400
            
            if len(variables) > 1:
                    resp = instancia_respuesta.responder_error("La integral debe ser unidimensional")
                    return jsonify(resp), 400

            instancia_respuesta.agregar_titulo1("Método Simpson Adaptativo")
            fx1 = conversla_html.mathl_(f_x)
            instancia_respuesta.agregar_parrafo(f"Integral {fx1}")
            instancia_respuesta.agregar_titulo1("Datos")

            def f(punto):
                return sp.N(funcion.subs(variables[0], punto))
            
            def recursivo_simpson(f, a, b, epsilon):
                h = b - a
                c = (a + b) / 2
                s_ab = h * (f(a) + 4 * f(c) + f(b)) / 6
                
                # División en dos subintervalos
                d = (a + c) / 2
                e = (c + b) / 2
                s_ac = (c - a) * (f(a) + 4 * f(d) + f(c)) / 6
                s_cb = (b - c) * (f(c) + 4 * f(e) + f(b)) / 6
                
                instancia_respuesta.agregar_parrafo("Intervalo [a, b]: [{}, {}]".format(a, b))
                instancia_respuesta.agregar_parrafo("Intervalo [a, c]: [{}, {}]".format(a, c))
                instancia_respuesta.agregar_parrafo("Intervalo [c, b]: [{}, {}]".format(c, b))
                
                instancia_respuesta.agregar_parrafo("s_ab: {}".format(s_ab))
                instancia_respuesta.agregar_parrafo("s_ac: {}".format(s_ac))
                instancia_respuesta.agregar_parrafo("s_cb: {}".format(s_cb))
                
                if abs(s_ac + s_cb - s_ab) < 15 * epsilon:
                    return s_ac + s_cb + (s_ac + s_cb - s_ab) / 15
                else:
                    return recursivo_simpson(f, a, c, epsilon/2) + recursivo_simpson(f, c, b, epsilon/2)
            resultado = recursivo_simpson(f, limites[0], limites[1], epsilon)
            

            instancia_respuesta.agregar_clave_valor_segundo("Resultado", sp.N(resultado))
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = instancia_respuesta.responder_error("Error interno en el servidor")
            return jsonify(resp), 500