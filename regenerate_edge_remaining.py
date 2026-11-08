
import asyncio
import csv
import random
from pathlib import Path

import edge_tts

ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "edge_short_226.csv"
OUTPUT_DIR = ROOT / "outputs" / "edge-tts-regenerated"

VOICE = "vi-VN-HoaiMyNeural"

# 5 ID đã tạo lại ở lần thử trước
DONE_IDS = {2, 4, 5, 6, 7}

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    count = 0

    for row in rows:
        clip_id = int(row["id"])

        if clip_id in DONE_IDS:
            continue

        text = row["text"].strip()
        if not text:
            continue

        # Bổ sung câu tự nhiên để tránh clip quá ngắn
        text = (
            "Xin lưu ý. "
            + text
            + " Vui lòng chờ trong giây lát để hệ thống hoàn tất xử lý."
        )

        output_file = OUTPUT_DIR / f"edge_{clip_id:04d}.mp3"

        try:
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(str(output_file))
            count += 1
            print(f"Đã tạo: {output_file.name} ({count}/221)")

        except Exception as e:
            print(f"Lỗi ID {clip_id}: {e}")

        await asyncio.sleep(random.uniform(0.5, 1.5))

    print(f"\nHoàn thành: {count}/221 file")

if __name__ == "__main__":
    asyncio.run(main())
