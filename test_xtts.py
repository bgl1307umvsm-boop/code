import os
import psutil
from pathlib import Path

os.environ["TEMP"] = r"D:\Temp"
os.environ["TMP"] = r"D:\Temp"
os.environ["TTS_HOME"] = r"D:\XTTS_Models"

model_dir = Path(
    r"D:\XTTS_Models\tts\tts_models--multilingual--multi-dataset--xtts_v2"
)

print("Đang kiểm tra model...")

for name in ["config.json", "model.pth", "vocab.json", "speakers_xtts.pth"]:
    file = model_dir / name
    print(name, "OK" if file.exists() else "THIẾU")

print("RAM còn trống:", round(
    psutil.virtual_memory().available / 1024**3, 2
), "GB")

print("Kiểm tra hoàn tất.")