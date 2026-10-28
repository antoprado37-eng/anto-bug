from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
import string

class AmongUsControlServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # Habilitar CORS para que tu página web pueda comunicarse sin bloqueos
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        if self.path == '/crear-sala':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Recibir los parámetros enviados por antobug.com
                params = json.loads(post_data.decode('utf-8'))
                impostores = params.get('impostores', 2)
                velocidad = params.get('velocidad', 1.5)
                
                print(f"[SERVIDOR] Creando sala bug con {impostores} impostores y velocidad x{velocidad}...")

                # Aquí genera un código aleatorio de 6 letras para simular la sala de Among Us
                letras_disponibles = string.ascii_uppercase
                codigo_sala = ''.join(random.choice(letras_disponibles) for _ in range(6))

                # Responderle a tu página web con el código creado
                self._set_headers()
                respuesta = {
                    "status": "success",
                    "code": codigo_sala
                }
                self.wfile.write(json.dumps(respuesta).encode('utf-8'))

            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AmongUsControlServer)
    print(f"[OK] Servidor de control de Among Us corriendo en el puerto {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    run()

