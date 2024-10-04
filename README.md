# VoiceTyping

VoiceTyping là một ứng dụng máy tính cho phép người dùng nhập văn bản bằng giọng nói tại vị trí con trỏ chuột, sử dụng công nghệ nhận dạng giọng nói của Google Docs.

## Kiến trúc dự án

Dự án được chia thành các thành phần chính sau:

1. Giao diện người dùng (GUI)
2. Mô-đun nhận dạng giọng nói
3. Mô-đun xử lý văn bản
4. Mô-đun điều khiển con trỏ và nhập liệu

## Công nghệ sử dụng

- **Ngôn ngữ lập trình:** Python
- **GUI Framework:** PyQt5
- **Nhận dạng giọng nói:** Google Cloud Speech-to-Text API
- **Điều khiển con trỏ và nhập liệu:** PyAutoGUI
- **Xử lý văn bản:** NLTK (Natural Language Toolkit)

## Cấu trúc dự án



VoiceTyping/
│
├── src/
│ ├── gui/
│ │ ├── init.py
│ │ └── main_window.py
│ ├── speech_recognition/
│ │ ├── init.py
│ │ └── recognizer.py
│ ├── text_processing/
│ │ ├── init.py
│ │ └── processor.py
│ ├── input_control/
│ │ ├── init.py
│ │ └── controller.py
│ └── main.py
│
├── tests/
│ ├── test_gui.py
│ ├── test_speech_recognition.py
│ ├── test_text_processing.py
│ └── test_input_control.py
│
├── requirements.txt
├── setup.py
├── README.md
└── .gitignore

## Cài đặt và Sử dụng

(Hướng dẫn cài đặt và sử dụng sẽ được thêm vào sau)

## Đóng góp

(Hướng dẫn đóng góp cho dự án sẽ được thêm vào sau)

## Giấy phép

(Thông tin về giấy phép sẽ được thêm vào sau)