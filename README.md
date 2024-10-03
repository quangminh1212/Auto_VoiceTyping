# VoiceTyping

Đây là kiến trúc phần mềm tối ưu cho ứng dụng Nhập liệu bằng giọng nói tiếng Việt, sử dụng tính năng Voice Typing của Google Docs và tích hợp đăng nhập Google.

## Kiến Trúc Phần Mềm Tổng Quan

1. Giao diện Người Dùng (UI Layer)
2. Tầng Xác thực (Authentication Layer)
3. Tầng Điều khiển Trình duyệt (Browser Automation Layer)
4. Tầng Quản lý Văn bản (Text Management Layer)
5. Tầng Tương tác Hệ thống (System Interaction Layer)
6. Tầng Quản lý Trạng thái (State Management Layer)
7. Tầng Bảo mật và Xử lý Lỗi (Security and Error Handling Layer)

### Công nghệ sử dụng

- Ngôn ngữ lập trình: Python 3.9+
- Framework GUI: PyQt6
- Xác thực: Google OAuth 2.0
- Điều khiển trình duyệt: Selenium với ChromeDriver
- Quản lý trạng thái: RxPY (Reactive Extensions for Python)
- Tương tác hệ thống: PyAutoGUI
- Xử lý bất đồng bộ: asyncio
- Logging: structlog
- Bảo mật: cryptography

### Cấu trúc dự án và Công dụng của từng file

```
voicetyping/
├── main.py                 # Điểm khởi đầu của ứng dụng, khởi tạo các thành phần chính
├── ui/
│   ├── __init__.py         # Đánh dấu thư mục ui là một Python package
│   └── main_window.py      # Định nghĩa giao diện chính của ứng dụng
├── auth/
│   ├── __init__.py         # Đánh dấu thư mục auth là một Python package
│   └── google_auth.py      # Xử lý xác thực với Google OAuth 2.0
├── browser/
│   ├── __init__.py         # Đánh dấu thư mục browser là một Python package
│   └── docs_controller.py  # Điều khiển Google Docs thông qua Selenium
├── text/
│   ├── __init__.py         # Đánh dấu thư mục text là một Python package
│   └── manager.py          # Quản lý và xử lý văn bản
├── system/
│   ├── __init__.py         # Đánh dấu thư mục system là một Python package
│   └── interaction.py      # Xử lý tương tác với hệ thống (nhập liệu, phím tắt)
├── state/
│   ├── __init__.py         # Đánh dấu thư mục state là một Python package
│   └── store.py            # Quản lý trạng thái ứng dụng sử dụng RxPY
└── utils/
    ├── __init__.py         # Đánh dấu thư mục utils là một Python package
    ├── security.py         # Xử lý các vấn đề bảo mật, mã hóa
    └── logger.py           # Cấu hình và quản lý logging
```

### Chi tiết các tầng và file liên quan

1. Giao diện Người Dùng (UI Layer)
   - File: `ui/main_window.py`
   - Công dụng: Định nghĩa giao diện chính của ứng dụng sử dụng PyQt6

2. Tầng Xác thực (Authentication Layer)
   - File: `auth/google_auth.py`
   - Công dụng: Xử lý quá trình xác thực với Google OAuth 2.0, lưu trữ và làm mới token

3. Tầng Điều khiển Trình duyệt (Browser Automation Layer)
   - File: `browser/docs_controller.py`
   - Công dụng: Điều khiển Google Docs thông qua Selenium, kích hoạt Voice Typing

4. Tầng Quản lý Văn bản (Text Management Layer)
   - File: `text/manager.py`
   - Công dụng: Trích xuất, xử lý và quản lý văn bản từ Google Docs

5. Tầng Tương tác Hệ thống (System Interaction Layer)
   - File: `system/interaction.py`
   - Công dụng: Xử lý tương tác với hệ thống như nhập liệu, phím tắt sử dụng PyAutoGUI

6. Tầng Quản lý Trạng thái (State Management Layer)
   - File: `state/store.py`
   - Công dụng: Quản lý trạng thái ứng dụng sử dụng RxPY, xử lý luồng dữ liệu reactive

