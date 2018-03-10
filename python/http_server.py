# simple HTTP server for python3
# run this server: python http_server.py >/dev/null 2>&1 &
from http.server import HTTPServer, CGIHTTPRequestHandler


port = 8080

httpd = HTTPServer(('',port), CGIHTTPRequestHandler)
print('Starting simple httpd on port: ' + str(httpd.server_port))
httpd.serve_forever()
