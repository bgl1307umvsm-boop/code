import csv
from pathlib import Path

ROOT = Path(__file__).parent

with open(ROOT / "edge_short_226.csv", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    if int(row["id"]) == 87:
        print("Nội dung câu ID 87:")
        print(row["text"])

mp3 = ROOT / "outputs" / "edge-tts-regenerated" / "edge_0087.mp3"

print("\nFile tồn tại:", mp3.exists())

if mp3.exists():
    print("Dung lượng:", mp3.stat().st_size, "bytes")