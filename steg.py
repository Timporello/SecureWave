import wave
import struct

class AudioSteganography:
    """
    Class responsible for hiding and extracting text messages within WAV audio files
    using LSB (least significant bit) steganography.
    """

    def __init__(self):
        # Could store configurations or other parameters if needed
        pass

    def hide_message(self, input_wav_path: str, output_wav_path: str, message: str) -> None:
        """
        Hide a UTF-8 text message inside a WAV file using least significant bit encoding.

        :param input_wav_path: Path to the original WAV file.
        :param output_wav_path: Path to the output WAV file with the hidden message.
        :param message: The text message to hide.
        :raises ValueError: If the WAV is not 16-bit or message doesn't fit.
        """
        message_bytes = message.encode('utf-8')
        message_length = len(message_bytes)
        length_bytes = message_length.to_bytes(4, byteorder='big')

        full_payload = length_bytes + message_bytes
        payload_bits = ''.join(f'{byte:08b}' for byte in full_payload)  # Convert to bit string

        with wave.open(input_wav_path, 'rb') as wav_in:
            params = wav_in.getparams()
            n_frames = wav_in.getnframes()
            raw_frames = wav_in.readframes(n_frames)

        # Check sample width: must be 16-bit
        if params.sampwidth != 2:
            raise ValueError("Currently only 16-bit WAV files are supported.")

        num_channels = params.nchannels
        total_samples = n_frames * num_channels

        if len(payload_bits) > total_samples:
            raise ValueError("The message is too long to fit in the given audio file.")

        # Unpack samples
        samples = list(struct.unpack('<' + 'h' * total_samples, raw_frames))

        # Embed payload bit-by-bit
        bit_index = 0
        for i in range(total_samples):
            if bit_index < len(payload_bits):
                # Modify LSB
                samples[i] = (samples[i] & ~1) | int(payload_bits[bit_index])
                bit_index += 1

        # Repacks samples
        modified_frames = struct.pack('<' + 'h' * total_samples, *samples)

        # Write to output
        with wave.open(output_wav_path, 'wb') as wav_out:
            wav_out.setparams(params)
            wav_out.writeframes(modified_frames)

    def extract_message(self, stego_wav_path: str) -> str:
        """
        Extract a hidden UTF-8 text message from a WAV file.

        :param stego_wav_path: Path to the WAV file containing the hidden message.
        :return: The extracted text message.
        :raises ValueError: If the WAV is not 16-bit or extraction fails.
        """
        with wave.open(stego_wav_path, 'rb') as wav_in:
            params = wav_in.getparams()
            n_frames = wav_in.getnframes()
            num_channels = params.nchannels

            if params.sampwidth != 2:
                raise ValueError("Currently only 16-bit WAV files are supported.")

            raw_frames = wav_in.readframes(n_frames)
            total_samples = n_frames * num_channels
            samples = list(struct.unpack('<' + 'h' * total_samples, raw_frames))

        # Extract bits
        bits = [str(sample & 1) for sample in samples]
        bit_string = ''.join(bits)

        # First 32 bits for message length
        length_bits = bit_string[:32]
        msg_length = int(length_bits, 2)

        message_bits = bit_string[32:32 + (msg_length * 8)]
        message_bytes = int(message_bits, 2).to_bytes(msg_length, byteorder='big')
        message = message_bytes.decode('utf-8', errors='replace')

        return message