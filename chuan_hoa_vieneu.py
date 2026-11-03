
import os
import soundfile as sf
import numpy as np
from scipy.signal import resample_poly
from math import gcd

source = r"C:\LE_GIA_BA0\Task2_SinhGiongGia\outputs\vieneu-tts"
target = r"C:\LE_GIA_BA0\Task2_SinhGiongGia\outputs\vieneu-tts_16k"

os.makedirs(target, exist_ok=True)

thanh_cong = 0
loi = 0
bo_qua = 0

for name in os.listdir(source):
    if not name.lower().endswith(".wav"):
        continue

    src = os.path.join(source, name)

    try:
        audio, sr = sf.read(src, dtype="float32", always_2d=True)

        # Chuyen stereo thanh mono neu can
        audio = np.mean(audio, axis=1)

        # Doi tan so lay mau sang 16 kHz
        if sr != 16000:
            g = gcd(sr, 16000)
            audio = resample_poly(
                audio, 16000 // g, sr // g
            )

        duration = len(audio) / 16000

        # Chi giu clip dai tu 3 den 10 giay
        if duration < 3 or duration > 10:
            bo_qua += 1
            continue

        dst = os.path.join(target, name)
        sf.write(dst, audio, 16000, subtype="PCM_16")

        thanh_cong += 1

    except Exception as e:
        print("Loi:", name, e)
        loi += 1

print("Chuan hoa thanh cong:", thanh_cong)
print("Bo qua do sai thoi luong:", bo_qua)
print("File gap loi:", loi)
print("Thu muc dau ra:", target)
