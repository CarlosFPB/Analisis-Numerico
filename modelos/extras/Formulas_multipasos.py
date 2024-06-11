import sympy as sp

class runge_kutta():


    @staticmethod
    def orden_2(x0, y0, h, y_prima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        k1 = y_prima.subs({x: x0, y: y0})
        k2 = y_prima.subs({x: x0 + h, y: y0 + h * k1})
        yi_siguiente = y0 + (1/2)*h*(k1 + k2)
        k1, k2, yi_siguiente = sp.N(k1), sp.N(k2), sp.N(yi_siguiente)
        return {'k1': k1, 'k2': k2, 'yi_siguiente': yi_siguiente}
    
    @staticmethod
    def orden_3(x0, y0, h, y_prima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        k1 = y_prima.subs({x: x0, y: y0})
        k2 = y_prima.subs({x: x0 + h/2, y: y0 + (h/2) * k1})
        k3 = y_prima.subs({x: x0 + h, y: y0 - h*k1 + 2*h*k2})
        yi_siguiente = y0 + (1/6)*h*(k1 + 4*k2 + k3)
        k1, k2, k3, yi_siguiente = sp.N(k1), sp.N(k2), sp.N(k3), sp.N(yi_siguiente)
        return {'k1': k1, 'k2': k2, 'k3': k3, 'yi_siguiente': yi_siguiente}

    @staticmethod
    def orden_4(x0,y0,h,yprima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        k1 = yprima.subs({x: x0, y: y0})
        k2 = yprima.subs({x: x0 + h/2, y: y0 + h/2*k1})
        k3 = yprima.subs({x: x0 + h/2, y: y0 + h/2*k2})
        k4 = yprima.subs({x: x0 + h, y: y0 + h*k3})
        yi_siguiente = y0 + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
        k1, k2, k3, k4, yi_siguiente = sp.N(k1), sp.N(k2), sp.N(k3), sp.N(k4), sp.N(yi_siguiente)
        return {'k1': k1, 'k2': k2, 'k3': k3, 'k4': k4, 'yi_siguiente': yi_siguiente}
    

class adams_bashfort():

    @staticmethod
    def orden_2(lista_x, lista_y, h, yprima):#encuentra y2
        x = sp.symbols('x')
        y = sp.symbols('y')
        x0 = lista_x[0]
        x1 = lista_x[1]
        y0 = lista_y[0]
        y1 = lista_y[1]
        y2 = y1 + (h/2)*(3*yprima.subs({x: x1 , y: y1}) - yprima.subs({x: x0, y: y0}))
        lista_x.append(x1 + h)
        lista_y.append(y2)
        return lista_x, lista_y, y2
    
    @staticmethod
    def orden_4(lista_x, lista_y, h, yprima):#encuentra y4
        x = sp.symbols('x')
        y = sp.symbols('y')
        x0 = lista_x[0]
        x1 = lista_x[1]
        x2 = lista_x[2]
        x3 = lista_x[3]
        y0 = lista_y[0]
        y1 = lista_y[1]
        y2 = lista_y[2]
        y3 = lista_y[3]
        y4 = y3 + (h/24)*(55*yprima.subs({x: x3, y: y3}) - 59*yprima.subs({x: x2, y: y2}) + 37*yprima.subs({x: x1, y: y1}) - 9*yprima.subs({x: x0, y: y0}))
        lista_x.append(x3 + h)
        lista_y.append(y4)
        return lista_x, lista_y, y4
    
class adams_moulton():

    @staticmethod
    def orden_1(lista_x, lista_y, h, yprima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        x1 = lista_x[1]
        y1 = lista_y[1]
        x2 = lista_x[2]
        y2 = lista_y[2]
        y2 = y1 + (h/2)*(yprima.subs({x: x2, y: y2}) + yprima.subs({x: x1, y: y1}))
        lista_y[-1] = y2
        return lista_x, lista_y, y2
    
    @staticmethod
    def orden_3(lista_x, lista_y, h, yprima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        x1 = lista_x[1]
        y1 = lista_y[1]
        x2 = lista_x[2]
        y2 = lista_y[2]
        x3 = lista_x[3]
        y3 = lista_y[3]
        x4 = lista_x[4]
        y4 = lista_y[4]
        y4 = y3 + (h/24)*(9*yprima.subs({x: x4, y: y4}) + 19*yprima.subs({x: x3, y: y3}) -5*yprima.subs({x: x2, y: y2}) + yprima.subs({x: x1, y: y1}))
        lista_y[-1] = y4
        return lista_x, lista_y, y4

        