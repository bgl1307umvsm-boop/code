import asyncio
import csv
from pathlib import Path
import edge_tts

ROOT = Path.cwd()
INPUT = ROOT / "data" / "sentences_1000_fixed.csv"
OUTPUT = ROOT / "outputs" / "fake_voice_1000" / "edge-tts" / "edge_0768.mp3"

async def main():
    with open(INPUT, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    row = next(r for r in rows if str(r["id"]).strip() == "768")
    text = row["text"].strip()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    await edge_tts.Communicate(text, "vi-VN-HoaiMyNeural").save(str(OUTPUT))

    print("Đã tạo:", OUTPUT)
    print("Nội dung:", text)
    print("Dung lượng:", OUTPUT.stat().st_size, "bytes")

asyncio.run(main())
