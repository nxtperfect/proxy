from dataclasses import dataclass
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

HTTP_SERVER_PORT = 8228


def main():
    print("Hello from proxy!")


@dataclass
class Proxy:
    ip: str
    port: int

    def start(self):
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with self.socket.bind((self.ip, self.port))
            self.socket.listen(5)
            try:
                while True:
                    c, addr = self.socket.accept()
                    c.send("Nice".encode())
                    c.close()
            except:
                self.socket.close()


def reverse_proxy():
    pass


def server():
    proxy = Proxy("", HTTP_SERVER_PORT)
    print(f"Server live on port {HTTP_SERVER_PORT}")
    proxy.start()


if __name__ == "__main__":
    main()
    server()
