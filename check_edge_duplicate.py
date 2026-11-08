import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
CSV_FILE = ROOT / "metadata_edge.csv"

with open(CSV_FILE, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

clip_ids = [row["clip_id"] for row in rows]
paths = [row["path"] for row in rows]

duplicate_ids = [
    key for key, count in Counter(clip_ids).items()
    if count > 1
]

duplicate_paths = [
    key for key, count in Counter(paths).items()
    if count > 1
]

print("Tổng dòng:", len(rows))
print("Số ID trùng:", len(duplicate_ids))
print("Số đường dẫn trùng:", len(duplicate_paths))

if duplicate_ids:
    print("ID trùng:", duplicate_ids)

if duplicate_paths:
    print("Đường dẫn trùng:", duplicate_paths)