from os import listdir
from os.path import isfile, join
from typing import Tuple

from streaming_server import config
from streaming_server.handler.base_request_handler import RequestHandler


class SongHandler(RequestHandler):
    def __init__(self, socket, client_address: Tuple[str, int]):
        super().__init__(socket, client_address)

    def execute(self):
        songs = [f for f in listdir(config.SONG_DIRECTORY) if isfile(join(config.SONG_DIRECTORY, f))]
        song_names = [".".join(s.split(".")[:-1]).encode(config.CODEC) for s in songs]

        return b"\n".join(song_names)
