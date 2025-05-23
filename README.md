# 🎙️ Audio to Text Transcription (OpenAI Whisper + ffmpeg)

This script transcribes large `.m4a` or `.mp3` audio files using OpenAI Whisper (`whisper-1`) via the OpenAI API.  
It splits the input audio into 10-minute chunks using `ffmpeg`.

---

## ✅ Features

- Splits large audio files into 10-minute chunks using `ffmpeg`
- Transcribes each chunk using OpenAI's Whisper model
- Appends all text into a single output `.txt` file
- Minimal dependencies, no use of deprecated Python libraries

---

## 🛠️ Requirements

- Python **3.11+**
- `ffmpeg` installed and available in your PATH
- An OpenAI API key

---

## 📦 Setup Instructions

### 1. Clone and create a virtual environment

```bash
git clone git@github.com:DmitryKhryukin/audio_to_text.git
cd audio_to_text

python3 -m venv venv
source venv/bin/activate
pip install openai
```

### 2. Install ffmpeg

#### macOS (Homebrew):
```bash
brew install ffmpeg
```
---

## 🔐 Set your OpenAI API key

```bash
export OPENAI_API_KEY="your-api-key-here"
```

---

## ▶️ How to Use

```bash
python audioToText.py --input /path/to/audio.m4a --output /path/to/output.txt
```

- `--input`: Required. Path to the input audio file (`.m4a` or `.mp3`)
- `--output`: Optional. Path to save the resulting `.txt`. Defaults to same name as input.

---

## 📁 Output

- All text is saved to the output file (`.txt`)

