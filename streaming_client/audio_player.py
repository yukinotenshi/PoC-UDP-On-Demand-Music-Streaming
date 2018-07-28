from threading import Thread
from time import sleep
from typing import List
import pyaudio
import socket

from streaming_client import config


class AudioPlayer(Thread):
    def __init__(self, sock: socket.SocketType):
        super().__init__()
        self.paused: bool = False
        self.socket: socket.SocketType = sock
        self.next_available = False
        self.current_pos: int = -1
        self.data: List[bytes] = []
        self.song: str = ""
        self.stream = None
        self.audio = pyaudio.PyAudio()

    def load_song(self, song_name):
        self.song: str = song_name
        self.data = []
        self.next_available = True

    def request_next_chunk(self):
        if not self.next_available:
            return
        sock.send(b"continue")
        data = sock.recv(config.BUFFER_SIZE)

        if len(data) < config.BUFFER_SIZE:
            self.next_available = False

        self.data.append(data)
        self.current_pos += 1

    def initialize(self):
        sock.send(f"info {self.song}".encode(config.CODEC))
        response = sock.recv(2048).decode('utf-8')
        print(response)
        channel_count, rate, sample_width = response.split(',')

        self.stream = self.audio.open(format=
                        self.audio.get_format_from_width(int(sample_width)),
                        channels=int(channel_count),
                        rate=int(rate),
                        output=True)

        sock.send(f"play {self.song}".encode(config.CODEC))
        self.data.append(sock.recv(config.BUFFER_SIZE))
        print(self.data)
        self.current_pos = 0

    def stop(self):
        self.paused = True
        sock.send(b"stop")

    def run(self):
        self.initialize()

        while self.next_available:
            self.stream.write(self.data[self.current_pos])
            self.request_next_chunk()
            while self.paused:
                sleep(0.1)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("0.0.0.0", 5555))

player = AudioPlayer(sock)
player.load_song("test")
player.start()
