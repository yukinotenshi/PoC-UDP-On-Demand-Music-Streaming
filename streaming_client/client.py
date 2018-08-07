from typing import List, Tuple, Dict
import socket

from streaming_client.audio_player import AudioPlayer
from streaming_client import config


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.player = AudioPlayer(self.socket)
        self.servers: Dict[str, Tuple[str, int]] = {}
        self.connected: bool = False
        self.playing: bool = False
        self.paused: bool = True
        self.songs: List[str] = []

    def subscribe(self, name: str, server: Tuple[str, int]):
        if name not in self.servers:
            self.servers[name] = server

    def connect(self, name: str):
        if name not in self.servers:
            raise Exception("Server hasn't been subscribed")

        server = self.servers[name]
        self.socket.connect(server)
        self.connected = True

    def close(self):
        self.socket.close()

    def list_song(self):
        if not self.connected:
            raise Exception("You should connect to a server first")

        self.songs = []
        self.socket.send(b"song")
        self.songs = self.socket.recv(config.BUFFER_SIZE).decode(config.CODEC)[1:].split("\n")

    def stop(self):
        self.player.next_available = False
        self.playing = False

    def empty_buffer(self):
        self.socket.settimeout(1)
        while True:
            try:
                self.socket.recv(config.BUFFER_SIZE)
            except:
                break
        self.socket.settimeout(None)

    def play(self, song_index: int):
        if len(self.songs) <= song_index:
            raise Exception("No such song")

        if self.paused:
            self.resume()

        if self.playing:
            self.stop()
            self.empty_buffer()

        self.player = AudioPlayer(self.socket)
        self.player.load_song(self.songs[song_index])
        self.player.start()
        self.playing = True

    def pause(self):
        if self.playing:
            self.player.paused = True
            self.paused = True

    def resume(self):
        if self.paused:
            self.player.paused = False
            self.paused = False

    def exit(self):
        self.stop()
        self.player.paused = False
        self.player.join()