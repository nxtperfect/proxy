from collections.abc import ByteString
from dataclasses import dataclass
import socket
from _thread import start_new_thread
from sys import exit

HTTP_SERVER_PORT = 8228


@dataclass
class Proxy:
    ip: str
    port: int
    max_connections: int = 5
    buffer_size: int = 1024

    def start(self):
        print("Starting new proxy...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen()
        try:
            conn, addr = self.sock.accept()
            data = conn.recv(self.buffer_size)
            print(data)
            _ = start_new_thread(self._connection_string, (data, conn, addr))
        except Exception as e:
            print(f"Failed to get request. {e}")
        finally:
            self.sock.close()
            exit(1)

    def _connection_string(self, data: ByteString, conn, addr):
        first_line = data.split(b"\n")[0]
        url = first_line.split()[1]
        url_pos = url.find(b"://")
        if url_pos:
            url = first_line[web_pos + 3 :].split()[
                0
            ]  # get url after http://, return until first whitespace
        ip_pos = url.find(b":")
        web_pos = url.find(b"/")
        ip = url[:ip_pos].split()[-1]
        if not ip:
            ip = "0.0.0.0"
        port = int(url[ip_pos:web_pos].split()[0])
        if not port:
            port = 80
        webserver = url[webpos:].split()[0]
        self._proxy_server(webserver, data, conn, addr)

    def _proxy_server(
        self,
    ):
        # get data from sending the request
        # return it
        pass


def reverse_proxy():
    pass


def server():
    proxy = Proxy("", HTTP_SERVER_PORT)
    print(f"Server live on port {HTTP_SERVER_PORT}")
    proxy.start()


if __name__ == "__main__":
    server()
