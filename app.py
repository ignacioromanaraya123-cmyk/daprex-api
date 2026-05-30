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

    # 🔥 CAMBIO IMPORTANTE: usar 'busqueda' en lugar de 'codigo'
    url = f"{URL_BASE}?busqueda={codigo}&tamano_pagina=10"
    headers = {"ticket": TICKET}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()

        # Si la API devuelve varios resultados, tomamos el primero
        items = data.get('payload', {}).get('items', [])
        if items:
            return jsonify(items[0])  # devolvemos solo la primera coincidencia
        else:
            return jsonify({"error": f"No se encontró la compra con código {codigo}"})
    except Exception as e:
        return jsonify({"error": str(e)})