7. Tầng Bảo mật và Xử lý Lỗi (Security and Error Handling Layer)
   - Files: `utils/security.py`, `utils/logger.py`
   - Công dụng: 
     - `security.py`: Xử lý các vấn đề bảo mật, mã hóa dữ liệu nhạy cảm
     - `logger.py`: Cấu hình và quản lý logging, ghi lại các sự kiện và lỗi

## Luồng Hoạt động Tổng thể

1. Người dùng khởi động ứng dụng (main.py)
2. Đăng nhập bằng tài khoản Google (auth/google_auth.py)
3. Ứng dụng mở Google Docs trong chế độ ẩn (browser/docs_controller.py)
4. Người dùng chọn "Bắt đầu ghi âm" trên giao diện (ui/main_window.py)
5. Hệ thống kích hoạt Voice Typing trong Google Docs (browser/docs_controller.py)
6. Người dùng nói, Google Docs chuyển đổi thành văn bản
7. Ứng dụng trích xuất văn bản từ Google Docs (text/manager.py)
8. Người dùng di chuyển con trỏ đến vị trí muốn nhập
9. Chọn "Dán văn bản" hoặc sử dụng phím tắt (system/interaction.py)
10. Hệ thống tự động nhập văn bản vào vị trí con trỏ (system/interaction.py)
11. Quá trình tiếp tục cho đến khi người dùng chọn "Dừng"

## Ưu điểm của Kiến trúc này

- Tận dụng độ chính xác cao của Voice Typing Google Docs
- Không cần chi phí API riêng cho nhận dạng giọng nói
- Hỗ trợ nhiều ngôn ngữ, bao gồm tiếng Việt
- Tích hợp chặt chẽ với hệ sinh thái Google
- Bảo mật cao với xác thực OAuth 2.0
- Giao diện người dùng thân thiện và dễ sử dụng

## Hướng dẫn Phát triển

1. Cài đặt môi trường:
   ```
   python -m venv venv
   source venv/bin/activate  # Trên Windows: venv\Scripts\activate
   pip install PyQt6 google-auth google-auth-oauthlib selenium pyautogui rxpy cryptography structlog
   ```

2. Cấu trúc dự án:
   ```
   voicetyping/
   ├── main.py
   ├── ui/
   │   ├── main_window.py
   │   └── login_dialog.py
   ├── auth/
   │   └── google_auth.py
   ├── browser/
   │   └── docs_controller.py
   ├── text/
   │   └── manager.py
   ├── system/
   │   └── interaction.py
   ├── state/
   │   └── store.py
   └── utils/
       ├── security.py
       └── logger.py
   ```

3. Phát triển từng module theo cấu trúc trên
4. Sử dụng Git để quản lý phiên bản
5. Viết unit test cho mỗi module
6. Tạo tài liệu API và hướng dẫn sử dụng

## Lưu ý Triển khai

- Đảm bảo tuân thủ chính sách sử dụng của Google Docs
- Xử lý các trường hợp mất kết nối hoặc lỗi trình duyệt
- Tối ưu hóa việc sử dụng tài nguyên khi chạy trình duyệt ẩn
- Cập nhật thường xuyên ChromeDriver để tương thích với phiên bản Chrome mới nhất
- Thực hiện kiểm tra bảo mật và penetration testing định kỳ

## Các bước khởi chạy phần mềm

1. Cài đặt môi trường:
   ```
   python -m venv venv
   source venv/bin/activate  # Trên Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Cấu hình Google OAuth:
   - Tạo một dự án mới trên Google Cloud Console
   - Kích hoạt Google Docs API và Google Drive API
   - Tạo thông tin xác thực OAuth 2.0 và tải về file `client_secret.json`
   - Đặt file `client_secret.json` vào thư mục gốc của dự án

3. Cài đặt ChromeDriver:
   - Tải ChromeDriver phiên bản tương

With kiến trúc này, bạn có thể xây dựng một ứng dụng nhập liệu bằng giọng nói tiếng Việt hiệu quả, tận dụng sức mạnh của Google Docs Voice Typing và tích hợp chặt chẽ với hệ sinh thái Google.
