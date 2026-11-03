
from pathlib import Path
import soundfile as sf
import numpy as np

ROOT = Path(__file__).parent

files = [
    ROOT / "outputs" / "vieneu-tts" / "vieneu_0001.wav",
    ROOT / "outputs" / "fake_voice_1000" / "vieneu-tts_16k" / "vieneu_0001.wav",
]

for path in files:
    print("\n------------------------------")
    print("File:", path)

    if not path.exists():
        print("KHONG TIM THAY FILE")
        continue

    info = sf.info(path)
    audio, sr = sf.read(path)

    print("Sample rate:", sr)
    print("So kenh:", info.channels)
    print("Thoi luong:", round(info.duration, 2), "giay")
    print("So mau am thanh:", len(audio))

    print("Gia tri lon nhat:", round(float(np.max(np.abs(audio))), 4))
    print("Am thanh co bi im lang hoan toan:", bool(np.max(np.abs(audio)) == 0))

print("\nDa kiem tra xong.")
