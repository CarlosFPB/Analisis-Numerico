import sympy as sp

class euler():

    @staticmethod
    def euler_mejorado(xi,yi,h,yprima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        Y_ray = yi+h* yprima.subs({x: xi, y: yi})
        a = yprima.subs({x: xi, y: yi})
        b = yprima.subs({x: xi + h, y: Y_ray})
        yi_siguiente = yi + (h/2)*(a + b)
        yi_siguiente = sp.N(yi_siguiente)
        return yi_siguiente
    
    @staticmethod
    def euler_hacia_atras(xi,yi,h,yprima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        y_ray = yi + h*yprima.subs({x: xi, y: yi})
        xi_siguiente = round(xi + h,10)
        yi_siguiente = yi + h*yprima.subs({x: xi_siguiente, y: y_ray})
        yi_siguiente = sp.N(yi_siguiente)
        return yi_siguiente
    
    #falta confirmar formula
    @staticmethod
    def euler_hacia_adelante(xi,yi,h,yprima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        yi_siguiente = yi + h*yprima.subs({x: xi, y: yi})
        yi_siguiente = sp.N(yi_siguiente)
        return yi_siguiente

    @staticmethod
    def euler_centrada(xi,yi,h,yprima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        yi_siguiente = yi + h*yprima.subs({x: xi, y: yi})
        yi_siguiente = sp.N(yi_siguiente)
        return yi_siguiente
