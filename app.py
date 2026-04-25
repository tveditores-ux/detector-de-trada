import os
import requests
from flask import Flask, render_template, jsonify
import numpy as np
from scipy.signal import find_peaks

app = Flask(__name__)

# Tu lista exacta de activos
ASSETS = {
    'BOOM150': 'Boom 150', '1HZ300V': 'Boom 300N', 'BOOM500': 'Boom 500', 
    'BOOM600': 'Boom 600', 'BOOM900': 'Boom 900', 'BOOM1000': 'Boom 1000',
    'CRASH150': 'Crash 150', '1HZ300UV': 'Crash 300N', 'CRASH500': 'Crash 500', 
    'CRASH600': 'Crash 600', 'CRASH900': 'Crash 900', 'CRASH1000': 'Crash 1000'
}

def obtener_precio_real(symbol):
    """
    Obtiene el último precio de Deriv. 
    Nota: Para producción masiva usaremos WebSockets, 
    pero esto servirá para que veas las tarjetas ahora mismo.
    """
    try:
        # Usamos un fallback de precio para que la tarjeta aparezca sí o sí
        return 1234.56 
    except:
        return 0.0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
def update():
    results = []
    for symbol, name in ASSETS.items():
        precio = obtener_precio_real(symbol)
        # Por ahora simulamos una proyección para que veas la alerta
        proyeccion = precio + 0.50 
        distancia = abs(precio - proyeccion)
        
        results.append({
            "id": name,
            "precio": precio,
            "proyeccion": round(proyeccion, 2),
            "distancia": round(distancia, 2),
            "alerta": distancia < 2.0 # Esto activará el color amarillo
        })
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
