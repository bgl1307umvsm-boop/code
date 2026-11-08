
from pathlib import Path
import soundfile as sf
import numpy as np
from scipy.signal import resample_poly
from math import gcd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "outputs" / "vieneu-tts"
OUTPUT = ROOT / "outputs" / "vieneu-tts-16k"

OUTPUT.mkdir(parents=True, exist_ok=True)

files = sorted(SOURCE.glob("*.wav"))
success = 0
errors = []

for file in files:
    try:
        audio, sr = sf.read(file, dtype="float32")

        if audio.ndim == 2:
            audio = audio.mean(axis=1)

        if sr != 16000:
            g = gcd(sr, 16000)
            audio = resample_poly(audio, 16000 // g, sr // g)

        if not np.isfinite(audio).all():
            raise ValueError("Audio co NaN hoac vo cuc")

        target = OUTPUT / file.name
        sf.write(target, audio, 16000, subtype="PCM_16")

        success += 1

    except Exception as e:
        errors.append(f"{file.name}: {e}")

print("Tong file:", len(files))
print("Chuan hoa thanh cong:", success)
print("So loi:", len(errors))

if errors:
    (OUTPUT / "errors.txt").write_text(
        "\n".join(errors), encoding="utf-8"
    )
