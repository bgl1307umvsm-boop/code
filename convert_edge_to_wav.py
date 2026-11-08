import subprocess
from pathlib import Path

ROOT = Path(__file__).parent

FFMPEG = Path(
    r"C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.2-full_build-shared\bin\ffmpeg.exe"
)

INPUT_DIR = ROOT / "outputs" / "fake_voice_1000" / "edge-tts"
OUTPUT_DIR = ROOT / "outputs" / "fake_voice_1000" / "edge-tts_16k"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = sorted(INPUT_DIR.glob("edge_*.mp3"))

success = 0
failed = []

for index, mp3 in enumerate(files, 1):
    wav = OUTPUT_DIR / (mp3.stem + ".wav")

    command = [
        str(FFMPEG),
        "-y",
        "-i", str(mp3),
        "-ac", "1",
        "-ar", "16000",
        "-c:a", "pcm_s16le",
        str(wav),
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if result.returncode == 0 and wav.exists() and wav.stat().st_size > 44:
        success += 1
    else:
        failed.append(mp3.name)

    if index % 100 == 0:
        print(f"Đã xử lý: {index}/{len(files)}")

print("\nHoàn thành!")
print("Tổng MP3:", len(files))
print("Chuyển thành công:", success)
print("Lỗi:", len(failed))
print("Thư mục WAV:", OUTPUT_DIR)

if failed:
    print("Các file lỗi:", failed)