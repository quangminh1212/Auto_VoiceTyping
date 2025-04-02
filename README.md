# VoiceTyping
venv\Scripts\activate
deactivate
pyinstaller --onefile --windowed main.py   

VoiceTyping là một ứng dụng máy tính cho phép người dùng nhập văn bản bằng giọng nói tại vị trí con trỏ chuột, sử dụng công nghệ nhận dạng giọng nói của Google Speech Recognition.

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
- **Nhận dạng giọng nói:** SpeechRecognition với Google Speech API
- **Điều khiển con trỏ và nhập liệu:** PyAutoGUI, pyperclip, keyboard
- **Xử lý văn bản:** NLTK (Natural Language Toolkit)
- **Xử lý âm thanh:** PyAudio, pydub (yêu cầu FFmpeg)

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
│   └── __init__.py     # File khởi tạo module
│
├── main.py             # Điểm khởi đầu của ứng dụng
├── requirements.txt    # Danh sách các thư viện cần thiết
├── run.bat             # Script tự động cài đặt và chạy ứng dụng
├── README.md           # Tài liệu hướng dẫn sử dụng
└── .gitignore          # Cấu hình Git ignore

### Chi tiết chức năng:

1. Frontend:
   - `main_window.py`: Tạo giao diện chính của ứng dụng, bao gồm các nút điều khiển và hiển thị trạng thái.

2. Backend:
   - `recognizer.py`: Xử lý việc nhận dạng giọng nói, kết nối với Google Speech Recognition API.
   - `processor.py`: Xử lý và định dạng văn bản nhận được từ nhận dạng giọng nói.
   - `controller.py`: Điều khiển con trỏ chuột và thực hiện việc nhập liệu tại vị trí con trỏ.

3. File chính:
   - `main.py`: Điểm khởi đầu của ứng dụng, kết nối frontend và backend.
   - `requirements.txt`: Liệt kê các thư viện Python cần thiết cho dự án.
   - `run.bat`: Script tự động cài đặt môi trường và chạy ứng dụng.
   - `README.md`: Cung cấp thông tin về dự án và hướng dẫn sử dụng.

## Cài đặt và Sử dụng

### Phương pháp 1: Sử dụng script tự động (khuyến nghị)

1. **Tải và cài đặt Python**:
   - Tải [Python](https://www.python.org/downloads/) (khuyến nghị phiên bản 3.8 trở lên)
   - Khi cài đặt, đảm bảo chọn "Add Python to PATH"

2. **Tải và giải nén dự án**:
   - Tải về và giải nén dự án VoiceTyping vào thư mục tùy chọn

3. **Chạy file run.bat**:
   - Nhấp đúp vào file `run.bat` trong thư mục dự án
   - Script sẽ tự động tạo môi trường ảo, cài đặt các thư viện cần thiết và khởi động ứng dụng

### Phương pháp 2: Cài đặt thủ công

1. **Tạo và kích hoạt môi trường ảo**:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. **Cài đặt các thư viện cần thiết**:
   ```
   pip install -r requirements.txt
   ```

3. **Chạy ứng dụng**:
   ```
   python main.py
   ```

### Cài đặt FFmpeg cho Windows (bắt buộc cho nhận dạng giọng nói)

FFmpeg là một công cụ xử lý âm thanh và video cần thiết cho thư viện pydub để xử lý âm thanh từ microphone.

#### Cách 1: Sử dụng Chocolatey (đơn giản nhất)

1. Cài đặt [Chocolatey](https://chocolatey.org/install) (nếu chưa có)
2. Mở Command Prompt hoặc PowerShell với quyền Administrator
3. Chạy lệnh:
   ```
   choco install ffmpeg
   ```

#### Cách 2: Tải và cấu hình thủ công

1. Tải bản FFmpeg dành cho Windows từ [trang chính thức](https://ffmpeg.org/download.html#build-windows) hoặc từ [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (khuyến nghị tải bản "essentials")
2. Giải nén tệp đã tải vào thư mục, ví dụ: `C:\ffmpeg`
3. Thêm thư mục bin vào PATH hệ thống:
   - Mở Control Panel > System > Advanced System Settings > Environment Variables
   - Trong phần "System Variables", tìm biến "Path", nhấp vào Edit
   - Nhấp vào New và thêm đường dẫn đến thư mục bin, ví dụ: `C:\ffmpeg\bin`
   - Nhấp OK để lưu thay đổi

4. Kiểm tra cài đặt:
   - Mở Command Prompt và chạy lệnh: `ffmpeg -version`
   - Nếu hiện thông tin phiên bản FFmpeg, cài đặt đã thành công

#### Cách 3: Đặt tệp FFmpeg vào thư mục C:\ffmpeg\bin

1. Tải bản FFmpeg như hướng dẫn ở Cách 2
2. Tạo thư mục `C:\ffmpeg\bin`
3. Giải nén và đặt các file thực thi (`ffmpeg.exe`, `ffprobe.exe`, `ffplay.exe`) vào thư mục bin
4. Ứng dụng VoiceTyping sẽ tự động tìm FFmpeg tại đường dẫn này

### Cài đặt PyAudio (nếu gặp lỗi khi cài đặt từ requirements.txt)

PyAudio đôi khi gặp vấn đề khi cài đặt thông qua pip. Nếu gặp lỗi:

1. Tải PyAudio phù hợp với phiên bản Python và hệ điều hành từ [trang này](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Cài đặt thủ công:
   ```
   pip install [đường_dẫn_đến_file_whl_đã_tải]
   ```

## Sử dụng ứng dụng

1. Sau khi khởi động, chương trình sẽ hiển thị nút "Start"
2. Nhấn nút "Start" hoặc giữ phím Ctrl để bắt đầu nhận dạng giọng nói
3. Nói vào microphone, văn bản sẽ được nhận dạng và nhập vào vị trí con trỏ hiện tại
4. Nhấn nút "Stop" hoặc thả phím Ctrl để dừng nhận dạng giọng nói

### Xử lý lỗi thường gặp

- **Không tìm thấy FFmpeg**: Đảm bảo FFmpeg đã được cài đặt và thêm vào PATH hệ thống
- **Không tìm thấy microphone**: Kiểm tra microphone đã được kết nối và cài đặt đúng cách
- **Lỗi nhận dạng giọng nói**: Đảm bảo kết nối Internet ổn định (Google Speech API yêu cầu kết nối Internet)
- **Văn bản không xuất hiện tại vị trí con trỏ**: Kiểm tra ứng dụng đích có cho phép dán văn bản không

## Tài nguyên

- [Python](https://www.python.org/)
- [FFmpeg](https://ffmpeg.org/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [PyAutoGUI](https://pypi.org/project/PyAutoGUI/)
- [NLTK](https://www.nltk.org/)

## Đóng góp

Chúng tôi rất hoan nghênh sự đóng góp từ cộng đồng. Để đóng góp cho dự án:

1. Fork repository
2. Tạo nhánh mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi của bạn (`git commit -m 'Add some AmazingFeature'`)
4. Push lên nhánh (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm thông tin.