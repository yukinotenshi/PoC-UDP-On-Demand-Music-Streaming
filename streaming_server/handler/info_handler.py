from typing import Tuple
import wave

from streaming_server.handler.base_request_handler import RequestHandler
from streaming_server import config


class InfoHandler(RequestHandler):
    def __init__(self, socket, client_address: Tuple[str, int]):
        super().__init__(socket, client_address)
        self.song_name: str = ""

    def load_arguments(self, *args):
        self.song_name: str = " ".join(args)

    def execute(self):
        wf = wave.open(f"{config.SONG_DIRECTORY}/{self.song_name}.wav", 'rb')

        channel_count: int = wf.getnchannels()
        rate: int = wf.getframerate()
        sample_width: int = wf.getsampwidth()

        meta_data: bytes = f"{channel_count},{rate},{sample_width}".encode(config.CODEC)
        wf.close()

        return meta_data
