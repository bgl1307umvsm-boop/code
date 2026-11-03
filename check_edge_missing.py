import csv
from pathlib import Path

ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "edge_short_226.csv"
OUTPUT_DIR = ROOT / "outputs" / "edge-tts-regenerated"

with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

missing = []

for row in rows:
    clip_id = int(row["id"])

    if clip_id in {2, 4, 5, 6, 7}:
        continue

    filename = f"edge_{clip_id:04d}.mp3"

    if not (OUTPUT_DIR / filename).exists():
        missing.append(clip_id)

print("Số file còn thiếu:", len(missing))
print("Danh sách ID thiếu:", missing)