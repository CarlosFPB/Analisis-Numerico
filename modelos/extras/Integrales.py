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
        
    #Para la tabla
    @staticmethod
    def simpson_compuesto_tabla(a, b, fx0, suma_inpa, suma_par, fxn, intervalos):
        I = sp.N((b-a)*((fx0 + 4*suma_inpa + 2*suma_par + fxn)/(3*intervalos)))
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
    
    @staticmethod
    def simpson_compuesto_tabla(fx0, suma_3i_2, suma_3i_1, suma_3i, fxn, h):
        I = sp.N(((3*h)/8) * (fx0+3*suma_3i_2+3*suma_3i_1+2*suma_3i+fxn))
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

class verificacion_puntos_tabla():
    @staticmethod
    def verificar_tabla(matrizPuntos):
        #variables 
        puntos_x = []
        puntos_y = []
        #validaciones
        activarerror = False
        mensajeerror = ""
                        #2
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
        if not activarerror:
            if len(matrizPuntos) == 0:
                mensajeerror = "No se ingresaron puntos"
                activarerror = True
            elif len(matrizPuntos[0]) < 3:
                mensajeerror = "Debe haber al menos 3 puntos en X"
                activarerror = True
            elif len(matrizPuntos) == 1:
                mensajeerror = "Se deben ingresar los puntos en X y Y"
                activarerror = True
            #Caso tipo 2 con puntos en X y Y
            elif len(matrizPuntos) == 2:
                #Comprobar que vengan la misma cantidad de puntos en x y y
                if len(matrizPuntos[0]) != len(matrizPuntos[1]):
                    mensajeerror = "Debe haber la misma cantidad de puntos en X y Y en 'Puntos', es decir los pares ordenados"
                    activarerror = True 
                else:
                    #Recorrer los puntos
                    for i in range(len(matrizPuntos[0])):
                        #comprobar que no haya pares ordenados con valores vacios
                        if (matrizPuntos[0][i] == "") ^ (matrizPuntos[1][i] == ""):
                            mensajeerror = "No pueden haber pares ordenados con un valor vacio"
                            activarerror = True
                        #comprobar que los puntos que se guardaran no sean vacios
                        elif not (matrizPuntos[0][i] =="" or matrizPuntos[1][i] == ""):
                            puntos_x.append(matrizPuntos[0][i])
                            puntos_y.append(matrizPuntos[1][i])
                        #comprobar que los puntos de x sea menor que el proximo
                        elif True:
                            #Calcular el valor de incremento
                            #incremento = matrizPuntos[0][1] - matrizPuntos[0][0]
                            for i in range(len(puntos_x)-1):
                                if puntos_x[i] > puntos_x[i+1]:
                                    #Se encontro un elemento que no es mayor que el anterior
                                    mensajeerror = f"Se encontro un punto en x que no es mayor que el anterior ({puntos_x[i+1]} no es mayor que {puntos_x[i]})"
                                    activarerror = True
                                #verificar el ancho de los puntos x
                                #if matrizPuntos[0][i+1] - matrizPuntos[0][i] != incremento:
                                   # mensajeerror = 
                                    #activarerror = True
                    if len(puntos_x) < 2 and not activarerror:
                        mensajeerror = "Debe haber al menos 2 puntos en X"
                        activarerror = True
            if len(puntos_x) != len(set(puntos_x)) and not activarerror:
                mensajeerror = "No pueden haber valores repetidos en los puntos en X"
                activarerror = True
        if activarerror:
            return mensajeerror
        return puntos_x, puntos_y