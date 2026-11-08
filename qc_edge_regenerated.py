import subprocess
import json
from pathlib import Path

ROOT = Path(__file__).parent

FFPROBE = Path(
    r"C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.2-full_build-shared\bin\ffprobe.exe"
)

WAV_DIR = ROOT / "outputs" / "edge-tts-regenerated-16k"

passed = 0

for wav in sorted(WAV_DIR.glob("edge_*.wav")):
    result = subprocess.run([
        str(FFPROBE), "-v", "error",
        "-show_entries", "stream=sample_rate,channels,codec_name",
        "-show_entries", "format=duration",
        "-of", "json", str(wav)
    ], capture_output=True, text=True)

    info = json.loads(result.stdout)
    stream = info["streams"][0]
    duration = float(info["format"]["duration"])

    ok = (
        stream["sample_rate"] == "16000"
        and stream["channels"] == 1
        and stream["codec_name"] == "pcm_s16le"
        and 3 <= duration <= 10
    )

    if ok:
        passed += 1

    print(
        wav.name,
        f"{duration:.3f}s",
        "ĐẠT" if ok else "KHÔNG ĐẠT"
    )

total = len(list(WAV_DIR.glob("edge_*.wav")))
print(f"\nKết quả: {passed}/{total} file đạt QC")