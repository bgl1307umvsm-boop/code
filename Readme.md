# TASK 2 – TỔNG HỢP DỮ LIỆU GIỌNG NÓI GIẢ

## 1. Giới thiệu

Task 2 thuộc dự án phát hiện giọng nói giả mạo bằng AI trong các cuộc gọi lừa đảo tiếng Việt.

Nhiệm vụ là tạo, chuẩn hóa và kiểm tra dữ liệu âm thanh giọng nói tổng hợp để phục vụ huấn luyện và đánh giá mô hình phát hiện giọng nói giả.

## 2. Công cụ sử dụng

Dự án sử dụng 4 công cụ tạo giọng nói tổng hợp:

| Công cụ | Mục đích |
|---|---|
| Edge-TTS | Tạo giọng nói tiếng Việt bằng dịch vụ Microsoft Edge |
| VieNeu-TTS | Tạo giọng nói bằng mô hình VieNeu-TTS |
| viXTTS | Tạo giọng nói tiếng Việt bằng mô hình viXTTS |
| F5-TTS | Tạo giọng nói tổng hợp bằng mô hình F5-TTS |

Các công cụ hỗ trợ:

- Python 3.11.
- VS Code.
- Jupyter Notebook.
- Các thư viện xử lý âm thanh, dữ liệu và mô hình TTS được sử dụng trong từng notebook.

## 3. Dữ liệu đầu vào

File đầu vào chính:

`data/sentences_1000.csv`

File chứa 1.000 câu tiếng Việt dùng làm nội dung đầu vào cho quá trình tạo giọng nói tổng hợp.

Các notebook sử dụng dữ liệu câu tiếng Việt này để tạo âm thanh bằng từng công cụ TTS.

## 4. Bốn notebook thực hiện

Các notebook được lưu trong thư mục `notebooks/`.

| Notebook | Công cụ | Nội dung |
|---|---|---|
| `01_edge_tts.ipynb` | Edge-TTS | Tạo và kiểm tra giọng nói bằng Edge-TTS |
| `02_vieneu_tts.ipynb` | VieNeu-TTS | Tạo và kiểm tra giọng nói bằng VieNeu-TTS |
| `03_vixtts.ipynb` | viXTTS | Tạo và kiểm tra giọng nói bằng viXTTS |
| `04_f5_tts.ipynb` | F5-TTS | Tạo và kiểm tra giọng nói bằng F5-TTS |

### Quy trình chung trong các notebook

1. Đọc dữ liệu câu tiếng Việt đầu vào.
2. Khởi tạo công cụ hoặc mô hình TTS.
3. Tạo file âm thanh từ nội dung văn bản.
4. Lưu file WAV vào thư mục đầu ra tương ứng.
5. Kiểm tra số lượng và thông tin file âm thanh.
6. Chuẩn hóa dữ liệu để phục vụ quá trình tổng hợp và kiểm tra.

Lưu ý: Mỗi công cụ có cách cài đặt, cấu hình mô hình và dependencies riêng. Cần sử dụng đúng phần hướng dẫn trong notebook tương ứng.

## 5. Dependencies và môi trường chạy

Môi trường thực hiện:

- Hệ điều hành: Windows.
- Python: 3.11.
- IDE: Visual Studio Code.
- Môi trường ảo: `.venv`.
- Công cụ chạy notebook: Jupyter Notebook.

Các nhóm thư viện cần thiết tùy theo công cụ:

| Nhóm | Mục đích |
|---|---|
| Edge-TTS | Kết nối và tạo giọng nói bằng Edge-TTS |
| VieNeu-TTS | Cài đặt và chạy mô hình VieNeu-TTS |
| viXTTS / TTS | Chạy mô hình tổng hợp giọng nói viXTTS |
| F5-TTS | Chạy mô hình F5-TTS |
| NumPy, Pandas | Xử lý dữ liệu và metadata |
| SoundFile, Librosa | Đọc và xử lý âm thanh |
| Torch, Torchaudio | Hỗ trợ xử lý và chạy mô hình học sâu |
| Jupyter | Chạy các notebook |

Phiên bản thư viện cụ thể cần được đối chiếu với môi trường và notebook thực tế trước khi cài đặt lại.

## 6. Dữ liệu đầu ra

Dự án đã tạo tổng cộng **4.000 file WAV**, phân bổ như sau:

| Công cụ | Số lượng |
|---|---:|
| Edge-TTS | 1.000 |
| VieNeu-TTS | 1.000 |
| F5-TTS | 1.000 |
| viXTTS | 1.000 |
| **Tổng cộng** | **4.000** |

Thông số dữ liệu WAV sau chuẩn hóa:

- Định dạng: WAV.
- Tần số lấy mẫu: 16.000 Hz.
- Số kênh: Mono.
- Độ sâu bit: PCM 16-bit.
- Thời lượng mục tiêu: từ 3 đến 10 giây.

## 7. Cấu trúc thư mục

