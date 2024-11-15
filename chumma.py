text = "நான் என்ன பண்ணினாலும் இந்த உலகம் என்ன பத்தி பேசவோ, இல்ல என்ன தீர்மானிகவோ தான் இருந்தாங்க, நான் செய்யாதா விஷயங்களுக்கு கூட"

# cmd = [
#     "edge-tts",
#     "--voice",
#     "ta-IN-ValluvarNeural",
#     "--text",
#     text,
#     "--write-media",
#     "srk_voice.wav",
# ]

merge_audio_cmd = [
    "ffmpeg",
    "-y",  # Automatically overwrite the output file
    "-i",
    "srk_sample_video.mp4",  # Input video file
    "-i",
    "sample_srk.wav",  # New audio file
    "-map",
    "0:v",  # Select the video stream from the original video
    "-map",
    "1:a",  # Select the audio stream from the new audio file
    "-c:v",
    "libx264",  # Use H.264 codec for video
    "-c:a",
    "aac",  # Encode audio to AAC
    "-strict",
    "experimental",  # Allow experimental codecs (needed for AAC encoding)
    "chumma_sample_out.mp4",  # Output file
]

import subprocess

subprocess.run(merge_audio_cmd)
