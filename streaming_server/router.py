import importlib
from typing import Tuple

from streaming_server import config
from streaming_server.handler.base_request_handler import RequestHandler


class Router:
    def __init__(self, socket, payload: bytes, client_address: Tuple[str, int]):
        self.payload: str = payload.decode('utf-8')
        self.socket = socket
        self.client_address = client_address

    def execute(self):
        split_payload = self.payload.split()
        command, args = split_payload[0], split_payload[1:]
        module = importlib.import_module(f"handler.{command}_handler")
        handler_class = getattr(module, f"{command[0].upper() + command[1:]}Handler")

        handler_instance: RequestHandler = handler_class(self.socket, self.client_address)
        handler_instance.load_arguments(*args)
        handler_instance.start()

        if handler_instance.can_stop:
            config.LONG_RUN_THREADS.append({
                "client" : self.client_address,
                "instance" : handler_instance
            })
