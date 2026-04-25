import os
from flask import Flask, render_template, jsonify
import numpy as np
from scipy.signal import find_peaks

app = Flask(__name__)

# Lista de activos solicitada
assets = [
    'BOOM150', '1HZ300V', 'BOOM500', 'BOOM600', 'BOOM900', 'BOOM1000',
    'CRASH150', '1HZ300UV', 'CRASH500', 'CRASH600', 'CRASH900', 'CRASH1000'
]

def calcular_triada(precios, tipo):
    if len(precios) < 20: return None
    data = np.array(precios)
    # Detectamos picos: valles para Boom, crestas para Crash
    indices, _ = find_peaks(-data if 'BOOM' in tipo or '300V' in tipo and 'U' not in tipo else data, 
                            distance=10, prominence=0.5)
    
    if len(indices) < 2: return None
    
    p1, p2 = indices[-2], indices[-1]
    v1, v2 = data[p1], data[p2]
    
    # Ecuación de la recta: y = mx + b
    m = (v2 - v1) / (p2 - p1)
    b = v1 - (m * p1)
    proyeccion = (m * len(data)) + b
    return round(float(proyeccion), 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
def update():
    # NOTA: En producción, aquí conectarías con la API de Deriv para obtener precios reales
    results = []
    for asset in assets:
        tipo = 'boom' if 'BOOM' in asset or '300V' in asset and 'U' not in asset else 'crash'
        precio_actual = 1000.00 # Simulado
        proy = 1001.50 # Simulado
        distancia = abs(precio_actual - proy)
        
        results.append({
            "id": asset,
            "precio": precio_actual,
            "proyeccion": proy,
            "distancia": round(distancia, 2),
            "alerta": distancia < 3.0 # Umbral de cercanía
        })
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
