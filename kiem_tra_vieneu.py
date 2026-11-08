
import os
import soundfile as sf

folder = r"C:\LE_GIA_BA0\Task2_SinhGiongGia\outputs\vieneu-tts"

total = 0
loi = 0
sai_mau = 0
sai_kenh = 0
sai_thoi_luong = 0

for name in os.listdir(folder):
    if not name.lower().endswith(".wav"):
        continue

    path = os.path.join(folder, name)

    try:
        info = sf.info(path)
        total += 1

        if info.samplerate != 16000:
            sai_mau += 1

        if info.channels != 1:
            sai_kenh += 1

        if not 3 <= info.duration <= 10:
            sai_thoi_luong += 1

    except Exception:
        loi += 1

print("Tong file WAV:", total)
print("File loi:", loi)
print("File khong phai 16 kHz:", sai_mau)
print("File khong phai mono:", sai_kenh)
print("File khong dung 3-10 giay:", sai_thoi_luong)
