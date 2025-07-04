from flask import Flask, request, jsonify
import whisper
import tempfile
import os

app = Flask(__name__)

# Gunakan model "tiny" agar cocok dengan memori gratisan Render
model = whisper.load_model("tiny")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    audio = request.files["file"]
    if audio.filename == "":
        return jsonify({"error": "No selected file"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        audio.save(tmp.name)
        try:
            result = model.transcribe(tmp.name)
            return jsonify({"text": result["text"]})
        finally:
            os.remove(tmp.name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
