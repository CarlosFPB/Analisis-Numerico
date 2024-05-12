from flask import Flask, render_template, request, jsonify, redirect
import os

# Importaciones de métodos
from modelos.metodos.iterativos.cerrados.biseccion.Biseccion import medoto_biseccion
from modelos.metodos.directos.polinomicas_mayor_3.ferrari.Ferrari import metodo_ferrari
from  modelos.metodos.directos.polinomicas_mayor_3.tartaglia.Tartaglia import metodo_tartaglia
from modelos.metodos.directos.polinomicas_menor_2.cuadratica.Cuadratica import metodo_cuadratico
from modelos.metodos.directos.polinomicas_menor_2.lineal.Lineal import metodo_lineal
from modelos.metodos.iterativos.abiertos.punto_fijo.Punto_fijo import metodo_punto_fijo
from modelos.metodos.iterativos.abiertos.newton.Newton import metodo_newton
from modelos.metodos.iterativos.abiertos.newton_modificado.Newton_modificado import metodo_newton_modificado
from modelos.metodos.iterativos.abiertos.secante.Secante import metodo_secante
from modelos.metodos.iterativos.polinomicos.horner.Horner import metodo_horner
from modelos.metodos.iterativos.polinomicos.muller.Muller import metodo_muller

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    # Redirige automáticamente a la URL de la imagen del gato
    return redirect("https://http.cat/404", code=302)

@app.errorhandler(504)
def page_not_found(e):
    #informar que el servidor no responde
    resp = {'error' :  "El servidor no responde"}
    return jsonify(resp), 504

@app.route('/metodos/iterativos/cerrados/Biseccion', methods=['GET'])
def renderizar_biseccion():
    return render_template('Biseccion.html')

@app.route('/metodos/iterativos/cerrados/Biseccion', methods=['POST'])
def calcular_biseccion():
    json_data = request.json
    respuesta = medoto_biseccion.calcular_biseccion(json_data)
    return respuesta

@app.route('/metodos/directos/gradomas3/Ferrari', methods=['GET'])
def renderizar_ferrari():
    return render_template('Ferrari.html')

@app.route('/metodos/directos/gradomas3/Ferrari', methods=['POST'])
def calcular_ferrari():
    json_data = request.json
    respuesta = metodo_ferrari.calcular_ferrari(json_data)
    return respuesta

@app.route('/metodos/directos/gradomas3/Tartaglia', methods=['GET'])
def renderizar_tartaglia():
    return render_template('Tartaglia.html')

@app.route('/metodos/directos/gradomas3/Tartaglia', methods=['POST'])
def calcular_tartaglia():
    json_data = request.json
    respuesta = metodo_tartaglia.calcular_tartaglia(json_data)
    return respuesta

@app.route('/metodos/directos/gradomenos2/cuartica', methods=['GET'])
def renderizar_cuartica():
    return render_template('Cuadratica.html')

@app.route('/metodos/directos/gradomenos2/cuartica', methods=['POST'])
def calcular_cuartica():
    json_data = request.json
    respuesta = metodo_cuadratico.calcular_cuadratico(json_data)
    return respuesta

@app.route('/metodos/directos/gradomenos2/lineal', methods=['GET'])
def renderizar_lineal():
    return render_template('Lineal.html')

@app.route('/metodos/directos/gradomenos2/lineal', methods=['POST'])
def calcular_lineal():
    json_data = request.json
    respuesta = metodo_lineal.calcular_lineal(json_data)
    return respuesta

@app.route('/metodos/directos/abiertos/punto-Fijo', methods=['GET'])
def Punto_fijo():
    return render_template('Punto_fijo.html')

@app.route('/metodos/directos/abiertos/punto-Fijo', methods=['POST'])
def calcular_punto_fijo():
    json_data = request.json
    respuesta = metodo_punto_fijo.calcular_punto_fijo(json_data)
    return respuesta    

@app.route('/metodos/directos/abiertos/newton', methods=['GET'])
def Newton():
    return render_template('Newton.html')

@app.route('/metodos/directos/abiertos/newton', methods=['POST'])
def calcular_newton():
    json_data = request.json
    respuesta = metodo_newton.calcular_newton(json_data)
    return respuesta

@app.route('/metodos/directos/abiertos/Newton-Modificado', methods=['GET'])
def Newton_Modificado():
    return render_template('Newton_modificado.html')

@app.route('/metodos/directos/abiertos/Newton-Modificado', methods=['POST'])
def calcular_newton_modificado():
    json_data = request.json
    respuesta = metodo_newton_modificado.calcular_newton_modificado(json_data)
    return respuesta

@app.route('/metodos/directos/abiertos/Secante', methods=['GET'])
def Secante():
    return render_template('Secante.html')

@app.route('/metodos/directos/abiertos/Secante', methods=['POST'])
def calcular_secante():
    json_data = request.json
    respuesta = metodo_secante.calcular_secante(json_data)
    return respuesta

@app.route('/metodos/iterativos/polinomicos/horner', methods=['POST'])
def calcular_horner():
    json_data = request.json
    respuesta = metodo_horner.calcular_Horner(json_data)
    return respuesta

@app.route('/metodos/iterativos/polinomicos/horner', methods=['GET'])
def Horner():
    return render_template('Horner.html')

@app.route('/metodos/iterativos/polinomicos/muller', methods=['POST'])
def calcular_muller():
    json_data = request.json
    respuesta = metodo_muller.calcular_Muller(json_data)
    return respuesta

@app.route('/metodos/iterativos/polinomicos/muller', methods=['GET'])
def Muller():
    return render_template('Muller.html')


        
 

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
