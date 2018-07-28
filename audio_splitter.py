from pydub import AudioSegment


class AudioSplitter:
    def __init__(self, file_name: str, name: str):
        self.name: str = name
        self.audio_segment: AudioSegment = AudioSegment.from_wav(file_name)

    def split(self, segment_size=5000):
        audio_duration: int = len(self.audio_segment)

        for x in range(0, audio_duration, segment_size):
            segment: AudioSegment = self.audio_segment[x:x+segment_size]
            segment.export(f"{self.name}-{int(x/segment_size)}.wav", format="wav")

        self.write_meta_data(int(audio_duration/segment_size))

    def write_meta_data(self, count):
        with open(f"{self.name}.txt", "w") as f:
            f.write(f"{count}")
