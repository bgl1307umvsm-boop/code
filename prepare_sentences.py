
import csv
from pathlib import Path

ROOT = Path(__file__).parent
OUTPUT_FILE = ROOT / "data" / "sentences_1000.csv"

subjects = [
    "Tôi", "Bạn", "Chúng tôi", "Bộ phận hỗ trợ",
    "Hệ thống", "Nhân viên", "Khách hàng", "Trung tâm",
    "Phòng kỹ thuật", "Đội ngũ chăm sóc khách hàng"
]

actions = [
    "đã ghi nhận", "đang kiểm tra", "đã cập nhật",
    "đang xử lý", "xin xác nhận", "sẽ thông báo",
    "đã tiếp nhận", "đang chuẩn bị", "xin kiểm tra",
    "sẽ gửi thông tin"
]

details = [
    "yêu cầu của bạn.", "thông tin tài khoản.",
    "kết quả giao dịch.", "nội dung đăng ký.",
    "thông tin liên hệ.", "yêu cầu hỗ trợ.",
    "dữ liệu vừa gửi.", "lịch hẹn của bạn.",
    "hồ sơ cần xác minh.", "kết quả kiểm tra."
]

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

sentences = []
for subject in subjects:
    for action in actions:
        for detail in details:
            sentences.append(f"{subject} {action} {detail}")

# Loại bỏ câu trùng và giới hạn 1.000 câu
sentences = list(dict.fromkeys(sentences))[:1000]

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "text"])
    for i, sentence in enumerate(sentences, start=1):
        writer.writerow([i, sentence])

print(f"Đã tạo {len(sentences)} câu tại: {OUTPUT_FILE}")
