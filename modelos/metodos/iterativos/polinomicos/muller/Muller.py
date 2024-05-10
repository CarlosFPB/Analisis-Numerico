import  sympy as sp
import numpy as np
from .....extras.Funciones import errores, respuesta_json

class metodo_muller():


    def calcular_Muller(json_data):
        try:
            # Definir símbolos
            x = sp.symbols('x')
            #intsancia de respuesta
            instancia_respuesta = respuesta_json()
            
            # obtengo los valores del json
            f_x_crudo = json_data["funcion"]
            x0_crudo = json_data["x0"]
            x1_crudo = json_data["x1"]
            x2_crudo = json_data["x2"]
            tolerancia_crudo = json_data["tolerancia"]
            try:
                f_x = sp.sympify(f_x_crudo)
            except:
                return instancia_respuesta.responder_error("La función ingresada es inválida, ingrese una funcion valida"), 400
            x0 = float(x0_crudo)
            x1 = float(x1_crudo)
            x2 = float(x2_crudo)
            error_aceptado = float(tolerancia_crudo)

            #hacemos la primera iteracion para el frontend
            #calcular evaluadas
            f_x0 = f_x.subs(x, x0)
            f_x1 = f_x.subs(x, x1)
            f_x2 = f_x.subs(x, x2)

            #calcular h0 y h1
            h0 = x1 - x0
            h1 = x2 - x1

            #calcular delta0 y delta1
            delta0 = (f_x1 - f_x0) / h0
            delta1 = (f_x2 - f_x1) / h1

            #calcular a, b, c
            a = (delta1 - delta0) / (h1 + h0)
            b = a * h1 + delta1
            c = f_x2

            #calcular D
            D = (sp.sqrt(b**2 - 4*a*c))

            if abs(b + D) > abs(b - D):
                x_calculado = x2 + ((-2*c)/(b + D)) #en la diapositiva de la ingeniera sale b**2 chapra no
            else:
                x_calculado = x2 + ((-2*c)/(b - D))# con b**2 tarda muchas iteraciones

            #mensajes del frontend
            instancia_respuesta.agregar_titulo1("Método de Muller")
            instancia_respuesta.agregar_clave_valor("Función", f_x)
            instancia_respuesta.agregar_parrafo("Primer paso: Se evalua la función en los puntos x0, x1 y x2")
            instancia_respuesta.agregar_parrafo(f"Se evalua f(x0) = {f_x0}")
            instancia_respuesta.agregar_parrafo(f"Se evalua f(x1) = {f_x1}")
            instancia_respuesta.agregar_parrafo(f"Se evalua f(x2) = {f_x2}")
            instancia_respuesta.agregar_parrafo("Segundo paso: Se calculan las diferencias divididas")
            instancia_respuesta.agregar_parrafo(f"Se calcula h0 = x1 - x0 = {x1} - {x0} = {x1 - x0}")
            instancia_respuesta.agregar_parrafo(f"Se calcula h1 = x2 - x1 = {x2} - {x1} = {x2 - x1}")
            instancia_respuesta.agregar_parrafo(f"Se calcula delta0 = (f(x1) - f(x0)) / h0 = ({f_x1} - {f_x0}) / {h0} = {delta0}")
            instancia_respuesta.agregar_parrafo(f"Se calcula delta1 = (f(x2) - f(x1)) / h1 = ({f_x2} - {f_x1}) / {h1} = {delta1}")
            instancia_respuesta.agregar_parrafo("Tercer paso: Se calculan los coeficientes a, b y c")
            instancia_respuesta.agregar_parrafo(f"Se calcula a = (delta1 - delta0) / (h1 + h0) = ({delta1} - {delta0}) / ({h1} + {h0}) = {a}")
            instancia_respuesta.agregar_parrafo(f"Se calcula b = a * h1 + delta1 = {a} * {h1} + {delta1} = {b}")
            instancia_respuesta.agregar_parrafo(f"Se calcula c = f(x2) = {f_x2}")
            instancia_respuesta.agregar_parrafo("Cuarto paso: Se calcula D")
            instancia_respuesta.agregar_parrafo(f"Se calcula D = sqrt(b^2 - 4*a*c) = sqrt({b}^2 - 4*{a}*{c}) = {D}")
            instancia_respuesta.agregar_parrafo("Quinto paso: Se calcula la raíz")
            instancia_respuesta.agregar_parrafo(f"Se calcula x_calculado = x2 + ((-2*c)/(b + D)) = {x2} + ((-2*{c})/({b} + {D})) = {x_calculado}")
            error_acomulado = errores.error_aproximado_porcentual(x2,x_calculado)
            instancia_respuesta.agregar_parrafo(f"Se calcula el error acomulado = {error_acomulado}")
            instancia_respuesta.agregar_parrafo("Sexto paso: Se evalua si el error es menor a la tolerancia sino se digue iterando")
           
            iteracion = 0
            tabla_final = []
            instancia_respuesta.crear_tabla()
            instancia_respuesta.agregar_fila(["Iteración", "x0", "x1", "x2", "x_calculado", "Error acomulado"])
            while True:
                iteracion +=1
                #calcular evaluadas
                f_x0 = f_x.subs(x, x0)
                f_x1 = f_x.subs(x, x1)
                f_x2 = f_x.subs(x, x2)

                #calcular h0 y h1
                h0 = x1 - x0
                h1 = x2 - x1

                #calcular delta0 y delta1
                delta0 = (f_x1 - f_x0) / h0
                delta1 = (f_x2 - f_x1) / h1

                #calcular a, b, c
                a = (delta1 - delta0) / (h1 + h0)
                b = a * h1 + delta1
                c = f_x2

                #calcular D
                D = (sp.sqrt(b**2 - 4*a*c))

                if abs(b + D) > abs(b - D):
                    x_calculado = x2 + ((-2*c)/(b + D)) #en la diapositiva de la ingeniera sale b**2 chapra no
                else:
                    x_calculado = x2 + ((-2*c)/(b - D))# con b**2 tarda muchas iteraciones


                #Error acomulado
                error_acomulado = errores.error_aproximado_porcentual(x2,x_calculado)
                instancia_respuesta.agregar_fila([iteracion, x0, x1, x2, x_calculado, error_acomulado])
                #ahy error cuando el metodo tiene un error muy grande rompe el codigo ya q no puede vealuar la comparacion
                if error_acomulado < error_aceptado:
                    break
                #sino cambiar valores
                x0 = x1
                x1 = x2
                x2 = x_calculado

            instancia_respuesta.agregar_titulo1("Resultado")
            instancia_respuesta.agregar_tabla()
            instancia_respuesta.agregar_parrafo(f"La raíz aproximada es: {x_calculado}")
            instancia_respuesta.agregar_parrafo(f"El error acomulado es: {error_acomulado}")
            instancia_respuesta.agregar_parrafo(f"Iteraciones: {iteracion}")
            resp = instancia_respuesta.obtener_y_limpiar_respuesta()
            return resp, 200
        except Exception as e:
            return instancia_respuesta.responder_error(f"Error durante el procedimiento\nError: {e}"), 500