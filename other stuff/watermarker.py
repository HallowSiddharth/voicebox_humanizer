import cv2
import numpy as np
import os


# Helper function: Apply DCT on an image block
def dct2(block):
    return cv2.dct(np.float32(block))


# Helper function: Apply inverse DCT on an image block
def idct2(block):
    return cv2.idct(block)


def embed_watermark(image, watermark):
    h, w = image.shape[:2]
    watermark = watermark[:h, :w]  # Resize watermark if necessary

    # Convert to YUV color space to focus on luminance (Y)
    yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    y_channel = yuv_image[:, :, 0]

    # Apply DCT to the Y channel
    dct_y = dct2(y_channel)

    # Increase watermark strength
    dct_y[: watermark.shape[0], : watermark.shape[1]] += (
        watermark * 0.2
    )  # Adjusted from 0.1 to 0.2

    # Apply inverse DCT
    y_channel_with_watermark = idct2(dct_y)

    # Replace Y channel with the watermarked Y channel
    yuv_image[:, :, 0] = y_channel_with_watermark
    watermarked_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR)

    return watermarked_image


# Load the video and embed watermark in each frame
def embed_watermark_in_video(input_video, output_video, watermark):
    cap = cv2.VideoCapture(input_video)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = None
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count == 0:
            # Initialize the video writer
            h, w = frame.shape[:2]
            out = cv2.VideoWriter(output_video, fourcc, 30, (w, h))

        # Embed watermark in the current frame
        watermarked_frame = embed_watermark(frame, watermark)

        # Write watermarked frame to output video
        out.write(watermarked_frame)
        frame_count += 1

    cap.release()
    out.release()
    print(f"Watermark embedded into {frame_count} frames of video.")


# Generate a fixed binary watermark (e.g., 8x8 block of ones)
def generate_fixed_watermark(size=(8, 8)):
    return np.ones(size, dtype=np.float32)  # Simple fixed watermark


# Example usage:
input_video = "input_video.mp4"
output_video = "output_with_watermark.mp4"
watermark = generate_fixed_watermark()  # Small watermark for testing

embed_watermark_in_video(input_video, output_video, watermark)


# Extract watermark from the DCT domain of the image
def extract_watermark(image, watermark_shape):
    # Convert to YUV color space to focus on luminance (Y)
    yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    y_channel = yuv_image[:, :, 0]

    # Apply DCT to the Y channel
    dct_y = cv2.dct(np.float32(y_channel))

    # Extract the watermark from the DCT coefficients
    extracted_watermark = dct_y[: watermark_shape[0], : watermark_shape[1]]

    # Normalize the watermark (optional step)
    extracted_watermark = np.where(extracted_watermark > 0, 1, 0)

    return extracted_watermark


# Check watermark presence in the video
def check_watermark_in_video(video_path, watermark_shape, original_watermark):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    watermark_detected = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Extract watermark from the current frame
        extracted_watermark = extract_watermark(frame, watermark_shape)

        # Check if the extracted watermark matches the original
        if np.array_equal(extracted_watermark, original_watermark):
            watermark_detected = True
            print(f"Watermark detected in frame {frame_count}.")
            break

        frame_count += 1

    cap.release()

    if not watermark_detected:
        print("Watermark not detected in the video.")


# Example usage:
watermark_shape = (8, 8)  # Shape must match the one used during embedding
check_watermark_in_video("output_with_watermark.mp4", watermark_shape, watermark)
