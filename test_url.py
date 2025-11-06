import whisper

# Test mit einer URL
model = whisper.load_model("tiny")

# Beispiel URL (du kannst hier eine echte Audio-URL einsetzen)
url = "https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav"

print("Downloading and transcribing from URL...")
result = model.transcribe(url)

print(f"\nText: {result['text']}")
print(f"Language: {result['language']}")
