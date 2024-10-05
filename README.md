# VoiceTyping
venv\Scripts\activate
deactivate

VoiceTyping là một ứng dụng máy tính cho phép người dùng nhập văn bản bằng giọng nói tại vị trí con trỏ chuột, sử dụng công nghệ nhận dạng giọng nói của Google Docs.

## Kiến trúc dự án

Dự án được chia thành hai phần chính:

1. Frontend: Giao diện người dùng (GUI)
2. Backend: 
   - Mô-đun nhận dạng giọng nói
   - Mô-đun xử lý văn bản
   - Mô-đun điều khiển con trỏ và nhập liệu

## Công nghệ sử dụng

- **Ngôn ngữ lập trình:** Python
- **GUI Framework:** PyQt5
- **Nhận dạng giọng nói:** Google Cloud Speech-to-Text API
- **Điều khiển con trỏ và nhập liệu:** PyAutoGUI
- **Xử lý văn bản:** NLTK (Natural Language Toolkit)

## Cấu trúc dự án và chức năng

VoiceTyping/
│
├── frontend/
│   ├── main_window.py  # Giao diện chính của ứng dụng
│   └── test_gui.py     # Kiểm thử giao diện người dùng
│
├── backend/
│   ├── recognizer.py   # Xử lý nhận dạng giọng nói
│   ├── processor.py    # Xử lý và định dạng văn bản
│   ├── controller.py   # Điều khiển con trỏ và nhập liệu
│   ├── test_speech_recognition.py  # Kiểm thử nhận dạng giọng nói
│   ├── test_text_processing.py     # Kiểm thử xử lý văn bản
│   └── test_input_control.py       # Kiểm thử điều khiển nhập liệu
│
├── main.py             # Điểm khởi đầu của ứng dụng
├── requirements.txt    # Danh sách các thư viện cần thiết
├── README.md           # Tài liệu hướng dẫn sử dụng
└── .gitignore          # Cấu hình Git ignore

### Chi tiết chức năng:

1. Frontend:
   - `main_window.py`: Tạo giao diện chính của ứng dụng, bao gồm các nút điều khiển và hiển thị trạng thái.
   - `test_gui.py`: Chứa các bài kiểm tra để đảm bảo giao diện hoạt động chính xác.

2. Backend:
   - `recognizer.py`: Xử lý việc nhận dạng giọng nói, kết nối với Google Cloud Speech-to-Text API.
   - `processor.py`: Xử lý và định dạng văn bản nhận được từ nhận dạng giọng nói.
   - `controller.py`: Điều khiển con trỏ chuột và thực hiện việc nhập liệu tại vị trí con trỏ.
   - Các file test tương ứng để kiểm tra tính năng của từng module.

3. File chính:
   - `main.py`: Điểm khởi đầu của ứng dụng, kết nối frontend và backend.
   - `requirements.txt`: Liệt kê các thư viện Python cần thiết cho dự án.
   - `README.md`: Cung cấp thông tin về dự án và hướng dẫn sử dụng.
   - `.gitignore`: Xác định các file và thư mục không nên theo dõi bởi Git.

## Cài đặt và Sử dụng

(Hướng dẫn cài đặt và sử dụng sẽ được thêm vào sau)

## Đóng góp

(Hướng dẫn đóng góp cho dự án sẽ được thêm vào sau)

## Giấy phép

(Thông tin về giấy phép sẽ được thêm vào sau)