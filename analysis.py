import numpy as np
import matplotlib.pyplot as plt
from utils import load_audio_file

class AudioAnalysis:
    def show_spectrogram(self, audio_path: str):
        channels, sampwidth, framerate, frame_count, raw_data = load_audio_file(audio_path)
        if sampwidth != 2:
            raise ValueError("Spectral analysis only supports 16-bit audio.")

        samples = np.frombuffer(raw_data, dtype='<h')
        # If multiple channels, just use the first for visualization
        if channels > 1:
            samples = samples.reshape(-1, channels)[:,0]

        plt.figure(figsize=(15, 4))  # Wider spectrogram
        plt.specgram(samples, NFFT=1024, Fs=framerate, noverlap=512, cmap='viridis')
        plt.title('Spectrogram')
        plt.xlabel('Time [s]')
        plt.ylabel('Frequency [Hz]')
        plt.colorbar(label='Intensity [dB]')
        plt.tight_layout()
        plt.show()