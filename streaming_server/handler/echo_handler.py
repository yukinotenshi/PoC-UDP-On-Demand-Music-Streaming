from typing import Tuple

from streaming_server.handler.base_request_handler import RequestHandler
from streaming_server import config


class EchoHandler(RequestHandler):
    def __init__(self, socket, client_address: Tuple[str, int]):
        super().__init__(socket, client_address)
        self.message = ""

    def load_arguments(self, *args):
        self.message = ' '.join(args)

    def execute(self):
        return self.message.encode(config.CODEC)
