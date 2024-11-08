import cv2


import cv2


def watermark_video(input_path, output_path, interval=20):
    cap = cv2.VideoCapture(input_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

    frame_no = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)  # Write the current frame

        # Check if it's time to duplicate
        if frame_no % interval == 0:
            out.write(frame)  # Write it again to watermark
            frame_no += 1  # Skip the next frame to avoid increasing frame count

        frame_no += 1  # Increment frame count normally

    cap.release()
    out.release()
    return frame_no


import cv2
import numpy as np


from skimage.metrics import structural_similarity as ssim


def detect_watermark(video_path, interval=20):
    cap = cv2.VideoCapture(video_path)
    detected_pattern = []
    frame_no = 0
    prev_frame = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_no % interval == 1:
            if prev_frame is not None:
                # Convert frames to grayscale for SSIM
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

                # Calculate SSIM
                similarity = ssim(frame_gray, prev_frame_gray)

                # Debug print to check the similarity
                print(f"Frame {frame_no}: Similarity = {similarity}")

                # If similarity is above a certain threshold, consider it a duplicate
                if similarity * 1000 > 999:  # Adjust threshold based on your needs
                    detected_pattern.append(frame_no)

        # Update the previous frame
        prev_frame = frame.copy()

        frame_no += 1

    cap.release()
    return detected_pattern


def check_pattern(interval, frames, detected):
    lst = []
    for i in range(1, frames, interval):
        lst.append(i + interval)
    ans = 0
    for i in lst:
        if i in detected:
            ans += 1
    if (ans / len(lst)) * 10 > 7:
        return True
    else:
        return False


def merge_audio():
    import subprocess
    import os

    # Define the input and output file names
    input_video = "inpt.mp4"
    watermarked_video = "watermarked.mp4"
    temp_output_video = "temp_watermarked.mp4"  # Temporary output file

    # Temporary audio file
    audio_extracted = "extracted_audio.mp3"

    # Step 1: Extract audio from the input video
    extract_audio_cmd = [
        "ffmpeg",
        "-i",
        input_video,
        "-q:a",
        "0",  # Quality
        "-map",
        "a",  # Map audio
        audio_extracted,
    ]

    # Run the command to extract audio
    subprocess.run(extract_audio_cmd)

    # Step 2: Merge the extracted audio with the watermarked video, using a temporary output file
    merge_audio_cmd = [
        "ffmpeg",
        "-i",
        watermarked_video,
        "-i",
        audio_extracted,
        "-c:v",
        "copy",  # Copy video codec
        "-c:a",
        "aac",  # Encode audio to AAC
        "-strict",
        "experimental",  # Allow experimental codecs
        temp_output_video,  # Use a temporary output file
    ]

    # Run the command to merge audio with the watermarked video
    subprocess.run(merge_audio_cmd)

    # Step 3: Rename the temporary output file to overwrite the original watermarked video
    # os.replace(temp_output_video, watermarked_video)

    # Clean up: Optionally remove the extracted audio file
    os.remove(audio_extracted)

    print("Audio extracted and merged successfully, overwriting watermarked.mp4.")


if __name__ == "__main__":
    frames = watermark_video("inpt.mp4", "watermarked.mp4", interval=20)

    merge_audio()

    detected = detect_watermark("temp_watermarked.mp4", interval=20)
    print("Detected watermark frames:", detected)
    print(check_pattern(20, frames, detected))
