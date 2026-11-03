import csv
import os
import re
import subprocess
import sys
from pathlib import Path

# =========================
# CAU HINH
# =========================
ROOT = Path(r"C:\LE_GIA_BA0\Task2_SinhGiongGia")

# File chứa 1000 câu gốc
CSV_FILE = ROOT / "data" / "sentences_1000.csv"

# File giọng mẫu
REF_AUDIO = (
    ROOT / "outputs" / "fake_voice_1000"
    / "vieneu-tts" / "vieneu_0001.wav"
)

# Thư mục lưu WAV F5-TTS
OUTPUT_DIR = (
    ROOT / "outputs" / "fake_voice_1000" / "f5-tts"
)

# Metadata đầu ra, không ghi đè CSV câu gốc
METADATA_FILE = OUTPUT_DIR / "metadata_f5.csv"

# Phải khớp chính xác lời nói trong file REF_AUDIO
REF_TEXT = "Xin chào các bạn"

# Chạy thử 3 câu trước.
# Sau khi kiểm tra thành công, đổi thành None để chạy toàn bộ.
TEST_LIMIT = None

MODEL_NAME = "F5TTS_Base"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_metadata(metadata):
    """Lưu metadata sau mỗi câu để hạn chế mất tiến độ."""
    columns = ["filename", "text", "model", "status"]

    with open(
        METADATA_FILE, "w", encoding="utf-8-sig", newline=""
    ) as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(metadata.values())


def main():
    # Kiểm tra đầu vào
    if not CSV_FILE.exists():
        print("LOI: Khong tim thay CSV:", CSV_FILE)
        return

    if not REF_AUDIO.exists():
        print("LOI: Khong tim thay file giọng mẫu:", REF_AUDIO)
        return

    if not REF_TEXT.strip():
        print("LOI: REF_TEXT dang trong.")
        return

    # Đọc danh sách câu gốc
    with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not {"id", "text"}.issubset(
            reader.fieldnames
        ):
            print("LOI: CSV phai co hai cot id va text.")
            print("Cac cot hien co:", reader.fieldnames)
            return

        sentences = list(reader)

    if not sentences:
        print("LOI: CSV khong co du lieu.")
        return

    # Đọc metadata cũ nếu có
    metadata = {}

    if METADATA_FILE.exists():
        with open(
            METADATA_FILE, "r", encoding="utf-8-sig", newline=""
        ) as f:
            for row in csv.DictReader(f):
                if row.get("filename"):
                    metadata[row["filename"]] = row

    # Chỉ chọn số câu cần chạy
    selected = [
    row for row in sentences
    if str(row.get("id", "")).strip() in {"104", "131"}
]
    print("Tong so cau goc:", len(sentences))
    print("So cau se kiem tra:", len(selected))
    print("Thu muc WAV:", OUTPUT_DIR)

    success = 0
    failed = 0
    skipped = 0

    for position, row in enumerate(selected, start=1):
        sentence_id = str(row.get("id", position)).strip()
        sentence = (row.get("text") or "").strip()

        # Dùng ID của câu để đặt tên file ổn định
        if not sentence_id.isdigit():
            print(f"[{position}] BO QUA: ID khong hop le.")
            failed += 1
            continue

        filename = f"f5_{int(sentence_id):04d}.wav"
        output_file = OUTPUT_DIR / filename

        if not sentence:
            print(f"[{position}] THAT BAI: Cau trong.")
            failed += 1
            metadata[filename] = {
                "filename": filename,
                "text": sentence,
                "model": MODEL_NAME,
                "status": "failed",
            }
            save_metadata(metadata)
            continue

        # Không ghi đè WAV đã có
        if output_file.exists() and output_file.stat().st_size > 1000:
            print(f"[{position}] DA CO, BO QUA: {filename}")
            skipped += 1

            # Chỉ bổ sung metadata nếu chưa có
            if filename not in metadata:
                metadata[filename] = {
                    "filename": filename,
                    "text": sentence,
                    "model": MODEL_NAME,
                    "status": "success",
                }
                save_metadata(metadata)
            continue

        command = [
            sys.executable,
            "-m", "f5_tts.infer.infer_cli",
            "--model", MODEL_NAME,
            "--ref_audio", str(REF_AUDIO),
            "--ref_text", REF_TEXT,
            "--gen_text", sentence,
            "--output_dir", str(OUTPUT_DIR),
            "--output_file", filename,
        ]

        print(f"\n[{position}/{len(selected)}] Dang tao: {filename}")
        print("Cau:", sentence)

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"

        try:
            result = subprocess.run(
                command,
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=600,
                env=env,
            )

            if (
                result.returncode == 0
                and output_file.exists()
                and output_file.stat().st_size > 1000
            ):
                success += 1
                status = "success"
                print("THANH CONG:", filename)
            else:
                failed += 1
                status = "failed"
                print("THAT BAI. Ma loi:", result.returncode)

                error_text = result.stderr or result.stdout or "Khong co log."
                print(error_text[-2500:])

        except subprocess.TimeoutExpired:
            failed += 1
            status = "failed"
            print("THAT BAI: Qua 10 phut.")

        except Exception as e:
            failed += 1
            status = "failed"
            print("LOI:", str(e))

        # Cập nhật metadata, không sửa CSV câu gốc
        metadata[filename] = {
            "filename": filename,
            "text": sentence,
            "model": MODEL_NAME,
            "status": status,
        }
        save_metadata(metadata)

    # Đếm số WAV thực tế
    wav_count = sum(
        1 for p in OUTPUT_DIR.glob("*.wav")
        if p.is_file()
    )

    print("\n===== KET QUA =====")
    print("Tao thanh cong trong lan nay:", success)
    print("That bai:", failed)
    print("Da bo qua file co san:", skipped)
    print("Tong WAV trong thu muc:", wav_count)
    print("Metadata:", METADATA_FILE)


if __name__ == "__main__":
    main()