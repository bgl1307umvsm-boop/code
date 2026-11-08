
import csv
from pathlib import Path

ROOT = Path(__file__).parent
CSV_FILE = ROOT / "metadata_edge_regenerated.csv"

with open(CSV_FILE, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print("Tổng dòng metadata:", len(rows))

missing = []
bad_duration = []

for row in rows:
    wav = ROOT / row["file_name"]

    if not wav.exists():
        missing.append(row["file_name"])

    duration = float(row["duration"])
    if not 3 <= duration <= 10:
        bad_duration.append((row["file_name"], duration))

print("File WAV bị thiếu:", len(missing))
print("File sai thời lượng:", len(bad_duration))
print("Speaker:", set(row["speaker"] for row in rows))
print("Split:", set(row["split"] for row in rows))

if missing:
    print("Danh sách file thiếu:", missing)

if bad_duration:
    print("Danh sách file sai thời lượng:", bad_duration)
