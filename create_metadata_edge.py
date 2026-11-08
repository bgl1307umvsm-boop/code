
import csv
import subprocess
import json
from pathlib import Path

ROOT = Path(__file__).parent

WAV_DIR = ROOT / "outputs" / "edge-tts-regenerated-16k"
MP3_DIR = ROOT / "outputs" / "edge-tts-regenerated"
OUTPUT_FILE = ROOT / "metadata_edge_regenerated.csv"

FFPROBE = Path(
    r"C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.2-full_build-shared\bin\ffprobe.exe"
)

# Nội dung thực tế dùng để tạo lại các câu có ID đặc biệt
EXTRA = {
    2: "Thông tin này đã được hệ thống ghi nhận thành công. Bạn vui lòng chờ trong giây lát nhé.",
    4: "Nội dung đăng ký của bạn đã được hệ thống ghi nhận thành công. Vui lòng chờ để tiếp tục xử lý.",
    5: "Thông tin liên hệ của bạn đã được ghi nhận đầy đủ. Bạn vui lòng chờ trong giây lát nhé.",
    6: "Yêu cầu hỗ trợ của bạn đã được tiếp nhận và ghi nhận thành công. Chúng tôi sẽ tiếp tục xử lý.",
    7: "Dữ liệu bạn vừa gửi đã được hệ thống ghi nhận thành công. Vui lòng chờ trong giây lát.",
    104: "Bạn đã ghi nhận đăng ký thành công. Vui lòng chờ hệ thống xử lý."
}

# Đọc nội dung gốc của 226 câu
with open(ROOT / "edge_short_226.csv", encoding="utf-8-sig", newline="") as f:
    source_rows = {
        int(row["id"]): row["text"].strip()
        for row in csv.DictReader(f)
    }

metadata = []

for wav in sorted(WAV_DIR.glob("edge_*.wav")):
    clip_id = int(wav.stem.split("_")[1])

    result = subprocess.run(
        [
            str(FFPROBE), "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json", str(wav)
        ],
        capture_output=True,
        text=True,
        check=True
    )

    duration = float(json.loads(result.stdout)["format"]["duration"])

    # Những câu đã được chỉnh sửa khi tạo lại
    if clip_id in EXTRA:
        text = EXTRA[clip_id]
    elif clip_id == 104:
        text = EXTRA[104]
    else:
        text = (
            "Xin lưu ý. " + source_rows[clip_id]
            + " Vui lòng chờ trong giây lát để hệ thống hoàn tất xử lý."
        )

    metadata.append({
        "file_name": str(wav.relative_to(ROOT)).replace("\\", "/"),
        "text": text,
        "tool": "Edge-TTS",
        "label": "fake",
        "language": "vi",
        "sample_rate": 16000,
        "duration": round(duration, 3),
        "speaker": "unknown",
        "split": "review_only"
    })

fields = [
    "file_name", "text", "tool", "label",
    "language", "sample_rate", "duration",
    "speaker", "split"
]

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(metadata)

print("Đã tạo metadata Edge-TTS:", len(metadata), "dòng")
print("File:", OUTPUT_FILE)
