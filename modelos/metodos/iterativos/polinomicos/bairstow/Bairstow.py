import numpy as np
import sympy as sp
from .....extras.Funciones import errores, respuesta_json


class metodo_bairstow():
    def format(number):
        return str(float(number))

    #funcion encargada de realizar la divicion sintetica
    def calcular_divsion_sinterica(coeficientes, divisor):
        divicion_sintetica = []
        divicion_sintetica.append(coeficientes) #Agregamos los coeficientes originales
        divicion_sintetica.append([0]*len(coeficientes)) #Agregamos los coeficientes de la divicion
        divicion_sintetica.append([0]*len(coeficientes)) #Agregamos los coeficientes de la suma
        #incialmente estos dos ultimos todos son 0 para luego ser reemplazados
        for i in range(len(coeficientes)):
            termino = divicion_sintetica[0][i]
            coeficiente = divicion_sintetica[2][i-1] * divisor
            divicion_sintetica[1][i] = float(coeficiente)
            resultado = float(termino + coeficiente)
            divicion_sintetica[2][i] = resultado
            if i == len(coeficientes) - 1:
                #al finalizar todo el proceso retorna el arreglo (matris) con la division sintetica tal cual
                return divicion_sintetica
    def dibujar_division_sinterica(arreglo_division_sintetica, divisor):

        texto = ""
        for i in range(len(arreglo_division_sintetica[0])):
            texto += "{:^21}".format(float(arreglo_division_sintetica[0][i]))
        texto += "|"
        print(texto)
        texto = ""


        for i in range(len(arreglo_division_sintetica[1])):
            texto += "{:^21}".format(float(arreglo_division_sintetica[1][i]))
        texto += "|"
        texto += "{:^21}".format(float(divisor))
        print(texto)
        print("-" * (21 * len(arreglo_division_sintetica[0]) + 12))
        texto = ""


        for i in range(len(arreglo_division_sintetica[2])):
            texto += "{:^21}".format(float(arreglo_division_sintetica[2][i]))
        texto += "|"
        print(texto)



  

    def calcular_bairstow(json_data):
        x = sp.symbols("x")

        #obtengo los valores del json
        f_x = sp.sympify(json_data["funcion"])

        r0 = float(json_data["r0"])
        s0 = float(json_data["s0"])
        error_de_tolerancia = float(json_data["tolerancia"])

        raicez = []

        terminos_crudo = sp.Poly(f_x, x).all_terms()
        terminos = []
        for termino in terminos_crudo:
            terminos.append(termino[1])

        if terminos[0] != 1:
            f_x = f_x / terminos[0]
        print("f(x) normalizada:", f_x)


        iteracion = 1
        while True:
            print("\n\nIteracion:", iteracion)
            print("-" * 50)

            terminos_a = terminos
            print("Terminos a:")
            texto = ""
            for index, termino in enumerate(terminos_a):
                texto +="a" + str(len(terminos_a) - index - 1) + ": " + str(termino) + ", "
            print(texto)


            terminos_b = []
            terminos_b.append(terminos_a[0])
            terminos_b.append(terminos_a[1] + r0 * terminos_b[0])
            for i in range(2, len(terminos_a)):
                terminos_b.append(terminos_a[i] + r0 * terminos_b[i-1] + s0 * terminos_b[i-2])
            print("Terminos b:")
            texto = ""
            for index, termino in enumerate(terminos_b):
                texto +="b" + str(len(terminos_b) - index - 1) + ": " + str(termino) + ", "
            print(texto)


            terminos_c = []
            terminos_c.append(terminos_b[0])
            terminos_c.append(terminos_b[1] + r0 * terminos_c[0])
            for i in range(2, len(terminos_b)):
                terminos_c.append(terminos_b[i] + r0 * terminos_c[i-1] + s0 * terminos_c[i-2])
            print("Terminos c:")
            texto = ""
            for index, termino in enumerate(terminos_c):
                texto +="c" + str(len(terminos_c) - index - 1) + ": " + str(termino) + ", "
            print(texto,"\n")

            #Formar las ecuaciones
            a = np.array([
                [float(terminos_c[-3]), float(terminos_c[-4])],
                [float(terminos_c[-2]), float(terminos_c[-3])]
                ])
            b = np.array([-float(terminos_b[-2]), -float(terminos_b[-1])])
            resultado = np.linalg.solve(a, b)
            delta_r = resultado[0]
            delta_s = resultado[1]
            print("delta_r:", delta_r)
            print("delta_s:", delta_s)

            ri = r0 + delta_r
            si = s0 + delta_s
            print("ri:", ri)
            print("si:", si)

            Ear = abs(delta_r / ri) * 100
            Eas = abs(delta_s / si) * 100
            print("Error aproximado r:", Ear, "%")
            print("Error aproximado s:", Eas, "%")

            if not(Ear < error_de_tolerancia and Eas < error_de_tolerancia):
                r0 = ri
                s0 = si
                iteracion += 1
            else:
                print("\n\ncalcular la raiz")
                x1 = (ri + (ri*2 + 4*si)*0.5) / 2
                x2 = (ri - (ri*2 + 4*si)*0.5) / 2
                print("x1:", x1)
                print("x2:", x2)
                print("aproximacion de las raices a las cifras significativas dadas esto con el fin de que en la division sintetica no hayan residuos")

                try:
                    x1 = round(float(x1), cifras_sifnificativas)
                    print("x2:", x1)
                except:
                    x1 = round(float(x1 * -1**(1/2)), cifras_sifnificativas) *1j
                    print("x1:", x1)
                try:
                    x2 = round(float(x2), cifras_sifnificativas)
                    print("x2:", x2)
                except:
                    pass
                
                print("\n\nDivision sintetica con x1")
                division = calcular_divsion_sinterica(terminos, x1)
                dibujar_division_sinterica(division, x1)
                print("\n\nDivision sintetica con x2")
                division = calcular_divsion_sinterica(division[2][:-1], x2)
                dibujar_division_sinterica(division, x2)

                f_q = 0
                for indice, termino in enumerate(division[2][:-1]):
                    f_q += termino * x ** (len(division[2][:-2]) - indice)
                raicez.append(x1)
                raicez.append(x2)
                print("\nla nueva funcion g(x) queda:", f_q)
                
                if len(division[2][:-1]) > 3:
                    print("\n\n\nse repite el proceso con el polinomio cociente dado que el grado es igual o mayor a 3")
                    print("nuevo polinomio:", f_q)
                    f_x = f_q
                    r0 = ri
                    s0 = si
                    calcular_Bairtow(f_x, r0, s0, error_de_tolerancia, cifras_sifnificativas)
                elif len(division[2][:-1]) == 3:
                    print("\nse resuelve el polinomio de grado 2 con la formula general")
                    x3 = (-division[2][1] + (division[2][1]*2 - 4 * division[2][0] * division[2][2])*0.5) / (2 * division[2][0])
                    raicez.append(x2)
                    x4 = (-division[2][1] - (division[2][1]*2 - 4 * division[2][0] * division[2][2])*0.5) / (2 * division[2][0])
                    raicez.append(x4)
                elif len(division[2][:-1]) == 2:
                    print("\nse resuelve el polinomio de grado 1 simplemente despejando x")
                    x3 = -division[2][1] / division[2][0]
                    raicez.append(x3)
                break

