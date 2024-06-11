from flask import Flask, render_template, request, jsonify, redirect
import os
import time

from modelos.rutas.rutaU2 import U2
from modelos.rutas.rutaU3 import U3
from modelos.rutas.rutaU4 import U4
from modelos.rutas.rutaU5 import U5

app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#registro los blueprints
app.register_blueprint(U2)
app.register_blueprint(U3)
app.register_blueprint(U4)
app.register_blueprint(U5)

#raiz y errores
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
    resp = {'error' :  'El servidor no responde'}
    return jsonify(resp), 504

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
