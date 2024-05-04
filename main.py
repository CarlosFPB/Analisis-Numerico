from flask import Flask, render_template, request, jsonify
import os

# Importaciones de métodos
from modelos.metodos.iterativos.cerrados.biseccion.Biseccion import medoto_biseccion
from modelos.metodos.directos.polinomicas_mayor_3.ferrari.Ferrari import metodo_ferrari
from  modelos.metodos.directos.polinomicas_mayor_3.tartaglia.Tartaglia import metodo_tartaglia

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
