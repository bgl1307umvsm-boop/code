
import asyncio
import edge_tts
from pathlib import Path

async def main():
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    text = "Xin chào. Đây là đoạn giọng nói tiếng Việt được tạo bằng trí tuệ nhân tạo."
    output_file = output_dir / "fake_edge_001.mp3"

    communicate = edge_tts.Communicate(
        text,
        voice="vi-VN-HoaiMyNeural"
    )

    await communicate.save(str(output_file))
    print(f"Đã tạo file: {output_file.resolve()}")

asyncio.run(main())
