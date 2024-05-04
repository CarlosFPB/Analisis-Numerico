import sympy as sp
import math
from modelos.extras.Funciones import errores, biseccion, respuesta_json

class metodo_tartaglia:
    
    def calcular_tartaglia(json_data):
        x1 = 0
        x2 = 0
        x3 = 0
        #istanciar la respuesta
        respuesta = respuesta_json()

        x = sp.symbols('x')
        #obtener los valores del json
        f_x_crudo = sp.simplify(json_data["funcion"])
        f_x = f_x_crudo/f_x_crudo.as_poly(x).coeffs()[0]

        #encontrar los coeficientes inlcuido los coeficientes 0
        polinomio = f_x.as_poly(x)
        grado = polinomio.degree()
        coeficientes = [polinomio.coeff_monomial(x**i) for i in range(grado, -1, -1)]#aunq haya 0
        a = coeficientes[1]
        b = coeficientes[2]
        c = coeficientes[3]

        #calculamos p y q
        p = (3*b-a**2)/3
        q = (2*a**3 - 9*a*b + 27*c)/27

        #discriminante
        delta = (q/2)**2 + (p/3)**3

        #obtener las raices
        if delta == 0:
            if p==0 and q==0:
                #tiene raiz triple
                x1 = x2 = x3 = (-a/3)
            if p*q != 0:
                x1 = x2 = (-(3*q)/(2*p)) - (a/3) #raiz doble
                x3 = ((-4*p**2)/(9*q)) - (a/3)

        elif delta > 0:
            #calculamos u y v
            u = math.cbrt(-q/2 + sp.sqrt(delta))
            v = math.cbrt(-q/2 - sp.sqrt(delta))
            #obtenemos las raices
            x1 = u + v - (a/3) #raiz real
            x2 = -(u+v)/2 - (a/3) + (u-v)*sp.sqrt(3)/2 #raices imaginarias
            x3 = -(u+v)/2 - (a/3) - (u-v)*sp.sqrt(3)/2

        elif delta < 0:
            #calculamos angulo
            k = 0
            angulo = sp.acos((-q/2)/sp.sqrt(-(p/3)**3))
            x1 = (2*sp.sqrt(-p/3))*sp.cos((angulo+2*k*sp.pi)/3) - (a/3)
            k = 1
            x2 = (2*sp.sqrt(-p/3))*sp.cos((angulo+2*k*sp.pi)/3) - (a/3)
            k = 2
            x3 = (2*sp.sqrt(-p/3))*sp.cos((angulo+2*k*sp.pi)/3) - (a/3)


        respuesta.agregar_titulo1("Método de Tartaglia")
        respuesta.agregar_titulo1("Resultados")
        respuesta.agregar_fila(["Raíz 1", x1])
        # imprimir las raices con leyenda
        print("Las raíces son:")
        print("x1 =", x1)
        print("x2 =", x2)
        print("x3 =", x3)
        return respuesta.obtener_y_limpiar_respuesta()

