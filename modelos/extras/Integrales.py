import sympy as sp


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

        return suma_funciones, variables, limites2




class Trapecio():
    @staticmethod
    def trapecio_simple(a, b, fx0, fx1):
        I = sp.N(((b-a)*(fx0+fx1))/2)
        return I
    
    @staticmethod
    def trapecio_compuesto(a, b, fx0, suma_intermedios, fxn, intervalos):
        I = sp.N((b-a)*((fx0 + 2*suma_intermedios + fxn) / (2*intervalos)))
        return I
    

class Simpson_13():
    @staticmethod
    def simpson_simple(a, b, fx0, fx1, fx2):
        I = sp.N((b-a)*((fx0+4*fx1+fx2) / 6))
        return I

    @staticmethod
    def simpson_compuesto(a, b, fx0, suma_intermedios, suma_subint, fxn, intervalos):
        I = sp.N((b-a)*((fx0+2*suma_intermedios+4*suma_subint+fxn)/(6*intervalos)))
        return I
    
class Simpson_38():
    @staticmethod
    def simpson_simple(a, b, fx0, fx1, fx2, fx3):
        I = sp.N((b-a)*((fx0+3*fx1+3*fx2+fx3)/8))
        return I
    
    @staticmethod
    def simpson_compuesto(a, b, fx0, suma_subint, suma_intermedios, fxn, intervalos):
        I = sp.N(((b-a)/(8*intervalos))*(fx0+(3*suma_subint)+(2*suma_intermedios)+fxn))
        return I

#cuadratura de gauss
gauss_legendre_data = {
        2: {
            'argumento_funcion': [-0.5773502692, 0.5773502692],
            'factor_ponderacion': [1.0, 1.0]
        },
        3: {
            'argumento_funcion': [-0.7745966692, 0.0, 0.7745966692],
            'factor_ponderacion': [0.5555555556, 0.8888888889, 0.5555555556]
        },
        4: {
            'argumento_funcion': [-0.8611363116, -0.3399810436, 0.3399810436, 0.8611363116],
            'factor_ponderacion': [0.3478548451, 0.6521451549, 0.6521451549, 0.3478548451]
        },
        5: {
            'argumento_funcion': [-0.9061798459, -0.5384693101, 0.0, 0.5384693101, 0.9061798459],
            'factor_ponderacion': [0.2369268850, 0.4786286705, 0.5688888889, 0.4786286705, 0.2369268850]
        },
        6: {
            'argumento_funcion': [-0.932469514, -0.661209386, -0.238619186, 0.238619186, 0.661209386, 0.932469514],
            'factor_ponderacion': [0.1713245, 0.3607616, 0.4679139, 0.4679139, 0.3607616, 0.1713245]
        },
        # Puedes añadir más órdenes aquí    
        }


class cuadratura_gaussiana_formula():

    @staticmethod
    def cuadratura_gaussiana(j, limite_a, limite_b, funcion, variable, puntos):
        data = gauss_legendre_data.get(puntos)
        I = sp.N(data['factor_ponderacion'][j] * funcion.subs(variable,( ((limite_b-limite_a)*data['argumento_funcion'][j] + (limite_b-limite_a))/ 2)))
        return I


class metodod_boyle():
    @staticmethod
    def boyle(h, x0, x1, x2, x3, x4):
        return sp.N(((2*h)/45)*(7*x0+32*x1+12*x2+32*x3+7*x4))
