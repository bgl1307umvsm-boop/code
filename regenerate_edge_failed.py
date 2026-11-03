
import asyncio
import csv
import random
from pathlib import Path

import edge_tts

ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "edge_short_226.csv"
OUTPUT_DIR = ROOT / "outputs" / "edge-tts-regenerated"

VOICE = "vi-VN-HoaiMyNeural"
FAILED_IDS = {87, 106, 146, 188, 225, 253, 523, 608}

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    success = 0
    failed = []

    for row in rows:
        clip_id = int(row["id"])

        if clip_id not in FAILED_IDS:
            continue

        text = row["text"].strip()
        if not text:
            failed.append(clip_id)
            continue

        text = (
            "Xin lưu ý. " + text
            + " Vui lòng chờ trong giây lát để hệ thống hoàn tất xử lý."
        )

        output_file = OUTPUT_DIR / f"edge_{clip_id:04d}.mp3"

        for attempt in range(1, 4):
            try:
                communicate = edge_tts.Communicate(text, VOICE)
                await communicate.save(str(output_file))

                if output_file.exists() and output_file.stat().st_size > 0:
                    success += 1
                    print(f"Đã tạo lại: {output_file.name}")
                    break

            except Exception as e:
                print(f"Lỗi ID {clip_id}, lần {attempt}: {e}")

            if output_file.exists():
                output_file.unlink()

            await asyncio.sleep(attempt * 2)

        else:
            failed.append(clip_id)

        await asyncio.sleep(random.uniform(3, 5))

    print("\n===== KẾT QUẢ =====")
    print("Tạo lại thành công:", success)
    print("Còn lỗi:", len(failed))
    print("ID còn lỗi:", failed)

if __name__ == "__main__":
    asyncio.run(main())
