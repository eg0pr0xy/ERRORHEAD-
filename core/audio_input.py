# core/audio_input.py

import numpy as np
from pydub import AudioSegment
import threading
import time
from scipy.fftpack import fft

class AudioReactiveInput:
    def __init__(self, file_path):
        self.amplitude = 0.0
        self.file_path = file_path
        self.audio = AudioSegment.from_file(file_path).set_channels(1).set_frame_rate(44100)
        self.samples = np.array(self.audio.get_array_of_samples()).astype(np.float32)
        self.sample_rate = 44100
        self.buffer_size = 2048
        self.position = 0
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.process)
        self.thread.start()

    def process(self):
        while self.running and self.position + self.buffer_size < len(self.samples):
            chunk = self.samples[self.position:self.position + self.buffer_size]
            self.position += self.buffer_size

            fft_vals = np.abs(fft(chunk))[:self.buffer_size // 2]
            self.amplitude = np.clip(np.mean(fft_vals) / 10000.0, 0.0, 1.0)

            time.sleep(self.buffer_size / self.sample_rate)

    def stop(self):
        self.running = False

    def get_amplitude(self):
        return self.amplitude