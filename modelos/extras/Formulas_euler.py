import sympy as sp

class euler():

    @staticmethod
    def euler_mejorado(xi,yi,h,yprima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        a = yprima.subs({x: xi, y: yi})
        b = yprima.subs({x: xi + h, y: yi + h*a})
        yi_siguiente = yi + (h/2)*(a + b)
        return yi_siguiente
    
    @staticmethod
    def euler_hacia_atras(xi,yi,h,yprima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        y_ray = yi + h*yprima.subs({x: xi, y: yi})
        xi_siguiente = xi + h
        yi_siguiente = yi + h*yprima.subs({x: xi_siguiente, y: y_ray})
        yi_siguiente = sp.N(yi_siguiente)
        return yi_siguiente
    
    #falta confirmar formula
    @staticmethod
    def euler_hacia_adelante(xi,yi,h,yprima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        yi_siguiente = yi + h*yprima.subs({x: xi, y: yi})
        return yi_siguiente

    @staticmethod
    def euler_centrada(xi,yi,h,yprima):
        x = sp.symbols('x')
        y = sp.symbols('y')
        yi_siguiente = yi + h*yprima.subs({x: xi, y: yi})
        return yi_siguiente
