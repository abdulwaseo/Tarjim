# Tarjim · ترجم
### Arabic → English Real-Time Voice Translator

A real-time voice translation web app powered by [Deepgram's Voice Agent API](https://deepgram.com/product/voice-agent-api). Speak Arabic — hear and read the English translation instantly.

---

## How It Works

1. Browser captures your Arabic speech via microphone
2. Audio streams to the FastAPI backend via WebSocket
3. Backend proxies audio to Deepgram Voice Agent API
4. Deepgram transcribes Arabic → GPT translates → Deepgram speaks English
5. Translation text and audio stream back to the browser in real time

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vanilla HTML/CSS/JS |
| Backend | FastAPI + Uvicorn |
| Voice Agent | Deepgram Voice Agent API |
| STT | Deepgram Nova-3 (Arabic) |
| LLM | OpenAI GPT-4o |
| TTS | Deepgram Aura-2 Thalia |

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/tarjim.git
cd tarjim
```

### 2. Install Python dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Add your Deepgram API key
```bash
cp .env.example .env
# Edit .env and add your key
```

Or create `.env` manually:
```
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

Get a free API key at [console.deepgram.com](https://console.deepgram.com)

### 4. Run the app
```bash
./run.sh
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Project Structure

```
tarjim/
├── main.html        # Frontend UI
├── server.py        # FastAPI backend + WebSocket proxy
├── run.sh           # Startup script
├── requirements.txt # Python dependencies
├── .env             # API key (never committed to Git)
├── .env.example     # Safe template for .env
└── .gitignore       # Git ignore rules
```

---

## Requirements

- Python 3.10+
- macOS / Linux / Windows (WSL)
- A Deepgram account with Voice Agent API access
- A modern browser (Chrome or Safari)
- Microphone access

---

## Notes

- Make sure no other app (e.g. Microsoft Teams) is hijacking your microphone input
- Voice Agent API is billed at $4.50/hr by Deepgram
- The `.env` file is gitignored — never commit your API key

---

## License

MIT