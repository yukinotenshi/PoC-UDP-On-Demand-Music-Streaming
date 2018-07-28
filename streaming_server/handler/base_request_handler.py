from threading import Thread
from typing import Tuple
from socket import SocketType

from streaming_server import config


class RequestHandler(Thread):
    def __init__(self, socket, client_address: Tuple[str, int]):
        super().__init__()
        self.socket: SocketType = socket
        self.client_address = client_address
        self.stop = False
        self.can_stop = False

    def load_arguments(self, *args):
        pass

    def execute(self):
        pass

    def run(self):
        response = self.execute()

        if response:
            self.socket.sendto(response, self.client_address)

    def dict(self):
        return {
            "client" : self.client_address,
            "instance" : self
        }
