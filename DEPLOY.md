# Whisper API - Railway Deployment Guide

## 🚀 Quick Deploy to Railway

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add Railway API support"
   git push
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select this repository
   - Railway will automatically detect the Dockerfile and deploy!

3. **Set Environment Variables** (Optional):
   - `WHISPER_MODEL` - Model size: `tiny`, `base`, `small`, `medium`, `large`, `turbo` (default: `base`)
   - Railway automatically sets `PORT`

## 📡 API Endpoints

### Health Check
```bash
GET /
GET /health
```

### Transcribe Audio from URL
```bash
POST /transcribe
Content-Type: application/json

{
  "url": "https://example.com/audio.mp3",
  "language": "en",  # Optional: "en", "de", "fr", etc.
  "task": "transcribe",  # or "translate" (to English)
  "word_timestamps": false,
  "temperature": 0.0
}
```

**Response:**
```json
{
  "text": "The transcribed text...",
  "language": "en",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 5.2,
      "text": " Hello world",
      "tokens": [...],
      "temperature": 0.0,
      "avg_logprob": -0.25,
      "compression_ratio": 1.5,
      "no_speech_prob": 0.01
    }
  ]
}
```

## 🧪 Test Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

2. **Run the API**:
   ```bash
   python api.py
   ```

3. **Test with cURL**:
   ```bash
   curl -X POST http://localhost:8000/transcribe \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav"}'
   ```

## 📊 Model Sizes & Memory Requirements

| Model  | Parameters | VRAM Required | Speed  | Quality |
|--------|-----------|---------------|--------|---------|
| tiny   | 39M       | ~1 GB         | ~10x   | Basic   |
| base   | 74M       | ~1 GB         | ~7x    | Good    |
| small  | 244M      | ~2 GB         | ~4x    | Better  |
| medium | 769M      | ~5 GB         | ~2x    | Great   |
| large  | 1550M     | ~10 GB        | 1x     | Best    |
| turbo  | 809M      | ~6 GB         | ~8x    | Best    |

**Recommendation for Railway**: Start with `base` or `small` for faster cold starts.

## 🔧 Configuration

Set `WHISPER_MODEL` environment variable in Railway:
- `tiny` - Fastest, lowest accuracy
- `base` - **Default** - Good balance
- `small` - Better accuracy
- `medium` - High accuracy, slower
- `large` - Best accuracy, very slow
- `turbo` - Fast & accurate (recommended for production)

## 📝 Example Usage

### JavaScript/Fetch
```javascript
const response = await fetch('https://your-app.railway.app/transcribe', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    url: 'https://example.com/audio.mp3',
    language: 'en'
  })
});

const result = await response.json();
console.log(result.text);
```

### Python
```python
import requests

response = requests.post('https://your-app.railway.app/transcribe', json={
    'url': 'https://example.com/audio.mp3',
    'language': 'en'
})

result = response.json()
print(result['text'])
```

## 🛠️ Files Overview

- `api.py` - FastAPI server with transcription endpoint
- `Dockerfile` - Container configuration for Railway
- `railway.json` - Railway deployment configuration
- `requirements.txt` - Python dependencies (updated with API deps)
- `whisper/transcribe.py` - Modified to support URL downloads
- `.dockerignore` - Files to exclude from Docker build

## ⚡ Performance Tips

1. **Use smaller models for faster response** (`base` or `small`)
2. **Set language explicitly** to skip auto-detection
3. **Disable word_timestamps** if not needed (faster processing)
4. **Use turbo model** for production (best speed/quality trade-off)

## 🔗 Supported Audio Formats

Via FFmpeg: MP3, WAV, FLAC, M4A, OGG, MP4, WebM, and more!

## 📚 API Documentation

Once deployed, visit:
- `https://your-app.railway.app/docs` - Interactive API documentation (Swagger UI)
- `https://your-app.railway.app/redoc` - Alternative documentation (ReDoc)

---

**Built with**: OpenAI Whisper + FastAPI + Railway 🚀
