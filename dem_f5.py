
import os

folder = r"C:\LE_GIA_BA0\Task2_SinhGiongGia\outputs\f5-tts"

if not os.path.exists(folder):
    print("Khong tim thay thu muc F5-TTS!")
else:
    wav_files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(".wav")
    ]

    print("So file WAV:", len(wav_files))

    metadata = os.path.join(folder, "metadata_f5.csv")

    if os.path.exists(metadata):
        with open(metadata, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()

        print("So dong metadata (khong tinh tieu de):", max(0, len(lines) - 1))

        failed = sum(
            1 for line in lines[1:]
            if ",failed" in line.lower()
        )
        print("So dong bao failed:", failed)
    else:
        print("Khong tim thay metadata_f5.csv")
