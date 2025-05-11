import http.server
import socketserver
import os

PORT = 3000
Handler = http.server.SimpleHTTPRequestHandler

# Change to the frontend directory
os.chdir('frontend')

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving frontend at http://localhost:{PORT}")
    httpd.serve_forever() 