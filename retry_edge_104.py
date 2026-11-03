
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "outputs" / "edge-tts-regenerated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    text = (
        "Bạn đã ghi nhận đăng ký thành công. "
        "Vui lòng chờ hệ thống xử lý."
    )

    output_file = OUTPUT_DIR / "edge_0104.mp3"

    communicate = edge_tts.Communicate(
        text, "vi-VN-HoaiMyNeural"
    )
    await communicate.save(str(output_file))

    print("Tạo thành công:", output_file.exists())
    print("Nội dung mới:", text)

asyncio.run(main())
