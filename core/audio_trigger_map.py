# core/audio_trigger_map.py

import numpy as np
from pydub import AudioSegment
from scipy.signal import find_peaks

def extract_trigger_times(audio_path, threshold=0.3, spacing=0.25):
    audio = AudioSegment.from_file(audio_path).set_channels(1).set_frame_rate(44100)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples /= np.max(np.abs(samples))

    # Rolling RMS (Signalenergie)
    window_size = 2048
    rms = np.sqrt(np.convolve(samples**2, np.ones(window_size)/window_size, mode='valid'))

    # Peaks im RMS finden
    peaks, _ = find_peaks(rms, height=threshold, distance=int(spacing * 44100))
    times = peaks / 44100.0  # Sekunden
    return times.tolist()