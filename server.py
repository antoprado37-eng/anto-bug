from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
import string

class AmongUsControlServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # Permisos de seguridad corregidos para antobug.com
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

                # Generar código aleatorio de 6 letras para Among Us
                letras = string.ascii_uppercase
                codigo_sala = ''.join(random.choice(letras) for _ in range(6))

                respuesta = {
                    "status": "success",
                    "code": codigo_sala
                }
                self.wfile.write(json.dumps(respuesta).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AmongUsControlServer)
    print(f"Servidor corriendo en puerto {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    run()
