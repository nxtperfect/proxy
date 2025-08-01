from http.server import HTTPServer, BaseHTTPRequestHandler

HTTP_SERVER_PORT = 8008


def main():
    print("Hello from proxy!")


def proxy():
    pass


def reverse_proxy():
    pass


def server():
    server_address = ("", HTTP_SERVER_PORT)
    httpd = HTTPServer(server_address, BaseHTTPRequestHandler)
    print(f"Server live on port {HTTP_SERVER_PORT}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
    server()
