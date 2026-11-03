
import csv
import wave
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "data" / "metadata_fake.csv"

COLUMNS = [
    "clip_id", "path", "label", "speaker_id",
    "source", "generator", "channel", "split", "duration"
]

def wav_info(path):
    with wave.open(str(path), "rb") as wav:
        duration = wav.getnframes() / wav.getframerate()
        rate = wav.getframerate()
        channels = wav.getnchannels()
        width = wav.getsampwidth()

    channel = f"wav_{rate}hz_{channels}ch_{width * 8}bit"
    return round(duration, 3), channel

rows = []
missing = []

def add_clip(clip_id, relative_path, generator, speaker_id="unknown"):
    path = ROOT / relative_path

    if not path.is_file():
        missing.append(str(relative_path))
        return

    duration, channel = wav_info(path)

    rows.append({
        "clip_id": clip_id,
        "path": relative_path.replace("\\", "/"),
        "label": "fake",
        "speaker_id": speaker_id,
        "source": "TTS",
        "generator": generator,
        "channel": channel,
        "split": "review_only",
        "duration": duration
    })

# 1. VieNeu-TTS
with open(ROOT / "metadata_fake.csv", encoding="utf-8-sig") as f:
    for item in csv.DictReader(f):
        add_clip(
            item["file_name"],
            item["file_name"],
            "VieNeu-TTS",
            item.get("speaker") or "unknown"
        )

# 2. Edge-TTS
with open(ROOT / "metadata_edge.csv", encoding="utf-8-sig") as f:
    for item in csv.DictReader(f):
        add_clip(
            item["clip_id"],
            item["path"],
            "Edge-TTS",
            item.get("speaker_id") or "unknown"
        )

# 3. viXTTS - dÃ¹ng thÆ° má»¥c WAV 16 kHz
with open(ROOT / "metadata_vixtts.csv", encoding="utf-8-sig") as f:
    for item in csv.DictReader(f):
        filename = item["file_name"]
        relative_path = f"outputs/fake_voice_1000/vixtts_16k/{filename}"

        add_clip(
            f"vixtts_{int(item['id']):04d}",
            relative_path,
            "viXTTS"
        )

# 4. F5-TTS
f5_metadata = ROOT / "outputs/fake_voice_1000/f5-tts/metadata_f5.csv"

with open(f5_metadata, encoding="utf-8-sig") as f:
    for item in csv.DictReader(f):
        if item["status"].strip().lower() != "success":
            continue

        filename = item["filename"]
        relative_path = f"outputs/fake_voice_1000/f5-tts_16k/{filename}"

        add_clip(
            Path(filename).stem,
            relative_path,
            "F5-TTS"
        )

# KhÃ´ng táº¡o file náº¿u cÃ²n thiáº¿u WAV
if missing:
    print("CÃ“ WAV Bá»Š THIáº¾U:")
    for path in missing[:20]:
        print("-", path)
    raise SystemExit("Dá»«ng: cáº§n xá»­ lÃ½ Ä‘Æ°á»ng dáº«n thiáº¿u trÆ°á»›c.")

# Kiá»ƒm tra ID trÃ¹ng
ids = [row["clip_id"] for row in rows]
if len(ids) != len(set(ids)):
    raise SystemExit("CÃ³ clip_id bá»‹ trÃ¹ng!")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Sao lÆ°u file cÅ© náº¿u cÃ³
if OUTPUT.exists():
    backup = OUTPUT.with_name(
        f"metadata_fake_backup_{datetime.now():%Y%m%d_%H%M%S}.csv"
    )
    OUTPUT.replace(backup)
    print("ÄÃ£ sao lÆ°u file cÅ©:", backup)

with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(rows)

print("\nHOÃ€N Táº¤T Gá»˜P METADATA")
print("Tá»•ng sá»‘ dÃ²ng:", len(rows))
print("VieNeu-TTS:", sum(r["generator"] == "VieNeu-TTS" for r in rows))
print("Edge-TTS:", sum(r["generator"] == "Edge-TTS" for r in rows))
print("viXTTS:", sum(r["generator"] == "viXTTS" for r in rows))
print("F5-TTS:", sum(r["generator"] == "F5-TTS" for r in rows))
print("File:", OUTPUT)

