import wave
from pathlib import Path
from collections import Counter

folder = Path("outputs/fake_voice_1000/f5-tts")
files = sorted(folder.glob("*.wav"))

formats = Counter()
errors = []

for p in files:
    try:
        with wave.open(str(p), "rb") as w:
            info = (w.getframerate(), w.getnchannels(), w.getsampwidth())
            duration = w.getnframes() / w.getframerate()
            formats[info] += 1

            if not (3 <= duration <= 10):
                errors.append((p.name, round(duration, 2), "Sai thời lượng"))
    except Exception as e:
        errors.append((p.name, str(e), "Lỗi đọc WAV"))

print("Tổng file:", len(files))
print("Định dạng (sample rate, channels, sample width):", formats)
print("Số lỗi:", len(errors))
for item in errors[:20]:
    print(item)
