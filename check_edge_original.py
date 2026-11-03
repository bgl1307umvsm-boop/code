import subprocess
from pathlib import Path

root = Path(__file__).parent

ffprobe = Path(
    r"C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.2-full_build-shared\bin\ffprobe.exe"
)

folders = [
    root / "outputs" / "fake_voice_1000" / "edge-tts",
    root / "outputs" / "fake_voice_1000" / "edge-tts_16k"
]

for folder in folders:
    print("\nTHƯ MỤC:", folder.name)

    for clip_id in [104, 227, 326]:
        file = folder / f"edge_{clip_id:04d}{'.mp3' if folder.name == 'edge-tts' else '.wav'}"

        result = subprocess.run(
            [str(ffprobe), "-v", "error",
             "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1",
             str(file)],
            capture_output=True, text=True
        )

        print(file.name, "Duration:", result.stdout.strip(),
              "Size:", file.stat().st_size if file.exists() else "Không tìm thấy")