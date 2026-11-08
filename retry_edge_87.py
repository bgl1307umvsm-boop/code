import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "outputs" / "edge-tts-regenerated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    text = None

    import csv
    with open(ROOT / "edge_short_226.csv", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if int(row["id"]) == 87:
                text = row["text"].strip()
                break

    if not text:
        print("Không tìm thấy câu ID 87")
        return

    text = (
        "Xin lưu ý. " + text
        + " Vui lòng chờ trong giây lát để hệ thống hoàn tất xử lý."
    )

    output_file = OUTPUT_DIR / "edge_0087.mp3"

    try:
        communicate = edge_tts.Communicate(text, "vi-VN-HoaiMyNeural")
        await communicate.save(str(output_file))

        print("Tạo thành công:", output_file.exists())
        if output_file.exists():
            print("Dung lượng:", output_file.stat().st_size, "bytes")

    except Exception as e:
        print("Lỗi:", repr(e))

asyncio.run(main())