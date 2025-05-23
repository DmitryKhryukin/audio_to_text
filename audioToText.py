import os
import subprocess
import time
from pathlib import Path
from openai import OpenAI
import argparse
import logging

# --- Configure Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# --- CLI Arguments ---
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="Input .m4a or .mp3 file")
parser.add_argument("--output", required=False, help="Output .txt file")
args = parser.parse_args()

input_path = Path(args.input)
output_path = Path(args.output) if args.output else input_path.with_suffix(".txt")
chunk_dir = Path("chunks")
chunk_dir.mkdir(exist_ok=True)

# --- Init Client ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("Please set OPENAI_API_KEY in the environment.")
client = OpenAI(api_key=api_key)

# --- Detect audio length using ffprobe ---
def get_audio_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return float(result.stdout.strip())

# --- Split with ffmpeg ---
def split_audio(input_path: Path, chunk_duration_sec: int):
    duration = get_audio_duration(input_path)
    num_chunks = int(duration // chunk_duration_sec + 1)

    for i in range(num_chunks):
        start = i * chunk_duration_sec
        out_path = chunk_dir / f"chunk_{i}.m4a"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(input_path),
            "-ss", str(start),
            "-t", str(chunk_duration_sec),
            "-c:a", "aac", "-b:a", "128k",  # re-encode audio to AAC
            "-vn",  # no video
            str(out_path)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        yield out_path

# --- Main Transcription ---
start = time.time()
with open(output_path, "w", encoding="utf-8") as out_file:
    for i, chunk_path in enumerate(split_audio(input_path, 600)):
        logging.info(f"🎧 Processing chunk {i + 1}: {chunk_path.name}")
        with open(chunk_path, "rb") as audio_file:
            try:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                result = transcription.text.strip() if transcription and transcription.text else "[EMPTY TRANSCRIPTION]"
                out_file.write(result + "\n")
            except Exception as e:
                logging.error(f"❌ Error on chunk {i}: {e}")
                out_file.write(f"[ERROR]: {e}\n")
        os.remove(chunk_path)

logging.info(f"\n✅ Done: {output_path}")
logging.info(f"⏱ Execution time: {time.time() - start:.2f} sec")
