from flask import Flask, render_template, request, send_file, send_from_directory
from audio_marking import embed_watermark, extract_watermark
from video_marking import watermark_video, detect_watermark
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


# Route to serve files from the uploads folder
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/embed", methods=["POST"])
def embed():
    print("Embed triggered")
    if "audio_file" not in request.files:
        return "No file uploaded", 400

    file = request.files["audio_file"]
    if file.filename == "":
        return "No file selected", 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, "watermarked_output")

    file.save(input_path)

    if file.filename.endswith(".mp3") or file.filename.endswith(".wav"):
        # Audio watermarking logic
        watermark = "This audio is created by VoiceCraft and is watermarked"
        embed_watermark(input_path, watermark, output_path + ".wav")
        audio_file = "watermarked_output.wav"
    elif file.filename.endswith(".mp4") or file.filename.endswith(".mov"):
        # Video watermarking logic
        watermark_video(input_path, output_path + ".mp4")

        audio_file = "watermarked_output.mp4"
    else:
        return "Unsupported file type", 400

    print(audio_file)
    return render_template("index.html", audio_file=audio_file)


@app.route("/check_watermark")
def check_watermark():
    return render_template("check_watermark.html")


@app.route("/extract", methods=["POST"])
def extract():
    if "audio_file" not in request.files:
        return "No file uploaded", 400

    file = request.files["audio_file"]
    if file.filename == "":
        return "No file selected", 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Check the file type
    if file.mimetype.startswith("audio"):
        watermark_length = len("This audio is created by VoiceCraft and is watermarked")
        extracted_watermark = extract_watermark(input_path, watermark_length)

    elif file.mimetype.startswith("video"):
        status = detect_watermark(input_path, 20)
        if status == True:
            extracted_watermark = (
                "This audio is created by VoiceCraft and is watermarked"
            )
        else:
            extracted_watermark = "Could not find any hidden watermark"
        # Video extraction logic will go here
        # Placeholder for video watermark extraction logic

    else:
        return "Unsupported file type", 400

    return render_template(
        "check_watermark.html", extracted_watermark=extracted_watermark
    )


if __name__ == "__main__":
    app.run()
