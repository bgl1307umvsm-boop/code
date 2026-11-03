
import csv
import subprocess
import sys
import shutil
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CSV_FILE = ROOT / "data" / "sentences_1000.csv"
REF_AUDIO = ROOT / "outputs" / "vieneu-tts" / "vieneu_0001.wav"
OUTPUT_DIR = ROOT / "outputs" / "fake_voice_1000" / "f5-tts"
METADATA_FILE = OUTPUT_DIR / "metadata_f5.csv"

# True: xóa WAV F5 cũ để sinh lại toàn bộ từ đầu.
# False: giữ WAV cũ.
RESET_OUTPUT = False

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Kiểm tra đầu vào
if not CSV_FILE.exists():
    sys.exit(f"Không tìm thấy CSV: {CSV_FILE}")

if not REF_AUDIO.exists():
    sys.exit(f"Không tìm thấy audio mẫu: {REF_AUDIO}")
import soundfile as sf

audio, sample_rate = sf.read(REF_AUDIO)

print("Audio mẫu:", REF_AUDIO.name)
print("Sample rate:", sample_rate)
print("Thời lượng:", len(audio) / sample_rate, "giây")
print("Tổng câu trong CSV:", len(rows) if "rows" in globals() else "Chưa đọc CSV")
# Đọc CSV
with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

if not rows:
    sys.exit("CSV không có dữ liệu.")

columns = list(rows[0].keys())

text_column = next(
    (c for c in ["text", "sentence", "noi_dung", "cau"] if c in columns),
    None
)

id_column = next(
    (c for c in ["id", "clip_id", "ID"] if c in columns),
    None
)

if text_column is None:
    sys.exit(f"Không tìm thấy cột nội dung câu. Các cột: {columns}")

# Nếu muốn chạy lại toàn bộ, chỉ xóa file do F5 tạo
if RESET_OUTPUT:
    for wav_file in OUTPUT_DIR.glob("f5_*.wav"):
        wav_file.unlink()

    if METADATA_FILE.exists():
        METADATA_FILE.unlink()

# Tạo ID ổn định theo CSV
used_ids = set()
tasks = []

for row_number, row in enumerate(rows, start=1):
    original_id = (
        str(row.get(id_column, "")).strip()
        if id_column else str(row_number)
    )

    if not original_id:
        original_id = str(row_number)

    # Làm ID an toàn để đặt tên file
    safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", original_id)

    if safe_id in used_ids:
        sys.exit(f"ID bị trùng trong CSV: {original_id}")

    used_ids.add(safe_id)

    sentence = (row.get(text_column) or "").strip()

    tasks.append({
        "id": original_id,
        "safe_id": safe_id,
        "text": sentence,
    })
print("\n===== KIỂM TRA DỮ LIỆU =====")
print("Tổng số câu:", len(tasks))
print("5 ID đầu:", [task["id"] for task in tasks[:5]])
print("5 câu đầu:", [task["text"] for task in tasks[:5]])
print("Số ID duy nhất:", len({task["safe_id"] for task in tasks}))
metadata_rows = []
existing_metadata = {}

if METADATA_FILE.exists():
    with open(METADATA_FILE, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_metadata[row["filename"]] = row
for index, task in enumerate(tasks, start=1):
    clip_id = task["id"]
    safe_id = task["safe_id"]
    sentence = task["text"]

    output_file = OUTPUT_DIR / f"f5_{safe_id}.wav"

    metadata = {
        "id": clip_id,
        "filename": output_file.name,
        "text": sentence,
        "model": "F5TTS_Base",
        "status": "",
        "error": "",
    }

    
    print(f"\n[{index}/{len(tasks)}] ID: {clip_id}")

    if not sentence:
        metadata["status"] = "skipped_empty_text"
        metadata["error"] = "Câu trong CSV bị trống"
        print("Bỏ qua vì câu trống.")

    elif output_file.exists():
        print("Đã có file, bỏ qua:", output_file.name)

        old_metadata = existing_metadata.get(output_file.name)

        if old_metadata:
            metadata.update(old_metadata)

        metadata["status"] = "success"
        metadata["error"] = ""

    else:
        temp_dir = OUTPUT_DIR / f"_temp_{safe_id}"

        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        temp_dir.mkdir(parents=True)

        try:
            command = [
                sys.executable,
                "-m", "f5_tts.infer.infer_cli",
                "--model", "F5TTS_Base",
                "--ref_audio", str(REF_AUDIO),
                "--ref_text", "Tôi đã ghi nhận yêu cầu của bạn.",
                "--gen_text", sentence,
                "--output_dir", str(temp_dir),
            ]

            result = subprocess.run(
                command,
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=600,
            )

            generated_files = list(temp_dir.rglob("*.wav"))

            if result.returncode == 0 and generated_files:
                generated_file = generated_files[0]
                shutil.copy2(generated_file, output_file)

                metadata["status"] = "success"
                print("Đã tạo:", output_file.name)

            else:
                metadata["status"] = "failed"
                metadata["error"] = (
                    (result.stderr or result.stdout or "Không tìm thấy WAV")[-2000:]
                )
                print("Sinh thất bại:", metadata["error"])

        except subprocess.TimeoutExpired:
            metadata["status"] = "timeout"
            metadata["error"] = "Quá thời gian 10 phút"
            print("Câu này bị timeout.")

        except Exception as e:
            metadata["status"] = "failed"
            metadata["error"] = str(e)
            print("Lỗi:", e)

        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

    metadata_rows.append(metadata)

    # Lưu tiến độ sau mỗi câu

    with open(
        METADATA_FILE, "w", encoding="utf-8-sig", newline=""
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id", "filename", "text",
                "model", "status", "error"
            ]
        )
        writer.writeheader()
        writer.writerows(metadata_rows)

# Tổng kết
success = sum(r["status"] == "success" for r in metadata_rows)
failed = sum(r["status"] == "failed" for r in metadata_rows)
timeout = sum(r["status"] == "timeout" for r in metadata_rows)
skipped = sum(r["status"] == "skipped_empty_text" for r in metadata_rows)

print("\n========== KẾT QUẢ F5-TTS ==========")
print("Tổng câu:", len(tasks))
print("Thành công:", success)
print("Thất bại:", failed)
print("Timeout:", timeout)
print("Câu trống:", skipped)
print("Metadata:", METADATA_FILE)
print("Thư mục WAV:", OUTPUT_DIR)
