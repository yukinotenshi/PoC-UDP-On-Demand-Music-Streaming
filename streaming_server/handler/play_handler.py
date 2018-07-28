from typing import Tuple
from time import sleep
import wave

from streaming_server.handler.base_request_handler import RequestHandler
from streaming_server import config


class PlayHandler(RequestHandler):
    def __init__(self, socket, client_address: Tuple[str, int]):
        super().__init__(socket, client_address)
        self.can_stop = True
        self.paused = False
        self.song_name: str = ""

    def load_arguments(self, *args):
        self.song_name: str = " ".join(args)

    def execute(self):
        chunk = config.BUFFER_SIZE

        wf = wave.open(f"{config.SONG_DIRECTORY}/{self.song_name}.wav", 'rb')

        data = wf.readframes(chunk)

        while data != '' and not self.stop:
            self.socket.sendto(data, self.client_address)
            data = wf.readframes(chunk)
            self.paused = True
            while self.paused:
                sleep(0.1)

        wf.close()
        config.LONG_RUN_THREADS.remove(self.dict())
