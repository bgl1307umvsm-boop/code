
import asyncio
import csv
import random
from pathlib import Path

import edge_tts

ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "data" / "sentences_1000.csv"
OUTPUT_DIR = ROOT / "outputs" / "edge-tts"
METADATA_FILE = ROOT / "metadata_fake.csv"

VOICE = "vi-VN-HoaiMyNeural"
MAX_RETRIES = 3


async def generate_one(text, output_file):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(str(output_file))

            if output_file.exists() and output_file.stat().st_size > 0:
                return True

        except Exception as e:
            print(
                f"Lỗi {output_file.name}, "
                f"lần {attempt}/{MAX_RETRIES}: {e}"
            )

        if output_file.exists():
            output_file.unlink()

        await asyncio.sleep(attempt * 2 + random.random())

    return False


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
        sentences = list(csv.DictReader(f))

    metadata = []

    for item in sentences:
        clip_id = int(item["id"])
        text = item["text"].strip()

        if not text:
            continue

        filename = f"edge_{clip_id:04d}.mp3"
        output_file = OUTPUT_DIR / filename

        if output_file.exists() and output_file.stat().st_size > 0:
            success = True
            print(f"Đã có: {filename}")
        else:
            success = await generate_one(text, output_file)

        if success:
            metadata.append({
                "file_name": str(output_file.relative_to(ROOT)),
                "text": text,
                "tool": "edge-tts",
                "label": "fake",
                "language": "vi",
                "sample_rate": "",
                "status": "success",
            })
            print(f"Tiến độ: {len(metadata)}/{len(sentences)}")

    with open(
        METADATA_FILE, "w", encoding="utf-8-sig", newline=""
    ) as f:
        fields = [
            "file_name", "text", "tool", "label",
            "language", "sample_rate", "status"
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(metadata)

    print(f"\nHoàn thành: {len(metadata)}/{len(sentences)} clip")
    print(f"Metadata: {METADATA_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
