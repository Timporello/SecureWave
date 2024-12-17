import struct
from utils import load_audio_file, save_audio_file

class AudioSteganography:
    def __init__(self):
        pass

    def hide_message(self, input_path: str, output_path: str, message: str) -> None:
        message_bytes = message.encode('utf-8')
        message_length = len(message_bytes)
        length_bytes = message_length.to_bytes(4, byteorder='big')
        full_payload = length_bytes + message_bytes
        payload_bits = ''.join(f'{byte:08b}' for byte in full_payload)

        channels, sampwidth, framerate, frame_count, raw_data = load_audio_file(input_path)
        if sampwidth != 2:
            raise ValueError("Only 16-bit PCM audio is supported for steganography.")

        total_samples = frame_count * channels
        if len(payload_bits) > total_samples:
            raise ValueError("Message too long for given audio file.")

        samples = list(struct.unpack('<' + 'h' * total_samples, raw_data))

        # Embed message bits into LSB of samples
        bit_index = 0
        for i in range(total_samples):
            if bit_index < len(payload_bits):
                samples[i] = (samples[i] & ~1) | int(payload_bits[bit_index])
                bit_index += 1

        modified_frames = struct.pack('<' + 'h' * total_samples, *samples)
        save_audio_file(channels, sampwidth, framerate, modified_frames, output_path)

    def extract_message(self, input_path: str) -> str:
        channels, sampwidth, framerate, frame_count, raw_data = load_audio_file(input_path)
        if sampwidth != 2:
            raise ValueError("Only 16-bit PCM audio is supported.")

        total_samples = frame_count * channels
        samples = list(struct.unpack('<' + 'h' * total_samples, raw_data))

        bits = [str(sample & 1) for sample in samples]
        bit_string = ''.join(bits)

        # First 32 bits = length
        length_bits = bit_string[:32]
        msg_length = int(length_bits, 2)
        message_bits = bit_string[32:32+(msg_length*8)]
        message_bytes = int(message_bits, 2).to_bytes(msg_length, byteorder='big')
        return message_bytes.decode('utf-8', errors='replace')