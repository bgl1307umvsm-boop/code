import asyncio
import csv
import random
from pathlib import Path

import edge_tts

ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "edge_short_226.csv"
OUTPUT_DIR = ROOT / "outputs" / "edge-tts-regenerated"

VOICE = "vi-VN-HoaiMyNeural"

# Câu được viết dài hơn nhưng giữ nguyên ý nghĩa
EXTRA = {
    2: "Thông tin này đã được hệ thống ghi nhận thành công. Bạn vui lòng chờ trong giây lát nhé.",
    4: "Nội dung đăng ký của bạn đã được hệ thống ghi nhận thành công. Vui lòng chờ để tiếp tục xử lý.",
    5: "Thông tin liên hệ của bạn đã được ghi nhận đầy đủ. Bạn vui lòng chờ trong giây lát nhé.",
    6: "Yêu cầu hỗ trợ của bạn đã được tiếp nhận và ghi nhận thành công. Chúng tôi sẽ tiếp tục xử lý.",
    7: "Dữ liệu bạn vừa gửi đã được hệ thống ghi nhận thành công. Vui lòng chờ trong giây lát.",
}

# Các ID còn lại tạm thời giữ nguyên để bổ sung câu sau khi rà soát.
async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    print("Tổng số câu:", len(rows))

    for row in rows:
        clip_id = int(row["id"])
        if clip_id not in EXTRA:
            continue

        text = EXTRA[clip_id]
        output_file = OUTPUT_DIR / f"edge_{clip_id:04d}.mp3"

        try:
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(str(output_file))
            print("Đã tạo:", output_file.name)
        except Exception as e:
            print("Lỗi ID", clip_id, ":", e)

        await asyncio.sleep(random.uniform(0.5, 1.5))

    print("Hoàn thành nhóm ID 2, 4, 5, 6, 7.")

if __name__ == "__main__":
    asyncio.run(main())