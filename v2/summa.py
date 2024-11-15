import cv2
import numpy as np
from moviepy.editor import AudioFileClip, VideoFileClip
import wave
import struct

# Video parameters
width, height = 640, 480
frame_rate = 30
duration = 5  # in seconds
total_frames = frame_rate * duration

# VideoWriter setup for MP4 (using H.264 codec)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # For MP4 format
video_filename = "frame_number_video.mp4"
out = cv2.VideoWriter(video_filename, fourcc, frame_rate, (width, height))

# Font for text
font = cv2.FONT_HERSHEY_SIMPLEX

# Create video with frame number
for frame_number in range(total_frames):
    # Create a black image (frame)
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Add frame number text to the image
    text = f"Frame {frame_number}"
    cv2.putText(
        frame, text, (150, height // 2), font, 1, (255, 255, 255), 2, cv2.LINE_AA
    )

    # Write the frame to the video
    out.write(frame)

# Release the video writer object
out.release()

# Generate random noise audio
sample_rate = 44100  # samples per second
num_samples = int(sample_rate * duration)
audio_data = np.random.uniform(-1, 1, num_samples)  # Random noise between -1 and 1
audio_data = np.int16(audio_data * 32767)

# Save the audio as a WAV file
audio_filename = "random_noise.wav"
with wave.open(audio_filename, "w") as audio_file:
    audio_file.setnchannels(1)  # Mono audio
    audio_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
    audio_file.setframerate(sample_rate)
    audio_file.writeframes(audio_data.tobytes())

# Load video and audio files using moviepy
video_clip = VideoFileClip(video_filename)
audio_clip = AudioFileClip(audio_filename)

# Set audio to the video
video_with_audio = video_clip.set_audio(audio_clip)

# Write the final video with audio to file
final_video_filename = "frame_number_video_with_audio.mp4"
video_with_audio.write_videofile(
    final_video_filename, codec="libx264", audio_codec="aac"
)

print(f"Video created successfully as {final_video_filename}.")
