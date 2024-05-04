import sympy as sp
import math
from modelos.extras.Funciones import errores, respuesta_json

class metodo_ferrari:
        
    def calcular_ferrari(json_data):
        x = sp.symbols('x')
        #obtener los valores del json
        f_x_crudo = sp.simplify(json_data["funcion"])
        f_x = f_x_crudo/f_x_crudo.as_poly(x).coeffs()[0]#para convertir en 0 el coeficiente de x^4


        #obtiene los coeficientes de la funcion de forma descendente
        polinomio = f_x.as_poly(x)
        coefficientes = [polinomio.coeff_monomial(x**i) for i in range(grado, -1, -1)]
        a = coefficientes[1]
        b = coefficientes[2]
        c = coefficientes[3]
        d = coefficientes[4]

        #calcular p y q y r
        P = (8*b - 3*a**2)/8
        Q = (a**3 - 4*a*b + 8*c)/8
        R = (-3*a**4 + 256*d - 64*a*c + 16*a**2*b)/256

        #contruimos la cubica
        y = sp.symbols('y')
        cubica = sp.simplify(y**3 - (P/2)*y**2 - R*y + (4*P*R - Q**2)/8)


        #encontramos a b c de tartaglia
        #encontrar los coeficientes inlcuido los coeficientes 0
        polinomio = cubica.as_poly(y)
        grado = polinomio.degree()
        coeficientesTartaglia = [polinomio.coeff_monomial(y**i) for i in range(grado, -1, -1)]#aunq haya un coeficiente con 0
        aT = coeficientesTartaglia[1]
        bT = coeficientesTartaglia[2]
        cT = coeficientesTartaglia[3]

        #calculamos p y q de tartaglia y delta
        pT = (3*bT-aT**2)/3
        qT = (2*aT**3 - 9*aT*bT + 27*cT)/27
        deltaT = (qT/2)**2 + (pT/3)**3


        #obtener 1 raiz real
        if deltaT == 0:
            if pT==0 and qT==0:
                #tiene raiz triple
                xreal = (-aT/3)
            if pT*qT != 0:
                xreal = ((-4*pT**2)/(9*qT)) - (aT/3)

        elif deltaT > 0:
            #calculamos u y v
            u = math.cbrt(-qT/2 + sp.sqrt(deltaT))
            v = math.cbrt(-qT/2 - sp.sqrt(deltaT))
            #obtenemos las raices
            xreal = u + v - (aT/3) #raiz real

        elif deltaT < 0:
            #calculamos angulo
            k = 0
            angulo = sp.acos((-qT/2)/sp.sqrt(-(pT/3)**3))
            xreal = (2*sp.sqrt(-pT/3))*sp.cos((angulo+2*k*sp.pi)/3) - (aT/3)

        #reescribimos
        U = xreal.evalf()
        P = P
        Q = Q
        a = a

        #encontramos V
        VF = sp.sqrt(2 * U - P)
        W = -(Q/(2*VF))

        #encontramos las raices
        x1 = (VF + sp.sqrt(VF**2 -4*(U - W)))/2 - (a/4)
        x2 = (VF - sp.sqrt(VF**2 -4*(U - W)))/2 - (a/4)
        x3 = (-VF + sp.sqrt(VF**2 -4*(U + W)))/2 - (a/4)
        x4 = (-VF - sp.sqrt(VF**2 -4*(U + W)))/2 - (a/4)


        #Imprimir todas las variables
        print("Las raices son:")
        print("x1 =", x1)
        print("x2 =", x2)
        print("x3 =", x3)
        print("x4 =", x4)