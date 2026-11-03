import subprocess
import json
from pathlib import Path

ROOT = Path(__file__).parent
FFPROBE = Path(
    r"C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.2-full_build-shared\bin\ffprobe.exe"
)

WAV_DIR = ROOT / "outputs" / "fake_voice_1000" / "edge-tts_16k"

total = 0
valid = 0
wrong_format = []
wrong_duration = []
errors = []

for wav in sorted(WAV_DIR.glob("edge_*.wav")):
    total += 1

    command = [
        str(FFPROBE),
        "-v", "error",
        "-show_entries",
        "stream=sample_rate,channels,codec_name,bits_per_sample",
        "-show_entries", "format=duration",
        "-of", "json",
        str(wav),
    ]

    result = subprocess.run(
        command, capture_output=True, text=True
    )

    if result.returncode != 0:
        errors.append(wav.name)
        continue

    try:
        data = json.loads(result.stdout)
        stream = data["streams"][0]
        duration = float(data["format"]["duration"])

        correct_format = (
            stream.get("sample_rate") == "16000"
            and stream.get("channels") == 1
            and stream.get("codec_name") == "pcm_s16le"
            and stream.get("bits_per_sample") == 16
        )

        correct_duration = 3 <= duration <= 10

        if not correct_format:
            wrong_format.append(wav.name)

        if not correct_duration:
            wrong_duration.append((wav.name, round(duration, 3)))

        if correct_format and correct_duration:
            valid += 1

    except Exception:
        errors.append(wav.name)

print("\n===== KẾT QUẢ QC EDGE-TTS =====")
print("Tổng file:", total)
print("Đạt định dạng và thời lượng:", valid)
print("Sai định dạng:", len(wrong_format))
print("Sai thời lượng (3–10 giây):", len(wrong_duration))
print("Lỗi đọc file:", len(errors))

if wrong_format:
    print("File sai định dạng:", wrong_format[:20])

if wrong_duration:
    print("File sai thời lượng:", wrong_duration[:20])

if errors:
    print("File lỗi:", errors[:20])