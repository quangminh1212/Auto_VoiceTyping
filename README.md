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

### Chi tiết các tầng

1. Giao diện Người Dùng (UI Layer)
   - PyQt6 cho giao diện đồ họa
   - QML cho thiết kế giao diện linh hoạt
   - Các thành phần: Đăng nhập, Bắt đầu/Dừng ghi âm, Hiển thị trạng thái, Cài đặt

2. Tầng Xác thực (Authentication Layer)
   - Sử dụng Google OAuth 2.0 để đăng nhập
   - Lưu trữ token an toàn bằng cryptography
   - Tự động làm mới token khi hết hạn

3. Tầng Điều khiển Trình duyệt (Browser Automation Layer)
   - Sử dụng Selenium với ChromeDriver
   - Mở và điều khiển Google Docs trong chế độ ẩn (headless)
   - Kích hoạt và quản lý tính năng Voice Typing

4. Tầng Quản lý Văn bản (Text Management Layer)
   - Trích xuất văn bản từ Google Docs
   - Xử lý và định dạng văn bản
   - Tích hợp với clipboard hệ thống

5. Tầng Tương tác Hệ thống (System Interaction Layer)
   - PyAutoGUI để mô phỏng nhập liệu
   - Xác định vị trí con trỏ và ứng dụng đang active
   - Hỗ trợ các phím tắt tùy chỉnh

6. Tầng Quản lý Trạng thái (State Management Layer)
   - Sử dụng RxPY để quản lý luồng dữ liệu và sự kiện
   - Xử lý bất đồng bộ với asyncio
   - Đảm bảo tính nhất quán giữa các tầng

7. Tầng Bảo mật và Xử lý Lỗi (Security and Error Handling Layer)
   - Mã hóa dữ liệu nhạy cảm với cryptography
   - Logging cấu trúc với structlog
   - Xử lý lỗi toàn diện và thông báo người dùng

## Luồng Hoạt động Tổng thể

1. Người dùng khởi động ứng dụng
2. Đăng nhập bằng tài khoản Google
3. Ứng dụng mở Google Docs trong chế độ ẩn
4. Người dùng chọn "Bắt đầu ghi âm"
5. Hệ thống kích hoạt Voice Typing trong Google Docs
6. Người dùng nói, Google Docs chuyển đổi thành văn bản
7. Ứng dụng trích xuất văn bản từ Google Docs
8. Người dùng di chuyển con trỏ đến vị trí muốn nhập
9. Chọn "Dán văn bản" hoặc sử dụng phím tắt
10. Hệ thống tự động nhập văn bản vào vị trí con trỏ
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

Với kiến trúc này, bạn có thể xây dựng một ứng dụng nhập liệu bằng giọng nói tiếng Việt hiệu quả, tận dụng sức mạnh của Google Docs Voice Typing và tích hợp chặt chẽ với hệ sinh thái Google.