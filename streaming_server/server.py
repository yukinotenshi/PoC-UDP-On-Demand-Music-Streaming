import socket
import threading
from typing import Tuple
from streaming_server.router import Router

from streaming_server import config


class SocketServer(threading.Thread):
    def __init__(self, address: str = "0.0.0.0", port: int = 5555):
        super().__init__()
        self.buffer = config.BUFFER_SIZE
        self.server: Tuple[str, int] = (address, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.server)

    def run(self):
        while True:
            payload, client_address = self.socket.recvfrom(self.buffer)
            router = Router(self.socket, payload, client_address)
            router.execute()
