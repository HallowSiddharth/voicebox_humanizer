import numpy as np
from scipy.io import wavfile


# Embed a watermark into an audio signal
def embed_watermark(audio_file, watermark, output_file):
    # Read the audio file
    samplerate, data = wavfile.read(audio_file)

    # Make sure the watermark is in the right format
    watermark = np.array(list(watermark.encode()), dtype=np.uint8)

    # Ensure the watermark fits into the audio data
    if len(watermark) * 8 > len(data):
        raise ValueError("Watermark is too long for this audio file.")

    # Embed the watermark into the LSB of the audio data
    for i in range(len(watermark)):
        for bit in range(8):  # Process each bit of the watermark byte
            data[i * 8 + bit] = (data[i * 8 + bit] & 0xFE) | (
                (watermark[i] >> (7 - bit)) & 0x01
            )

    # Save the watermarked audio
    wavfile.write(output_file, samplerate, data)


# Extract the watermark from the audio signal
def extract_watermark(audio_file, watermark_length):
    samplerate, data = wavfile.read(audio_file)

    # Extract the LSB from the audio data
    extracted_watermark = []
    for i in range(watermark_length):
        byte_value = 0
        for bit in range(8):  # Collect 8 bits to form a byte
            byte_value = (byte_value << 1) | (data[i * 8 + bit] & 0x01)
        extracted_watermark.append(byte_value)

    # Convert to string
    extracted_watermark = "".join(chr(b) for b in extracted_watermark)
    return extracted_watermark


# # Example usage
# audio_file = "audio.wav"
# output_file = "watermarked_output.wav"
# watermark = "This audio is generated using VoiceCraftAI"

# embed_watermark(audio_file, watermark, output_file)
# extracted_watermark = extract_watermark(output_file, len(watermark))

# print("Extracted Watermark:", extracted_watermark)
