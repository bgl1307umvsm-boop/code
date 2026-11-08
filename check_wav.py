
import os
import wave
import csv

# Duong dan du an
thu_muc_du_an = r"C:\LE_GIA_BA0\Task2_SinhGiongGia"

# File metadata va thu muc WAV
csv_path = os.path.join(thu_muc_du_an, "metadata_fake.csv")
folder = os.path.join(
    thu_muc_du_an,
    "outputs",
    "fake_voice_1000",
    "vieneu-tts_16k"
)

total = 0
valid = 0
invalid = 0
empty = 0
wrong_rate = 0
wrong_channels = 0
wrong_duration = 0

# Kiem tra duong dan
if not os.path.isfile(csv_path):
    print("LOI: Khong tim thay metadata_fake.csv:", csv_path)
    raise SystemExit

if not os.path.isdir(folder):
    print("LOI: Khong tim thay thu muc WAV:", folder)
    raise SystemExit

# Doc metadata
with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print("Bat dau kiem tra WAV...\n")

for row in rows:
    filename = row.get("file_name", "").strip()
    total += 1

    if not filename:
        print("LOI: Dong CSV khong co file_name")
        invalid += 1
        continue

    # file_name da la duong dan day du
    # Neu chi la ten file thi tim trong folder WAV
    if os.path.isabs(filename):
        path = filename
    else:
        path = os.path.join(folder, os.path.basename(filename))

    if not os.path.exists(path):
        print("THIEU FILE:", filename)
        invalid += 1
        continue

    if os.path.getsize(path) == 0:
        print("FILE RONG:", filename)
        empty += 1
        continue

    try:
        with wave.open(path, "rb") as wav:
            rate = wav.getframerate()
            channels = wav.getnchannels()
            frames = wav.getnframes()
            duration = frames / rate if rate else 0

            if duration <= 0:
                print("FILE LOI:", filename)
                invalid += 1
                continue

            valid += 1

            if rate != 16000:
                wrong_rate += 1

            if channels != 1:
                wrong_channels += 1

            if duration < 3 or duration > 10:
                wrong_duration += 1

            if rate != 16000 or channels != 1 or duration < 3 or duration > 10:
                print(
                    "CAN KIEM TRA:", os.path.basename(path),
                    "| Hz:", rate,
                    "| Kenh:", channels,
                    "| Giay:", round(duration, 2)
                )

    except Exception as e:
        print("KHONG DOC DUOC:", filename, "|", e)
        invalid += 1

print("\n===== TONG KET =====")
print("So dong CSV:", total)
print("WAV doc duoc:", valid)
print("File loi/khong doc duoc:", invalid)
print("File rong:", empty)
print("WAV khong phai 16 kHz:", wrong_rate)
print("WAV khong phai mono:", wrong_channels)
print("WAV ngoai 3-10 giay:", wrong_duration)
