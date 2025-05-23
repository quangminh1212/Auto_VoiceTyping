@echo off
echo ===== CHUONG TRINH VOICETYPING =====
echo.

:: Kiểm tra và tạo môi trường ảo nếu chưa tồn tại
if not exist venv\ (
    echo Dang tao moi truong ao Python...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [LOI] Khong the tao moi truong ao. Hay kiem tra Python da duoc cai dat chua.
        pause
        exit /b 1
    )
    echo Moi truong ao da duoc tao thanh cong.
)

:: Kích hoạt môi trường ảo
echo Dang kich hoat moi truong ao...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [LOI] Khong the kich hoat moi truong ao.
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

:: Dọn dẹp các gói không hợp lệ và ẩn cảnh báo
echo Dang nang cap pip va don dep goi khong hop le...
pip install --quiet --upgrade pip >nul 2>nul
:: Tắt hiển thị cảnh báo và chỉ hiển thị lỗi
set PYTHONWARNINGS=ignore

:: Cài đặt các thư viện từ requirements.txt (ẩn cảnh báo)
echo Dang cai dat cac thu vien can thiet...
pip install -r requirements.txt 2>pip_error.log
if %errorlevel% neq 0 (
    echo [LOI] Khong the cai dat cac thu vien. Xem chi tiet trong file pip_error.log
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
        echo [OK] Da tim thay FFmpeg tai C:\ffmpeg\bin
        set "PATH=C:\ffmpeg\bin;%PATH%"
    ) else (
        echo [CANH BAO] FFmpeg khong duoc tim thay! Nhan dang giong noi se khong hoat dong.
    )
) else (
    echo [OK] Da tim thay FFmpeg trong PATH he thong.
)

:: Khởi tạo NLTK data nếu cần (ẩn cảnh báo)
echo Dang khoi tao NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); print('[OK] Da cai dat NLTK data.')" 2>nul

:: Kiểm tra PyAudio
echo Dang kiem tra PyAudio...
python -c "import pyaudio; print('[OK] PyAudio hoat dong.')" 2>nul
if %errorlevel% neq 0 (
    echo [CANH BAO] PyAudio khong hoat dong, co the can cai dat thu cong.
    echo Tai tai https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
)

:: Bỏ tắt cảnh báo nghiêm trọng khi chạy chương trình chính, nhưng vẫn ẩn DeprecationWarning
set PYTHONWARNINGS=ignore::DeprecationWarning

:: Tạo file .pth để ẩn cảnh báo từ PyQt5
if not exist venv\Lib\site-packages\suppress_warnings.pth (
    echo Dang tao file de an canh bao PyQt5...
    echo import warnings >> venv\Lib\site-packages\suppress_warnings.py
    echo warnings.filterwarnings("ignore", category=DeprecationWarning) >> venv\Lib\site-packages\suppress_warnings.py
    echo from suppress_warnings import * > venv\Lib\site-packages\suppress_warnings.pth
)

:: Chạy chương trình chính
echo.
echo Dang khoi dong chuong trinh...
python -W ignore::DeprecationWarning main.py

:: Chờ để người dùng xem được kết quả
echo.
echo Chuong trinh da ket thuc.
pause 