import pyaudio
import wave
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("0.0.0.0", 5555))

sock.send(b"info test")
response = sock.recv(2048).decode('utf-8')
print(response)
channel_count, rate, sample_width = response.split(',')


p = pyaudio.PyAudio()

stream = p.open(format =
                p.get_format_from_width(int(sample_width)),
                channels = int(channel_count),
                rate = int(rate),
                output = True)

sock.send(b"play test")
data = sock.recv(2048)

while data != '':
    stream.write(data)
    sock.send(b"continue")
    data = sock.recv(2048)

stream.close()
p.terminate()
