
import sympy as sp

class errores():

    def __init__(self) -> None:
        pass

    def error_verdadero(valor_aproximado, valor_real):
        return abs(valor_real - valor_aproximado)
    
    def error_relativo_largo(valor_aproximado, valor_real):
        if valor_real == 0:
            return 0
        return abs(valor_real - valor_aproximado) / valor_real
    
    def error_relativo_corto(error_verdadero, valor_real):
        if valor_real == 0:
            return 0
        return abs(error_verdadero/valor_real)

    def error_relativo_porcentual_largo(valor_aproximado, valor_real):
        if valor_real == 0:
            return 0
        return abs(valor_real - valor_aproximado) / valor_real * 100
    
    def error_relativo_porcentual_corto(error_relativo):
        return error_relativo * 100
    


    def error_aproximado(valor_anterior, valor_actual):
        if valor_actual == 0:
            return 0
        return abs((valor_actual - valor_anterior) / valor_actual)
    
    def error_aproximado_porcentual(valor_anterior, valor_actual):
        if valor_actual == 0:
            return 0
        return abs((valor_actual - valor_anterior) / valor_actual) * 100
    

    def error_de_tolerancia(cantidad_de_cifras_significativas):
        return 0.5 * 10 ** (2-cantidad_de_cifras_significativas)
        

        
class biseccion():
    def __init__(self) -> None:
        pass

    def primera_aproximacion(x1,xu):
        return (x1 + xu)/2
    
    def multiplicacion_evaluadas(funcion,x1,xr):
        x = sp.symbols('x')
        f_x = funcion
        respuesta = f_x.subs(x, x1) * f_x.subs(x, xr)
        return respuesta

      
class falsaPosicion():
    
    def __init__(self) -> None:
        pass

    def primera_aproximacion(funcion,x1,xu):
        x = sp.symbols('x')
        f_x = funcion
        funcion_evaluada_x1 = f_x.subs(x, x1)
        funcion_evaluada_xu = f_x.subs(x, xu)

        respuesta = xu - (funcion_evaluada_xu * (x1 - xu))/(funcion_evaluada_x1-funcion_evaluada_xu)
        return float(respuesta)

    def multiplicacion_evaluadas(funcion,x1,xr):
        x = sp.symbols('x')
        f_x = funcion
        respuesta = (f_x.subs(x, x1)) * (f_x.subs(x, xr))
        return float(respuesta)
    
    
class evaluarfuncion():
    def __init__(self) -> None:
        pass

    def evaluar(funcion,var):
        x = sp.symbols('x')
        f_x = funcion
        return float(f_x.subs(x, var))
    


class newton():
    def __init__(self) -> None:
        pass

    def aproximacion(f_x_evaluada,f_prima_evaluada,x0):
        respuesta = x0 - (f_x_evaluada/f_prima_evaluada)
        return float(respuesta)
    
class secante():
    def __init__(self) -> None:
        pass

    def aproximacion(f_x_evaluada_anterior, f_x_evaluada_actual, x_anterior, x_actual):
        respuesta = x_actual - (f_x_evaluada_actual * (x_anterior - x_actual))/(f_x_evaluada_anterior - f_x_evaluada_actual)
        return float(respuesta)



class newton_modificado():
    def __init__(self) -> None:
        pass

    def aproximacion(f_x_evaluada,f_prima_evaluada,f_prima_prima_evaluada,x0):
        respuesta = x0 - (f_x_evaluada * f_prima_evaluada)/(f_prima_evaluada**2 - f_x_evaluada * f_prima_prima_evaluada)
        return float(respuesta)
    

class bairstow():
    def __init__(self) -> None:
        pass

    