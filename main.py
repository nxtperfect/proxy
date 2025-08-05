from dataclasses import dataclass
from http.server import HTTPServer, BaseHTTPRequestHandler
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
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(self.max_connections)
        try:
            while True:
                conn, addr = self.socket.accept()
                data = conn.recv(self.buffer_size)
                _ = start_new_thread(self._connection_string, (conn, data, addr))
        except Exception as e:
            self.socket.close()
            print(f"! Error {e}")

    def _connection_string(
        self, conn: socket.socket, data: str, addr: socket._RetAddress
    ):
        print(data)
        first_line = data.split(b"\n")[0]
        http_position = data.find(b"://")
        url = first_line.split()[1]
        temp = first_line
        if http_position:
            temp = url[http_position + 3 :]  # 3 = len('://')
        port_pos = temp.find(b":")
        web_pos = temp.find(b"/")
        if not web_pos:
            web_pos = len(temp)
        webserver = ""
        port = -1
        if not port_pos or web_pos < port_pos:
            port = 80
            webserver = temp[:web_pos]
        else:
            port = int((temp[(port_pos + 1) :])[: web_pos - port_pos - 1])
            webserver = temp[:port_pos]
        self._proxy_server(webserver, port, conn, addr, data)

    def _proxy_server(
        self,
        webserver: str,
        port: int,
        conn: socket.socket,
        addr: socket._RetAddress,
        data,
    ):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((webserver, port))
            _ = sock.send(data)

            while 1:
                reply = sock.recv(self.buffer_size)
                if not len(reply):
                    break
                _ = conn.send(reply)

                data_size_kb = float(len(reply))
                data_size_kb = f"{data_size_kb/1024.0:.2f} KB"
                print("Request Done: %s => %s <=" % (str(addr[0]), str(data_size_kb)))

        except socket.error:
            print(sock.error)
            exit(1)
        finally:
            sock.close()
            conn.close()


def reverse_proxy():
    pass


def server():
    proxy = Proxy("", HTTP_SERVER_PORT)
    print(f"Server live on port {HTTP_SERVER_PORT}")
    proxy.start()


if __name__ == "__main__":
    server()
