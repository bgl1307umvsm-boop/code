
import csv
from pathlib import Path
import soundfile as sf

ROOT = Path(__file__).parent

METADATA_GOC = ROOT / "metadata_vieneu.csv"
THU_MUC_WAV = ROOT / "outputs" / "fake_voice_1000" / "vieneu-tts_16k"
METADATA_MOI = ROOT / "metadata_fake_bao_review.csv"

with open(METADATA_GOC, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    du_lieu_goc = list(reader)

# Ghép metadata với file WAV theo tên file
metadata_theo_ten = {
    Path(dong["file_name"]).name: dong
    for dong in du_lieu_goc
}

du_lieu = []

for file_wav in sorted(THU_MUC_WAV.glob("*.wav")):
    if file_wav.name.lower() == "test_vieneu.wav":
        continue

    dong_goc = metadata_theo_ten.get(file_wav.name)

    if dong_goc is None:
        print("Khong tim thay metadata:", file_wav.name)
        continue

    info = sf.info(file_wav)

    du_lieu.append({
        "clip_id": file_wav.stem.replace("vieneu_", ""),
        "path": file_wav.relative_to(ROOT).as_posix(),
        "text": dong_goc["text"],
        "speaker_id": "bao_speaker_01_UNVERIFIED",
        "source": "not_verified",
        "generator": "VieNeu-TTS",
        "channel": "mono",
        "duration": round(info.duration, 3),
        "split": "review_only"
    })

cot = [
    "clip_id",
    "path",
    "text",
    "speaker_id",
    "source",
    "generator",
    "channel",
    "duration",
    "split"
]

with open(METADATA_MOI, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=cot)
    writer.writeheader()
    writer.writerows(du_lieu)

print("Da tao:", METADATA_MOI.name)
print("So dong metadata:", len(du_lieu))
print("So cot:", len(cot))
print("Luu y: Day la metadata review, chua phai bo du lieu chinh thuc.")
