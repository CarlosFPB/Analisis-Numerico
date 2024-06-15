from sympy import expand, printing
from latex2sympy2 import latex2sympy

class conversla(): #soluciona bug de variables
    @staticmethod
    def latex_(latex):   
        importlib.reload(importlib.import_module('latex2sympy2'))
        return expand(latex2sympy(latex))

class conversla_html():
    @staticmethod
    def mathl_(expr):
        mathml_code = printing.mathml(expr, printer='presentation')
        mathml_code = f'<math xmlns="http://www.w3.org/1998/Math/MathML">{mathml_code}</math>'
        return mathml_code


