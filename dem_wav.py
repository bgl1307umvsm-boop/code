
import os

root = r"C:\LE_GIA_BA0\Task2_SinhGiongGia\outputs"

for tool in os.listdir(root):
    folder = os.path.join(root, tool)

    if os.path.isdir(folder):
        wav_files = [
            f for f in os.listdir(folder)
            if f.lower().endswith(".wav")
        ]

        print(f"{tool}: {len(wav_files)} file WAV")
