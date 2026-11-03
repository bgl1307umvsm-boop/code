
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent

FFMPEG = Path(
    r"C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.2-full_build-shared\bin\ffmpeg.exe"
)

INPUT_DIR = ROOT / "outputs" / "edge-tts-regenerated"
OUTPUT_DIR = ROOT / "outputs" / "edge-tts-regenerated-16k"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

success = 0
failed = []

for mp3 in sorted(INPUT_DIR.glob("edge_*.mp3")):
    wav = OUTPUT_DIR / (mp3.stem + ".wav")

    try:
        subprocess.run([
            str(FFMPEG), "-y", "-v", "error",
            "-i", str(mp3),
            "-ac", "1",
            "-ar", "16000",
            "-c:a", "pcm_s16le",
            str(wav)
        ], check=True, capture_output=True, text=True)

        success += 1
        print("Đã chuyển:", wav.name)

    except subprocess.CalledProcessError:
        failed.append(mp3.name)
        if wav.exists():
            wav.unlink()
        print("File lỗi:", mp3.name)

print("\n===== KẾT QUẢ =====")
print("Chuyển thành công:", success)
print("File lỗi:", len(failed))
print("Danh sách lỗi:", failed)
