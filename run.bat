@echo off
chcp 65001 >nul
echo ===== CHUONG TRINH VOICETYPING =====
echo.

:: Kiểm tra phiên bản Python
echo Dang kiem tra phien ban Python...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo Phien ban Python: %PYVER%

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

:: Tắt hiển thị cảnh báo
set PYTHONWARNINGS=ignore

:: Nâng cấp pip
echo Dang nang cap pip...
python -m pip install --quiet --upgrade pip >nul 2>nul

:: Cài đặt các thư viện từ requirements.txt
echo Dang cai dat cac thu vien can thiet...
pip install -r requirements.txt 2>nul
if %errorlevel% neq 0 (
    echo [CANH BAO] Co mot so thu vien khong cai duoc.
)

:: Kiểm tra sounddevice (thay thế PyAudio)
echo Dang kiem tra thu vien am thanh...
python -c "import sounddevice; print('[OK] Sounddevice hoat dong binh thuong.')" 2>nul
if %errorlevel% neq 0 (
    echo [CANH BAO] Sounddevice chua duoc cai dat!
    pip install sounddevice
)

:: Bỏ ẩn các cảnh báo quan trọng khi chạy chương trình
set PYTHONWARNINGS=ignore::DeprecationWarning

:: Chạy chương trình chính
echo.
echo Dang khoi dong chuong trinh...
echo Nhan giu phim Alt de noi. Nhan nut X de thoat.
echo.
python -W ignore::DeprecationWarning main.py

:: Chờ để người dùng xem được kết quả
echo.
echo Chuong trinh da ket thuc.
pause