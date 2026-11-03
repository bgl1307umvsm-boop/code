import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent

FFPROBE = Path(
    r"C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.2-full_build-shared\bin\ffprobe.exe"
)

WAV_DIR = ROOT / "outputs" / "fake_voice_1000" / "edge-tts_16k"
CSV_FILE = ROOT / "data" / "sentences_1000.csv"

with open(CSV_FILE, encoding="utf-8-sig", newline="") as f:
    sentences = {int(r["id"]): r["text"] for r in csv.DictReader(f)}

short = []

for wav in sorted(WAV_DIR.glob("edge_*.wav")):
    result = subprocess.run([
        str(FFPROBE), "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json", str(wav)
    ], capture_output=True, text=True)

    duration = float(json.loads(result.stdout)["format"]["duration"])

    if duration < 3:
        clip_id = int(wav.stem.split("_")[1])
        short.append({
            "id": clip_id,
            "duration": round(duration, 3),
            "text": sentences.get(clip_id, "Không tìm thấy câu")
        })

with open("edge_short_226.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "duration", "text"])
    writer.writeheader()
    writer.writerows(short)

print("Số câu dưới 3 giây:", len(short))
print("Đã lưu danh sách: edge_short_226.csv")