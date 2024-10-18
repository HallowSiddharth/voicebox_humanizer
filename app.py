from flask import Flask, render_template, request, send_file
from audio_marking import embed_watermark, extract_watermark
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/embed", methods=["POST"])
def embed():
    if "audio_file" not in request.files:
        return "No file uploaded", 400

    file = request.files["audio_file"]
    if file.filename == "":
        return "No file selected", 400

    # watermark = request.form["watermark"]
    watermark = "This audio is created by VoiceCraft and is watermarked"
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, "watermarked_output.wav")

    file.save(input_path)
    embed_watermark(input_path, watermark, output_path)

    return render_template("index.html", audio_file="watermarked_output.wav")


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

    # watermark_length = int(request.form["watermark_length"])
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(input_path)
    watermark_length = len("This audio is created by VoiceCraft and is watermarked")
    extracted_watermark = extract_watermark(input_path, watermark_length)

    return render_template(
        "check_watermark.html", extracted_watermark=extracted_watermark
    )


if __name__ == "__main__":
    app.run(debug=True)
