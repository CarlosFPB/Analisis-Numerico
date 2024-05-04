from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Agregar importación

# Importaciones de métodos
from modelos.metodos.iterativos.cerrados.biseccion.Biseccion import medoto_biseccion

app = Flask(__name__, static_url_path='/static')
CORS(app)  # Habilitar CORS en la aplicación

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

if __name__ == '_main_':
    app.run()
