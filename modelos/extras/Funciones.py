
import sympy as sp

class errores():

    @staticmethod
    def error_verdadero(valor_aproximado, valor_real):
        return abs(valor_real - valor_aproximado)
    
    @staticmethod
    def error_relativo_largo(valor_aproximado, valor_real):
        if valor_real == 0:
            return 0
        return abs(valor_real - valor_aproximado) / valor_real
    
    @staticmethod
    def error_relativo_corto(error_verdadero, valor_real):
        if valor_real == 0:
            return 0
        return abs(error_verdadero/valor_real)

    @staticmethod
    def error_relativo_porcentual_largo(valor_aproximado, valor_real):
        if valor_real == 0:
            return 0
        return abs(valor_real - valor_aproximado) / valor_real * 100
    
    @staticmethod
    def error_relativo_porcentual_corto(error_relativo):
        return error_relativo * 100
    
    @staticmethod
    def error_aproximado(valor_anterior, valor_actual):
        if valor_actual == 0:
            return 0
        return abs((valor_actual - valor_anterior) / valor_actual)
    
    @staticmethod
    def error_aproximado_porcentual(valor_anterior, valor_actual):
        if valor_actual == 0:
            return 0
        return abs((valor_actual - valor_anterior) / valor_actual) * 100
    
    @staticmethod
    def error_de_tolerancia(cantidad_de_cifras_significativas):
        return 0.5 * 10 ** (2-cantidad_de_cifras_significativas)
        

        
class biseccion():

    @staticmethod
    def primera_aproximacion(x1,xu):
        return (x1 + xu)/2
    
    @staticmethod
    def multiplicacion_evaluadas(funcion,x1,xr):
        x = sp.symbols('x')
        f_x = funcion
        respuesta = f_x.subs(x, x1) * f_x.subs(x, xr)
        return respuesta

      
class falsaPosicion():
    
    @staticmethod
    def primera_aproximacion(funcion,x1,xu):
        x = sp.symbols('x')
        f_x = funcion
        funcion_evaluada_x1 = f_x.subs(x, x1)
        funcion_evaluada_xu = f_x.subs(x, xu)

        respuesta = xu - (funcion_evaluada_xu * (x1 - xu))/(funcion_evaluada_x1-funcion_evaluada_xu)
        return float(respuesta)

    @staticmethod
    def multiplicacion_evaluadas(funcion,x1,xr):
        x = sp.symbols('x')
        f_x = funcion
        respuesta = (f_x.subs(x, x1)) * (f_x.subs(x, xr))
        return float(respuesta)
    
    
class evaluarfuncion():
    
    @staticmethod
    def evaluar(funcion,var):
        x = sp.symbols('x')
        f_x = funcion
        return float(f_x.subs(x, var))
    


class newton():
    
    @staticmethod
    def aproximacion(f_x_evaluada,f_prima_evaluada,x0):
        respuesta = x0 - (f_x_evaluada/f_prima_evaluada)
        return float(respuesta)
    
class secante():
    
    @staticmethod
    def aproximacion(f_x_evaluada_anterior, f_x_evaluada_actual, x_anterior, x_actual):
        respuesta = x_actual - (f_x_evaluada_actual * (x_anterior - x_actual))/(f_x_evaluada_anterior - f_x_evaluada_actual)
        return float(respuesta)



class newton_modificado():
    
    @staticmethod
    def aproximacion(f_x_evaluada,f_prima_evaluada,f_prima_prima_evaluada,x0):
        respuesta = x0 - (f_x_evaluada * f_prima_evaluada)/(f_prima_evaluada**2 - f_x_evaluada * f_prima_prima_evaluada)
        return float(respuesta)
    

class integr_obtener():

    @staticmethod
    def integr_Obtener(sympy_expr):
    
        funciones = []
        variables = []
        limites2 = [] 

        # Si la expresión es una suma de integrales, extraer cada una
        if isinstance(sympy_expr, sp.Add):
            num_inte = 0   
            for term in sympy_expr.args:
                if isinstance(term, sp.Integral):
                    #Verifica el numero de integral
                    tipo_integral = len(term.limits)
                    #extraer_funcion_limites(term, tipo_integral, num_inte)
                    if isinstance(term, sp.Integral):
                        funcion = term.function
                        if num_inte == 0:
                            for i in range(tipo_integral):
                                limites = term.limits[i]
                                variable, limite_inferior, limite_superior = limites
                                variables.append(variable)
                                limites2.append(limite_inferior)
                                limites2.append(limite_superior)
                        funciones.append(funcion)
                        num_inte =+ 1
                    else:
                        raise ValueError("El objeto proporcionado no es una integral válida")          
        else:
            # Caso en que solo hay una integral
            if isinstance(sympy_expr, sp.Integral):
                tipo_integral = len(sympy_expr.limits)

                for i in range(tipo_integral):
                        limites = sympy_expr.limits[i]
                        variable, limite_inferior, limite_superior = limites
                        variables.append(variable)
                        limites2.append(limite_inferior)
                        limites2.append(limite_superior)

                funcion = sympy_expr.function
                funciones = [funcion]

        # Sumar las funciones
        suma_funciones = sum(funciones)
        print("Suma funciones: ", suma_funciones)

        # Verificar que todos los límites sean iguales (asumimos que son iguales para simplificar)
        print("Funciones extraídas y límites:")
        for funcion in funciones:
            print("Función:", funcion)

        for limite in limites2:
            print("Limite:", limite)

        #Variables#
        for variable in variables:
            print("Variable:", variable)

        print(f"Tipo limites: {limites2[0]}", type(limites2[0]))
        print(f"Tipo limites: {variables[0]}", type(variables[0]))


        return suma_funciones, variables, limites2


