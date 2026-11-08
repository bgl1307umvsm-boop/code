
import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent

SENTENCE_FILE = ROOT / "data" / "sentences_1000.csv"
ORIGINAL_DIR = ROOT / "outputs" / "fake_voice_1000" / "edge-tts_16k"
REGENERATED_DIR = ROOT / "outputs" / "edge-tts-regenerated-16k"
REGENERATED_METADATA = ROOT / "metadata_edge_regenerated.csv"
OUTPUT_FILE = ROOT / "metadata_edge.csv"

FFPROBE = Path(
    r"C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.2-full_build-shared\bin\ffprobe.exe"
)


def get_duration(path):
    result = subprocess.run(
        [
            str(FFPROBE), "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path)
        ],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return None
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


with open(SENTENCE_FILE, encoding="utf-8-sig", newline="") as f:
    sentences = {
        int(row["id"]): row["text"].strip()
        for row in csv.DictReader(f)
    }

with open(REGENERATED_METADATA, encoding="utf-8-sig", newline="") as f:
    regenerated = {
        int(Path(row["file_name"]).stem.split("_")[-1]): row
        for row in csv.DictReader(f)
    }

rows = []
errors = []

for clip_id, text in sorted(sentences.items()):
    filename = f"edge_{clip_id:04d}.wav"

    # Ưu tiên WAV tạo lại nếu clip nằm trong danh sách 226 clip.
    if clip_id in regenerated:
        wav = REGENERATED_DIR / filename
        metadata_text = regenerated[clip_id]["text"]
    else:
        wav = ORIGINAL_DIR / filename
        metadata_text = text

    if not wav.exists():
        errors.append((filename, "Không tìm thấy file"))
        continue

    duration = get_duration(wav)

    if duration is None or not 3 <= duration <= 10:
        errors.append((filename, f"Thời lượng không hợp lệ: {duration}"))
        continue

    rows.append({
        "clip_id": f"edge_{clip_id:04d}",
        "path": wav.relative_to(ROOT).as_posix(),
        "label": "fake",
        "speaker_id": "unknown",
        "source": "TTS",
        "generator": "Edge-TTS",
        "channel": "wav_16k_mono_pcm16",
        "split": "review_only",
        "duration": round(duration, 3)
    })

fields = [
    "clip_id", "path", "label", "speaker_id",
    "source", "generator", "channel", "split", "duration"
]

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print("Số câu:", len(sentences))
print("Số dòng metadata đạt:", len(rows))
print("Số lỗi:", len(errors))
print("File xuất:", OUTPUT_FILE)

if errors:
    print("\nDanh sách lỗi:")
    for error in errors:
        print(error)
