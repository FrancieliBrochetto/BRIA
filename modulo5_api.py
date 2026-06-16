# modulo5_api.py
# Módulo 5 — API Flask (ponte entre o banco e o frontend)

from flask import Flask, jsonify
from flask_cors import CORS
from modulo3_banco import buscar_noticias_do_dia, buscar_historico
from datetime import date

app = Flask(__name__)
CORS(app)  # permite que o navegador acesse a API


@app.route("/api/briefing/hoje")
def briefing_hoje():
    noticias = buscar_noticias_do_dia()
    return jsonify({
        "data": date.today().isoformat(),
        "noticias": noticias
    })


@app.route("/api/briefing/<data>")
def briefing_por_data(data):
    noticias = buscar_noticias_do_dia(data)
    return jsonify({
        "data": data,
        "noticias": noticias
    })


@app.route("/api/historico")
def historico():
    dias = buscar_historico(dias=7)
    return jsonify(dias)


if __name__ == "__main__":
    app.run(debug=True, port=5000)