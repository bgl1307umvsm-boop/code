
import numpy as np
import soundfile as sf
from vieneu import Vieneu

model = Vieneu()

text = "Tôi đã ghi nhận yêu cầu của bạn."

audio = model.infer(text)
audio = np.asarray(audio)

print("Shape:", audio.shape)
print("Kieu du lieu:", audio.dtype)
print("Gia tri lon nhat:", np.max(np.abs(audio)))
print("Gia tri nho nhat:", np.min(audio))
print("Co NaN:", np.isnan(audio).any())
print("Co vo cuc:", np.isinf(audio).any())

# Luu file thu rieng, khong ghi de file cu
sf.write("test_vieneu.wav", audio, 48000)

info = sf.info("test_vieneu.wav")
print("Sample rate:", info.samplerate)
print("So kenh:", info.channels)
print("Thoi luong:", info.duration)
print("Da tao test_vieneu.wav")
