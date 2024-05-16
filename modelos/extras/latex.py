from sympy import expand
from latex2sympy2 import latex2sympy, latex2latex




 
class conversla():
    @staticmethod
    def latex_(latex):        
        latex2sympy(latex)
        latex2latex(latex)
        return expand(latex2sympy(latex))




