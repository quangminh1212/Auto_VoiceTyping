@echo off
chcp 65001 >nul
echo ===== CHUONG TRINH VOICETYPING =====
echo.

:: Sử dụng Python 3.13 cụ thể
set PYTHON_CMD=py -3.13
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI] Python 3.13 chua duoc cai dat!
    echo Hay cai dat tu: https://www.python.org/downloads/release/python-3130/
    echo Hoac su dung: winget install Python.Python.3.13
    pause
    exit /b 1
)

:: Kiểm tra phiên bản Python
echo Dang kiem tra phien ban Python...
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYVER=%%i
echo Phien ban Python: %PYVER%

:: Kiểm tra và tạo môi trường ảo nếu chưa tồn tại
if not exist venv\ (
    echo Dang tao moi truong ao Python 3.13...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo [LOI] Khong the tao moi truong ao.
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

:: Kiểm tra PyAudio
echo Dang kiem tra PyAudio...
python -c "import pyaudio; print('[OK] PyAudio version:', pyaudio.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo [CANH BAO] PyAudio chua duoc cai dat!
    pip install pyaudio
)

:: Kiểm tra sounddevice (backup)
echo Dang kiem tra Sounddevice...
python -c "import sounddevice; print('[OK] Sounddevice hoat dong.')" 2>nul
if %errorlevel% neq 0 (
    pip install sounddevice 2>nul
)

:: Bỏ ẩn các cảnh báo quan trọng khi chạy chương trình
set PYTHONWARNINGS=ignore::DeprecationWarning

:: Chạy chương trình chính
echo.
echo ====================================
echo Dang khoi dong chuong trinh...
echo Nhan giu phim Alt de noi.
echo Nhan nut X de thoat.
echo ====================================
echo.
python -W ignore::DeprecationWarning main.py

:: Chờ để người dùng xem được kết quả
echo.
echo Chuong trinh da ket thuc.
pause