from flask import Flask, render_template, jsonify
import numpy as np
from scipy.signal import find_peaks

app = Flask(__name__)

# Configuración de activos
assets = [
    'BOOM150', '1HZ300V', 'BOOM500', 'BOOM600', 'BOOM900', 'BOOM1000',
    'CRASH150', '1HZ300UV', 'CRASH500', 'CRASH600', 'CRASH900', 'CRASH1000'
]

def detectar_triada(precios, tipo):
    data = np.array(precios)
    # Buscamos valles para Boom y crestas para Crash
    indices, _ = find_peaks(-data if tipo == 'boom' else data, distance=10, prominence=0.5)
    
    if len(indices) < 2: return None
    
    p1, p2 = indices[-2], indices[-1]
    v1, v2 = data[p1], data[p2]
    
    m = (v2 - v1) / (p2 - p1)
    b = v1 - (m * p1)
    # Proyección para la vela actual (índice len(data))
    proyeccion = (m * len(data)) + b
    return round(proyeccion, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
def update():
    # Aquí simularíamos la data de Deriv, en producción conectas con tu API
    results = []
    for asset in assets:
        tipo = 'boom' if 'BOOM' in asset or '300V' in asset and 'U' not in asset else 'crash'
        # Simulación de datos para el ejemplo
        precio_actual = 1200.00 
        proy = 1200.50 # Ejemplo de proyección calculada
        distancia = abs(precio_actual - proy)
        
        results.append({
            "id": asset,
            "precio": precio_actual,
            "proyeccion": proy,
            "distancia": round(distancia, 2),
            "alerta": distancia < 2.0 # Alerta si está a menos de 2 pips
        })
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
