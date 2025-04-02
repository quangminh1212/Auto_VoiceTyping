@echo off
echo ===== CHUONG TRINH VOICETYPING =====
echo.

:: Kiểm tra và tạo môi trường ảo nếu chưa tồn tại
if not exist venv\ (
    echo Dang tao moi truong ao Python...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [LỖI] Khong the tao moi truong ao. Hay kiem tra Python da duoc cai dat chua.
        pause
        exit /b 1
    )
    echo Moi truong ao da duoc tao thanh cong.
)

:: Kích hoạt môi trường ảo
echo Dang kich hoat moi truong ao...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [LỖI] Khong the kich hoat moi truong ao.
    pause
    exit /b 1
)

:: Sao chép file requirements.txt từ thư mục dist nếu không có ở thư mục gốc
if not exist requirements.txt (
    if exist dist\requirements.txt (
        echo Dang sao chep file requirements.txt tu thu muc dist...
        copy dist\requirements.txt .
    ) else (
        echo Tao file requirements.txt moi...
        echo PyQt5==5.15.6 > requirements.txt
        echo pyautogui==0.9.53 >> requirements.txt
        echo pyperclip==1.9.0 >> requirements.txt
        echo keyboard==0.13.5 >> requirements.txt
        echo SpeechRecognition==3.8.1 >> requirements.txt
        echo pydub==0.25.1 >> requirements.txt
        echo nltk==3.6.5 >> requirements.txt
        echo PyAudio==0.2.14 >> requirements.txt
    )
)

:: Cài đặt các thư viện từ requirements.txt
echo Dang cai dat cac thu vien can thiet...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [LỖI] Khong the cai dat cac thu vien. 
    echo Hay thu cai dat thu cong: pip install PyQt5 pyautogui pyperclip keyboard SpeechRecognition pydub
    pause
    exit /b 1
)

:: Kiểm tra xem FFmpeg đã được cài đặt chưa
echo Dang kiem tra FFmpeg...
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo [CANH BAO] Khong tim thay FFmpeg trong PATH.
    echo Chuc nang nhan dang giong noi co the khong hoat dong.
    echo Hay tai FFmpeg tu https://ffmpeg.org/download.html va them vao PATH he thong.
    
    :: Kiểm tra thư mục C:\ffmpeg\bin
    if exist "C:\ffmpeg\bin\ffmpeg.exe" (
        echo Da tim thay FFmpeg tai C:\ffmpeg\bin
        set "PATH=C:\ffmpeg\bin;%PATH%"
    )
)

:: Chạy chương trình chính
echo.
echo Dang khoi dong chuong trinh...
python main.py

:: Chờ để người dùng xem được kết quả
echo.
echo Chuong trinh da ket thuc.
pause 