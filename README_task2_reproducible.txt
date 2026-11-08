# Task 2 – bộ notebook tái lập (bản chỉnh sửa)

- Các notebook `*_revised.ipynb` giữ lại các cell gốc; phần inference đầy đủ được bổ sung cho viXTTS/F5.
- `sentences_1000_fixed.csv` được dựng từ cột `text` của `metadata_fake(1).csv`, với ID trích từ tên WAV. Kiểm tra lại câu/ID với file nguồn gốc của nhóm trước khi dùng làm chuẩn chính thức.
- `03_vixtts_revised.ipynb`: inference gọi API `model.synthesize` hiện có. Trước khi chạy đủ 1.000, chạy test cell và xác nhận tokenizer `language="vi"` hoạt động. Nếu lỗi, log từng ID, không kết luận tái lập thành công.
- `04_f5_tts_revised.ipynb`: vòng sinh dùng API `F5TTS.infer`; metadata/conversion ghép ID bằng tên `f5_####.wav`, không dùng vị trí dòng để tránh lệch text khi file lỗi.
- Reference: `TTS_vixtts/model/samples/nam-calm.wav`. `REF_TEXT` trong F5 phải được đối chiếu/nghe lại để bảo đảm khớp chính xác. Không có bằng chứng trong file upload để khẳng định đây là speaker VIVOS.
- Dependencies: xem `requirements-task2-reproducible.txt`. Tạo lock thật trong máy đã chạy thành công bằng `pip freeze`; không tự bịa revision hash.
- Các bước sạch: sinh raw -> chuyển đổi/chuẩn hóa sang thư mục `_16k` -> QC. Không QC trực tiếp thư mục raw.
