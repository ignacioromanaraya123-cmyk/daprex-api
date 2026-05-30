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
    
    # Usamos el parámetro 'codigo' (no 'busqueda')
    url = f"{URL_BASE}?codigo={codigo}&tamano_pagina=10"
    headers = {"ticket": TICKET}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        # Verificar si la respuesta es exitosa
        if data.get('success') == 'OK':
            items = data.get('payload', {}).get('items', [])
            if items:
                return jsonify(items[0])
            else:
                return jsonify({"error": f"No se encontró la compra con código {codigo}"})
        else:
            # Devolver el error exacto de la API
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
