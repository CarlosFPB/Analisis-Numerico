import sympy as sp

class finita_hacia_delante():

    @staticmethod
    def primera_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b = xi+h, xi
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        respuesta = (a-b)/h
        return respuesta
    
    @staticmethod
    def primera_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c = xi+2*h, xi+h, xi
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        respuesta = (-3*c+4*b-a)/(2*h)
        return respuesta
    
    @staticmethod
    def segunda_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c = xi+2*h, xi+h, xi
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        respuesta = (a-2*b+c)/(h**2)
        return respuesta
    
    @staticmethod
    def segunda_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d = xi+3*h, xi+2*h, xi+h, xi
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        respuesta = (-a+4*b-5*c+2*d)/(h**2)
        return respuesta
    
    @staticmethod
    def tercer_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d = xi+3*h, xi+2*h, xi+h, xi
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        respuesta = (a-3*b+3*c-d)/(h**3)
        return respuesta
    
    @staticmethod
    def tercer_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e = xi+4*h, xi+3*h, xi+2*h, xi+h, xi
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        respuesta = (-3*a+14*b-24*c+18*d-5*e)/(2*h**3)
        return respuesta

    @staticmethod
    def cuarta_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e = xi+4*h, xi+3*h, xi+2*h, xi+h, xi
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        respuesta = (a-4*b+6*c-4*d+e)/(h**4)
        return respuesta

    @staticmethod
    def cuarta_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e, f = xi+5*h, xi+4*h, xi+3*h, xi+2*h, xi+h, xi
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        f = f_x.subs(x,f)
        respuesta = (-2*a+11*b-24*c+26*d-14*e+3*f)/(h**4)
        return respuesta
    
class finita_hacia_atras():
    
    @staticmethod
    def primera_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b = xi, xi-h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        respuesta = (a-b)/h
        return respuesta

    @staticmethod
    def primera_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c = xi, xi-h, xi-2*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        respuesta = (3*a-4*b+c)/(2*h)
        return respuesta
    
    @staticmethod
    def segunda_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c = xi, xi-h, xi-2*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        respuesta = (a-2*b+c)/(h**2)
        return respuesta
    
    @staticmethod
    def segunda_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d = xi, xi-h, xi-2*h, xi-3*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        respuesta = (2*a-5*b+4*c-d)/(h**2)
        return respuesta
    
    @staticmethod
    def tercer_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d = xi, xi-h, xi-2*h, xi-3*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        respuesta = (a-3*b+3*c-d)/(h**3)
        return respuesta
    
    @staticmethod
    def tercer_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e = xi, xi-h, xi-2*h, xi-3*h, xi-4*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        respuesta = (5*a-18*b+24*c-14*d+3*e)/(2*h**3)
        return respuesta

    @staticmethod
    def cuarta_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e = xi, xi-h, xi-2*h, xi-3*h, xi-4*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        respuesta = (a-4*b+6*c-4*d+e)/(h**4)
        return respuesta
    
    @staticmethod
    def cuarta_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e, f = xi, xi-h, xi-2*h, xi-3*h, xi-4*h, xi-5*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        f = f_x.subs(x,f)
        respuesta = (3*a-14*b+26*c-24*d+11*e-2*f)/(h**4)
        return respuesta
    

class finita_central():

    @staticmethod
    def primera_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b = xi+h, xi-h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        respuesta = (a-b)/(2*h)
        return respuesta
    
    @staticmethod
    def primera_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d = xi+2*h, xi+h, xi-h, xi-2*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        respuesta = (-a+8*b-8*c+d)/(12*h)
        return respuesta
    
    @staticmethod
    def segunda_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c = xi+h, xi, xi-h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        respuesta = (a-2*b+c)/(h**2)
        return respuesta
    
    @staticmethod
    def segunda_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e = xi+2*h, xi+h, xi, xi-h, xi-2*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        respuesta = (-a+16*b-30*c+16*d-e)/(12*h**2) 
        return respuesta
    
    @staticmethod
    def tercer_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d = xi+2*h, xi+h, xi-h, xi-2*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        respuesta = (a-2*b+2*c-d)/(2*h**3)
        return respuesta
    
    @staticmethod
    def tercer_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e, f = xi+3*h, xi+2*h, xi+h, xi-h, xi-2*h, xi-3*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        f = f_x.subs(x,f)
        respuesta = (-a+8*b-13*c+13*d-8*e+f)/(8*h**3)
        return respuesta
    
    @staticmethod
    def cuarta_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d,e = xi+2*h, xi+h, xi,xi-h, xi-2*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        respuesta = (a-4*b+6*c-4*d+e)/(h**4)
        return respuesta
    
    @staticmethod
    def cuarta_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e, f, g = xi+3*h, xi+2*h, xi+h, xi, xi-h, xi-2*h, xi-3*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        f = f_x.subs(x,f)
        g = f_x.subs(x,g)
        respuesta = (-a+12*b+39*c+56*d-39*e+12*f+g)/(6*h**4)
        return respuesta
    
class finita_tres_puntos():

    @staticmethod
    def primera_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c = xi+h, xi, xi-h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        respuesta = (a-c)/(2*h)
        return respuesta
    
    @staticmethod
    def primera_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c = xi, xi + h, xi +2*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        respuesta = (-3*a+4*b-c)/(2*h)
        return respuesta
    
class finita_cinco_puntos():

    @staticmethod
    def primera_derivada_v1(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e = xi, xi + h, xi + 2*h, xi +3*h, xi + 4*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        respuesta = (-25*a+48*b-36*c+16*d-3*e)/(12*h)
        return respuesta
    
    @staticmethod
    def primera_derivada_v2(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e = xi-h, xi, xi + h, xi + 2*h, xi +3*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        respuesta = (-3*a-10*b+18*c-6*d+e)/(12*h)
        return respuesta
    
    @staticmethod
    def primera_derivada_v3(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d = xi -2*h, xi - h, xi + h, xi + 2*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        respuesta = (a-8*b+8*c-d)/(12*h)
        return respuesta
    
    @staticmethod
    def primera_derivada_v4(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e, f = xi -3*h, xi +2*h, xi - h, xi, xi+ h, xi + 2*h
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        f = f_x.subs(x,f)
        respuesta = (4*a+6*b-8*c+34*d+3*e+34*f)/(12*h)
        return respuesta
    
    @staticmethod
    def primera_derivada_v5(f_x,xi,h):
        x = sp.symbols('x')
        a, b, c, d, e = xi -4*h, xi -3*h, xi - 2*h, xi - h, xi
        a = f_x.subs(x,a)
        b = f_x.subs(x,b)
        c = f_x.subs(x,c)
        d = f_x.subs(x,d)
        e = f_x.subs(x,e)
        respuesta = (a-3*b+4*c-36*d+25*e)/(12*h)
        return respuesta
    

class Diferenciacion:
    """Clase principal que encapsula todas las clases de derivadas."""
    
    def __init__(self):
        self.finita_hacia_delante = finita_hacia_delante
        self.finita_hacia_atras = finita_hacia_atras
        self.finita_central = finita_central
        self.finita_tres_puntos = finita_tres_puntos
        self.finita_cinco_puntos = finita_cinco_puntos
        
