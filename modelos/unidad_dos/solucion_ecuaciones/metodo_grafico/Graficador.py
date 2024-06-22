import sympy as sp
from modelos.extras.Funciones import respuesta_json, verificaciones
import math
from modelos.extras.Funciones import respuesta_json, verificaciones, commprobaciones_json
from flask import jsonify
from modelos.extras.latex import conversla
import sympy as sp
import numpy as np
import io
import base64
import matplotlib.pyplot as plt

class graficador:
    
    def calcular_grafico(json_data):
        x = sp.symbols('x')
        #istanciar la respuesta
        respuesta = respuesta_json()

        try:
            #Verificar la funcion obtenida
            response, status_code = commprobaciones_json.comprobar_funcionX_latex(json_data, respuesta)
            if status_code != 200:
                resp = response
                return resp, 400
            f_x = response
        except Exception as e:
            resp = respuesta.responder_error("Error al obtener la función ingresada: "+str(e))
            return jsonify(resp), 400
        
        try:
            f_x_crudo = sp.expand(f_x_crudo)#para que se vea bien la funcion
            f_x = f_x_crudo
            respuesta.agregar_clave_valor("Funcion", f"{f_x}")

            x_vals = []
            y_vals = []

            dominio = sp.calculus.util.continuous_domain(f_x, x, sp.S.Reals)
            
                            
            try:
                if dominio.is_Union:
                    for interval in dominio.args:
                        respuesta.agregar_clave_valor("Dominio", f"({interval.start}, {interval.end})")
                else:
                    respuesta.agregar_clave_valor("Dominio", f"({dominio.start}, {dominio.end})")
            except:
                respuesta.agregar_clave_valor("Dominio", "(-∞, ∞)")


            roots = sp.solve(f_x)
            complexs = []


            for i in range(len(roots)):
                try:
                    roots[i] = float(roots[i])
                except:
                    complexs.append(roots[i])


            for complex in complexs:
                roots.remove(complex)

            if len(complexs) > 0 and len(roots) > 0:
                respuesta.agregar_clave_valor("Raices Reales", f"{roots}")
                respuesta.agregar_parrafo("Esta funcion tiene " + str(len(complexs)) + " raices complejas")
            elif len(complexs) > 0:
                respuesta.agregar_parrafo("Esta funcion no tiene raices reales")
                respuesta.agregar_clave_valor("Raices Complejas", f"{complexs}")
            elif len(roots) > 0:
                respuesta.agregar_clave_valor("Raices Reales", f"{roots}")

            STEPS = 100
            first = -10
            last = 10

            if dominio.start.is_infinite and dominio.end.is_infinite:
                if len(roots) > 0:
                    first = float(roots[0]-10)
                    last = float(roots[-1]+10)
                x_vals = np.linspace(first, last, STEPS)
            else:
                # si el limite superior/derecha es infinito
                if dominio.end.is_infinite:
                    if len(roots) > 0:
                        first = float(dominio.start)
                        last = float(roots[-1]+10)

                    if dominio.left_open:
                        x_vals = np.linspace(first + 0.001, last, STEPS)
                    else:
                        x_vals = np.linspace(first, last, STEPS)

                # si el limite inferior/izquierda es infinito
                elif dominio.start.is_infinite:
                    if len(roots) > 0:
                        first = float(roots[-1]-10)
                        last = float(dominio.end)
                    if dominio.right_open:
                        x_vals = np.linspace(first, last-0.001, STEPS)
                    else:
                        x_vals = np.linspace(first, last, 1000)

            # Obtener valores de f(x) #
            for x_val in x_vals:
                y_vals.append(f_x.subs(x, x_val).evalf() )  

            # graficar #
            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label=f"{f_x}", color="green")
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid("both")
            ax.scatter(roots, [0,] * len(roots), color="red", label="Raices")

            for i, root in enumerate(roots):
                position = 'top'
                if i % 2 == 0:
                    position = 'bottom'
                ax.text(root, 0, f'({round(root,2)}, 0)', ha='center', va=position)

            ax.legend()

            # Save the figure as a byte array
            image_bytes = io.BytesIO()
            plt.savefig(image_bytes, format='jpg')
            image_bytes.seek(0)

            # Convert the byte array to base64 string
            image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            respuesta.agregar_titulo1("Grafico de la funcion")
            respuesta.agregar_imagen(image_base64)
            resp = respuesta.obtener_y_limpiar_respuesta()
            return jsonify(resp), 200
        except Exception as e:
            resp = respuesta.responder_error("Error en el codigo interno\n"+str(e))
            return jsonify(resp), 500