class verificaciones():

    @staticmethod
    def es_polinomio(funcion):
        x = sp.symbols('x')
        poly_funcion = funcion.as_poly(x)
        if poly_funcion is None:
            return False
        return True
    
    #returna none si no es polinomica
    @staticmethod
    def obtener_grado(funcion):
        x = sp.symbols('x')
        if not verificaciones.es_polinomio(funcion):
            return None
        poly_funcion = funcion.as_poly(x)
        return poly_funcion.degree()
    
    
    @staticmethod
    def obtener_coeficientes(funcion):
        #ordenado del grado mayor al menor
        x = sp.symbols('x')
        poly_funcion = funcion.as_poly(x)
        grado = poly_funcion.degree()
        coeficientes = [poly_funcion.coeff_monomial(x**i) for i in range(grado, -1, -1)]#aunq haya 0
        return coeficientes
    
    def obtener_coeficientes_de_y(funcion):
        #ordenado del grado mayor al menor
        y = sp.symbols('y')
        poly_funcion = funcion.as_poly(y)
        grado = poly_funcion.degree()
        coeficientes = [poly_funcion.coeff_monomial(y**i) for i in range(grado, -1, -1)]
        return coeficientes
    
    @staticmethod
    def posee_raices_reales(funcion):
        x = sp.symbols('x')
        soluciones = sp.solve(sp.Eq(funcion, 0), x)
        if not any(sol.is_real for sol in soluciones):
            return False
        return True
    
    @staticmethod
    def es_matriz(matriz):
        if isinstance(matriz, list) and all(isinstance(row, list) for row in matriz):
            return True
        else:
            return False
        

    def es_entero(parametro):
        if isinstance(parametro, int):
            return True
        elif isinstance(parametro, str):
            return parametro.isdigit()
        else:
            return False
        
    
    @staticmethod
    def verificar_numeros_matriz(matriz):
        for row in matriz:
            if not isinstance(row, list):
                return False
            for element in row:
                if isinstance(element, str):
                    try:
                        # Intentar convertir la cadena a un número
                        float(element)
                    except ValueError:
                        return False
                elif not isinstance(element, (float, int)):
                    return False
        return True

        
    @staticmethod
    def verificar_puntos_unicos(puntos):
        if len(puntos) == len(set(puntos)):
            return True
        else:
            return False


class respuesta_json():
    respuesta = []
    tabla = []

    def __init__(self) -> None:
        self.respuesta = []

    def agregar_titulo1(self, contenido):
        self.respuesta.append({'type': 'titulo1', 'content': str(contenido)})

    def agregar_parrafo(self, contenido):
        self.respuesta.append({'type': 'parrafo', 'content': str(contenido)})

    def agregar_tabla(self):
        self.respuesta.append({'type': 'tabla', 'content': self.tabla})

    def agregar_clave_valor(self,clave ,contenido):
        cont = [str(clave), str(contenido)]
        self.respuesta.append({'type': "clavevalor", 'content': cont})

    def agregar_divicion_sinterica(self, contenido):
        #contenido es una matriz con 3 filas
        resp = []
        for i in contenido:
            convertidas = []
            for j in i:
                convertidas.append(str(j))
            resp.append(convertidas)
        self.respuesta.append({'type': 'divicionsinterica', 'content': resp})
        

    def responder_error(self, contenido):
        self.respuesta = []
        resp = {'error' :  str(contenido)}
        return resp

    def obtener_respuesta(self):
        return self.respuesta
    
    def limpiar_respuesta(self):
        self.respuesta = []
        return self.respuesta
    
    def crear_tabla(self):
        self.tabla = []
        return []
    
    def agregar_fila(self, fila):
        convertidas = []
        for i in fila:
            convertidas.append(str(i))
        fila = convertidas

        self.tabla.append(fila)
        return self.tabla
    
    def obtener_tabla(self):
        return self.tabla
    
    def obtener_y_limpiar_respuesta(self):
        res = self.respuesta
        self.tabla = []
        self.limpiar_respuesta()
        return res
    
    def responder_solo_respuesta(self, contenido):
        self.respuesta = []
        res = {'respuesta' :  str(contenido)}
        return res

