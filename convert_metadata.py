import csv
from pathlib import Path
import soundfile as sf

ROOT = Path(__file__).resolve().parent
SENTENCES = ROOT / "data" / "sentences_1000.csv"
AUDIO_DIR = ROOT / "outputs" / "fake_voice_1000" / "vieneu-tts"
OUTPUT = ROOT / "outputs" / "fake_voice_1000" / "vieneu-tts" / "metadata_vieneu.csv"

metadata = []
errors = []

with open(SENTENCES, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    filename = f"vieneu_{int(row['id']):04d}.wav"
    audio_path = AUDIO_DIR / filename

    try:
        if not audio_path.exists():
            raise FileNotFoundError(f"Khong tim thay: {audio_path}")

        sf.info(str(audio_path))

        metadata.append({
    "filename": filename,
    "path": audio_path.relative_to(ROOT).as_posix(),
    "text": row["text"],
    "model": "VieNeu-TTS",
    "status": "success"
})

    except Exception as e:
        errors.append(f"{filename}: {e}")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["filename", "path", "text", "model", "status"]
    )
    writer.writeheader()
    writer.writerows(metadata)

print("Tong so cau:", len(rows))
print("Metadata thanh cong:", len(metadata))
print("So loi:", len(errors))
print("Metadata:", OUTPUT)

if errors:
    (ROOT / "metadata_vieneu_errors.txt").write_text(
        "\n".join(errors), encoding="utf-8"
    )