from flask import Flask, render_template, request, jsonify

#importaciones de metodos
from modelos.metodos.iterativos.cerrados.biseccion.Biseccion import medoto_biseccion
from modelos.metodos.iterativos.abiertos.newton.Newton import metodo_newton
from modelos.metodos.iterativos.abiertos.newton_modificado.Newton_modificado import metodo_newton_modificado
from modelos.metodos.iterativos.abiertos.punto_fijo.Punto_fijo import punto_fijo
from modelos.metodos.iterativos.abiertos.secante.Secante import metodo_secante

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metodos/directos/cerrados/Biseccion', methods=['GET'])
def renderizar_biseccion():
    return render_template('Biseccion.html')

@app.route('/metodos/directos/cerrados/Biseccion', methods=['POST'])
def calcular_biseccion():
    json_data = request.json
    respuesta = medoto_biseccion.calcular_biseccion(json_data)
    return respuesta

@app.route('/metodos/directos/abiertos/Newton', methods=['GET'])
def renderizar_Newton():
    return render_template('Newton.html')

@app.route('/metodos/directos/abiertos/Newton', methods=['POST'])
def calcular_Newton():
    json_data = request.json
    respuesta = metodo_newton().calcular_newton(json_data)
    return respuesta

@app.route('/metodos/directos/abiertos/Newton-Modificado', methods=['GET'])
def renderizar_Newton_Modificado():
    return render_template('Newton_modificado.html')

@app.route('/metodos/directos/abiertos/Newton-Modificado', methods=['POST'])
def calcular_Newton_Modificado():
    json_data = request.json
    respuesta = metodo_newton_modificado().calcular_newton_modificado(json_data)
    return respuesta

@app.route('/metodos/directos/abiertos/Punto-Fijo', methods=['GET'])
def renderizar_Punto_Fijo():
    return render_template('Punto_fijo.html')

@app.route('/metodos/directos/abiertos/Punto-Fijo', methods=['POST'])
def calcular_Punto_Fijo():
    json_data = request.json
    respuesta = punto_fijo().calcular_punto_fijo(json_data)
    return respuesta

@app.route('/metodos/directos/abiertos/Secante', methods=['GET'])
def renderizar_secante():
    return render_template('Secante.html')

@app.route('/metodos/directos/abiertos/Secante', methods=['POST'])
def calcular_secante():
    json_data = request.json
    respuesta = metodo_secante().calcular_secante(json_data)
    return respuesta


if __name__ == '__main__':
    app.run()