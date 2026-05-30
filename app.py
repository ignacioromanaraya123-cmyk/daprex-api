from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TICKET = "68D39C0B-D8C4-4726-BB9C-26844070E4A9"
URL_BASE = "https://api2.mercadopublico.cl/v2/compra-agil"

@app.route('/')
def proxy():
    codigo = request.args.get('codigo')
    if not codigo:
        return jsonify({"error": "Ejemplo: ?codigo=5756-282-COT26"})
    
    # Usar el endpoint de DETALLE (no listado)
    url = f"{URL_BASE}/{codigo}"
    headers = {"ticket": TICKET}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        # Si la API respondió con éxito, devolvemos el payload
        if data.get('success') == 'OK':
            return jsonify(data.get('payload'))
        else:
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
