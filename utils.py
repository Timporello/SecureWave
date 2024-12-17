from pydub import AudioSegment
import struct

def load_audio_file(filepath: str):
    """
    Load an audio file (wav, mp3, m4a, etc.) and return:
      channels, sample_width, frame_rate, frame_count, raw_data (16-bit PCM)
    Requires ffmpeg installed for formats other than WAV.
    """
    audio = AudioSegment.from_file(filepath)

    # Convert to 16-bit PCM if not already
    if audio.sample_width != 2:
        audio = audio.set_sample_width(2)

    channels = audio.channels
    sample_width = audio.sample_width
    frame_rate = audio.frame_rate
    # Each frame = sample for each channel, total frames = len(raw_data) / (channels*sample_width)
    frame_count = len(audio.raw_data) // (channels * sample_width)
    raw_data = audio.raw_data

    return channels, sample_width, frame_rate, frame_count, raw_data

def save_audio_file(channels, sample_width, frame_rate, raw_data, output_path: str):
    """
    Save PCM data to an output audio file (WAV by default).
    You can choose another format supported by pydub.
    """
    audio = AudioSegment(
        data=raw_data,
        sample_width=sample_width,
        frame_rate=frame_rate,
        channels=channels
    )
    audio.export(output_path, format="wav")  # You can change format if desired.