
import csv
from collections import Counter
from pathlib import Path

file = Path("metadata_fake.csv")

with open(file, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print("Tổng số dòng:", len(rows))
print("\nSố lượng theo công cụ:")

for tool, count in Counter(row["tool"] for row in rows).items():
    print(tool, ":", count)
