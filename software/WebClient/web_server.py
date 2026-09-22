import http.server
import ssl
import socket

PORT = 4443

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

handler = http.server.SimpleHTTPRequestHandler
httpd = http.server.HTTPServer(('0.0.0.0', PORT), handler)

# Enable SSL using the generated certs
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

local_ip = get_local_ip()
print("="*50)
print(f"WEB CLIENT RUNNING!")
print(f"Tell players to open this URL on their phones:")
print(f"👉 https://{local_ip}:{PORT}")
print("\n(Note: Browsers will show a 'Not Secure' warning because it's a self-signed local cert. Just click 'Advanced' -> 'Proceed to site').")
print("="*50)

httpd.serve_forever()
