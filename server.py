from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import string
import os

app = Flask(__name__)
# Permitir que antobug.com acceda sin bloqueos de seguridad
CORS(app)

@app.route('/crear-sala', methods=['POST'])
def crear_sala():
    try:
        data = request.get_json() or {}
        impostores = data.get('impostores', 2)
        velocidad = data.get('velocidad', 1.5)
        
        print(f"Petición recibida: Impostores {impostores}, Velocidad {velocidad}")

        # Generar código de 6 letras válido para Among Us
        letras = string.ascii_uppercase
        codigo_sala = ''.join(random.choice(letras) for _ in range(6))

        return jsonify({
            "status": "success",
            "code": codigo_sala
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Render asigna el puerto automáticamente aquí
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
