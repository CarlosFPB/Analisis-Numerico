
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

    def obtener_respuesta(self):
        return self.respuesta
    
    def limpiar_respuesta(self):
        self.respuesta = []
        return self.respuesta
    
    def crear_tabla(self):
        self.tabla = []
        return []
    
    def agregar_fila(self, fila):
        self.tabla.append(str(fila))
        return self.tabla
    
    def obtener_tabla(self):
        return self.tabla
    
    def obtener_y_limpiar_respuesta(self):
        res = self.respuesta
        self.limpiar_respuesta()
        return res
    

