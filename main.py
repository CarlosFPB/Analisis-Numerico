from flask import Flask, render_template, request, jsonify

#importaciones de metodos
from modelos.Metodos.Directos.Cerrados.Biseccion.biseccion import medoto_biseccion

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

if __name__ == '__main__':
    app.run()