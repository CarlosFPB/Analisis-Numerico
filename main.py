from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metodos/directos/cerrados/Biseccion', methods=['GET'])
def biseccion():
    return render_template('Biseccion.html')

@app.route('/metodos/directos/cerrados/Biseccion', methods=['POST'])
def prueba():
    print(request.json)
    return jsonify({'result': 'success', 'data': 'Hola Mundo'})

if __name__ == '__main__':
    app.run()