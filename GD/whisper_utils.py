import whisper

model = whisper.load_model("base")

def transcribe_audio_file(file_path):
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        return f"Error in transcription: {str(e)}"
