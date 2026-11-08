import csv
from pathlib import Path

import soundfile as sf
from vieneu import Vieneu

ROOT = Path(__file__).resolve().parent
INPUT_FILE = ROOT / "data" / "sentences_1000.csv"
OUTPUT_DIR = ROOT / "outputs" / "vieneu-tts"
METADATA_FILE = ROOT / "metadata_vieneu.csv"
ERROR_FILE = ROOT / "errors_vieneu.txt"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Khong tim thay: {INPUT_FILE}")

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    sentences = list(csv.DictReader(f))

if not sentences:
    raise ValueError("File CSV khong co du lieu.")

if not {"id", "text"}.issubset(sentences[0].keys()):
    raise ValueError("CSV can co hai cot id va text.")

# Khoi tao mo hinh VieNeu-TTS
model = Vieneu()

# Metadata dung 9 cot theo yeu cau
fields = [
    "clip_id",
    "path",
    "speaker_id",
    "source",
    "generator",
    "channel",
    "duration",
    "label",
    "split",
]

metadata = []
errors = []

# Chi tao lai hai file nay
REGENERATE_IDS = {104, 131}

for index, item in enumerate(sentences, start=1):
    try:
        clip_id = int(item["id"])
        text = item["text"].strip()

        if not text:
            raise ValueError("Van ban rong.")

        output_file = OUTPUT_DIR / f"vieneu_{clip_id:04d}.wav"

        # Tao lai ID 104 va 131.
        # Cac file khac chi tao neu chua co hoac file rong.
        if (
            clip_id in REGENERATE_IDS
            or not output_file.exists()
            or output_file.stat().st_size == 0
        ):
            audio = model.infer(text)
            sf.write(
                str(output_file),
                audio,
                48000,
                subtype="PCM_16",
            )

        info = sf.info(str(output_file))

        metadata.append({
            "clip_id": output_file.stem,
            "path": output_file.relative_to(ROOT).as_posix(),
            "speaker_id": "unknown",
            "source": "synthetic",
            "generator": "VieNeu-TTS",
            "channel": "mono" if info.channels == 1 else f"{info.channels}_channels",
            "duration": round(info.duration, 3),
            "label": "fake",
            "split": "review_only",
        })

        print(f"Tien do: {index}/{len(sentences)}")

    except Exception as e:
        errors.append(
            f"Dong {index}, ID {item.get('id', '')}: {e}"
        )
        print(f"Loi dong {index}: {e}")

# Ghi lai metadata
with open(METADATA_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(metadata)

# Ghi cac loi neu co
ERROR_FILE.write_text("\n".join(errors), encoding="utf-8")

print("\nDa xu ly xong.")
print(f"Tong cau: {len(sentences)}")
print(f"Metadata tao duoc: {len(metadata)}")
print(f"So loi: {len(errors)}")
print(f"Metadata: {METADATA_FILE}")
print(f"File loi: {ERROR_FILE}")