```text
Task2_SinhGiongGia/
├── data/
│   ├── sentences_1000.csv
│   ├── sentences_1000_fixed.csv
│   ├── metadata_fake.csv
│   ├── qc_report.csv
│   ├── qc_listen_sample.csv
│   └── sha256_manifest.csv
│
├── outputs/
│   ├── fake_voice_1000/
│   │   ├── vieneu-tts_16k/
│   │   ├── edge-tts_16k/
│   │   ├── vixtts_16k/
│   │   └── f5-tts_16k/
│   │
│   └── edge-tts-regenerated-16k/
│
├── notebooks/
│   ├── 01_edge_tts.ipynb
│   ├── 02_vieneu_tts.ipynb
│   ├── 03_vixtts.ipynb
│   └── 04_f5_tts.ipynb
│
├── TTS_vixtts/
├── generate_edge_tts.py
├── generate_vieneu.py
├── generate_f5.py
├── merge_metadata.py
├── normalize_wav.py
├── README.md
└── .venv/
```

Lưu ý: Đây là các thư mục và file chính. Dự án còn có thể chứa file dữ liệu gốc, script kiểm tra và file thử nghiệm khác.

## 8. Metadata

File metadata tổng hợp:

`data/metadata_fake.csv`

Schema gồm 9 trường:

```text
clip_id,path,label,speaker_id,source,generator,channel,split,duration
```

Ý nghĩa:

- `clip_id`: Mã định danh của clip.
- `path`: Đường dẫn đến file WAV.
- `label`: Nhãn dữ liệu.
- `speaker_id`: Mã người nói.
- `source`: Nguồn dữ liệu.
- `generator`: Công cụ tạo giọng nói.
- `channel`: Thông tin kênh âm thanh.
- `split`: Tập dữ liệu.
- `duration`: Thời lượng clip.

Metadata có 4.000 dòng tương ứng với 4.000 file WAV.

## 9. Hướng dẫn chạy lại quy trình

### Bước 1: Mở thư mục dự án

Mở thư mục `Task2_SinhGiongGia` bằng VS Code.

### Bước 2: Kích hoạt môi trường Python

Mở Terminal tại thư mục dự án và chạy:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Bước 3: Cài đặt dependencies

Cài đặt các thư viện cần thiết theo đúng môi trường của từng công cụ TTS và notebook tương ứng.

### Bước 4: Chạy các notebook

Mở thư mục `notebooks/` và chạy notebook theo công cụ cần sử dụng:

1. `01_edge_tts.ipynb`
2. `02_vieneu_tts.ipynb`
3. `03_vixtts.ipynb`
4. `04_f5_tts.ipynb`

Đối với viXTTS, cần chuẩn bị đúng mô hình và cấu hình theo notebook.

### Bước 5: Chạy các script tạo dữ liệu

Các script hiện có:

```powershell
python generate_edge_tts.py
python generate_vieneu.py
python generate_f5.py
```

### Bước 6: Chuẩn hóa và tổng hợp dữ liệu

Sau khi tạo dữ liệu, sử dụng các script:

```powershell
python normalize_wav.py
python merge_metadata.py
```

### Bước 7: Kiểm tra dữ liệu

Kiểm tra file WAV, metadata và manifest SHA256 trước khi sử dụng dữ liệu.

Lưu ý: Không cần chạy lại các script tạo 4.000 clip nếu chỉ muốn kiểm tra hoặc sử dụng bộ dữ liệu đã tạo. Các script sinh dữ liệu có thể tạo thêm hoặc ghi đè file tùy cấu hình.

## 10. Chuẩn hóa và kiểm tra WAV

Các file âm thanh được chuẩn hóa về:

- Sample rate: 16.000 Hz.
- Channels: Mono.
- Bit depth: PCM 16-bit.
- Thời lượng mục tiêu: 3–10 giây.

File báo cáo:

`data/qc_report.csv`

Kết quả QC được ghi nhận:

| Nội dung | Kết quả |
|---|---:|
| Tổng số WAV | 4.000 |
| PASS | 4.000 |
| FAIL | 0 |

Các thông số được kiểm tra trực tiếp từ file WAV, không chỉ dựa trên thông tin thời lượng trong metadata.

## 11. SHA256 và tính toàn vẹn dữ liệu

File manifest:

`data/sha256_manifest.csv`

Mỗi file WAV có một mã SHA256 riêng để hỗ trợ kiểm tra tính toàn vẹn và nhận diện thay đổi dữ liệu.

Kết quả kiểm tra manifest:

- Tổng số dòng: 4.000.
- SHA256 bị thiếu: 0.
- SHA256 sai độ dài: 0.
- Clip ID bị thiếu: 0.
- Đường dẫn bị thiếu: 0.

## 12. Kết quả

Sau quá trình tạo và chuẩn hóa dữ liệu, dự án thu được 4.000 file WAV từ bốn công cụ Edge-TTS, VieNeu-TTS, F5-TTS và viXTTS.

Metadata tổng hợp, báo cáo QC và manifest SHA256 được tạo để hỗ trợ quản lý, kiểm tra và sử dụng dữ liệu cho các bước tiếp theo.

## 13. Lưu ý

- QC PASS không đồng nghĩa với việc toàn bộ nội dung giọng nói đã được nghe và xác nhận chính xác.
- Danh tính người nói cần được xác minh trước khi sử dụng speaker ID như thông tin đã được xác nhận.
- Việc chia tập train, validation và test cần tuân theo nguyên tắc tránh rò rỉ dữ liệu.
- Cần kiểm tra giấy phép sử dụng của từng công cụ, mô hình và dữ liệu giọng tham chiếu trước khi chia sẻ hoặc sử dụng trong sản phẩm.
- Khi chạy lại từ đầu, cần kiểm tra đường dẫn, model, dependencies và cấu hình của từng công cụ.
