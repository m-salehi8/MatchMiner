
#!/usr/bin/env python3

import http.server
import socketserver
import os

PORT = 8081
Handler = http.server.SimpleHTTPRequestHandler

current_directory = os.getcwd()

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Serving HTTP on 0.0.0.0 port {PORT} (http://0.0.0.0:{PORT}/) from {current_directory}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")







