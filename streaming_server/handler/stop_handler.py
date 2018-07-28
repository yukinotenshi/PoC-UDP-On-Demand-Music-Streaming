from typing import Tuple

from streaming_server import config
from streaming_server.handler.base_request_handler import RequestHandler


class StopHandler(RequestHandler):
    def __init__(self, socket, client_address: Tuple[str, int]):
        super().__init__(socket, client_address)

    def execute(self):
        for t in config.LONG_RUN_THREADS:
            if t['client'] == self.client_address:
                t['instance'].stop = True
                t['instance'].paused = False
                break

        return None
