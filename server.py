from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
import string
import os

class AmongUsControlServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        if self.path == '/crear-sala':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
                
                params = json.loads(post_data.decode('utf-8')) if post_data else {}
                impostores = params.get('impostores', 2)
                velocidad = params.get('velocidad', 1.5)

                # Código de 6 letras aleatorio para Among Us
                letras = string.ascii_uppercase
                codigo_sala = ''.join(random.choice(letras) for _ in range(6))

                respuesta = {
                    "status": "success",
                    "code": codigo_sala
                }
                self.wfile.write(json.dumps(respuesta).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

def run():
    # Detecta automáticamente el puerto asignado por Render (por defecto 10000 o el 8080 que pusiste)
    port = int(os.environ.get("PORT", 8080))
    # Enlaza el host a 0.0.0.0 requerido obligatoriamente por Render
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, AmongUsControlServer)
    print(f"Servidor corriendo en el puerto {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    run()
