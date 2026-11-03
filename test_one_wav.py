
import os

root = r"C:\LE_GIA_BA0\Task2_SinhGiongGia"
count = 0

for folder, dirs, files in os.walk(root):
    dirs[:] = [d for d in dirs if d != ".venv"]

    for name in files:
        if name.lower().endswith(".wav"):
            print(os.path.join(folder, name))
            count += 1

            if count >= 10:
                break

    if count >= 10:
        break
