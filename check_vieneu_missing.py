import csv
from pathlib import Path

ROOT = Path(__file__).parent
CSV_FILE = ROOT / "metadata_fake.csv"

with open(CSV_FILE, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

ids = set()

for row in rows:
    filename = Path(row["file_name"]).stem
    if filename.startswith("vieneu_"):
        ids.add(int(filename.split("_")[-1]))

missing = sorted(set(range(1, 1001)) - ids)

print("Tổng clip có metadata:", len(ids))
print("Số ID còn thiếu:", len(missing))
print("ID còn thiếu:", missing)