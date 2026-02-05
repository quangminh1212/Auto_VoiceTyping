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
pip install --quiet --upgrade pip >nul 2>nul

:: Cài đặt các thư viện cơ bản từ requirements.txt
echo Dang cai dat cac thu vien can thiet...
pip install -r requirements.txt 2>pip_error.log
if %errorlevel% neq 0 (
    echo [CANH BAO] Co mot so thu vien khong cai duoc. Xem chi tiet trong file pip_error.log
)

:: Cài đặt PyAudio - thử nhiều cách
echo Dang cai dat PyAudio...
python -c "import pyaudio" 2>nul
if %errorlevel% neq 0 (
    echo PyAudio chua duoc cai dat, dang thu cac phuong phap...
    
    :: Phương pháp 1: Thử pip thông thường
    pip install pyaudio 2>nul
    if %errorlevel% neq 0 (
        echo [INFO] Pip khong the cai dat PyAudio, thu dung pipwin...
        
        :: Phương pháp 2: Thử pipwin
        pip install pipwin 2>nul
        pipwin install pyaudio 2>nul
        
        if %errorlevel% neq 0 (
            echo [CANH BAO] Khong the cai dat PyAudio tu dong.
            echo.
            echo De cai dat PyAudio thu cong:
            echo 1. Tai file .whl tu: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
            echo 2. Chon phien ban phu hop voi Python cua ban
            echo 3. Chay: pip install [ten_file.whl]
            echo.
            echo Hoac su dung Python 3.13 hoac thap hon de co wheel san.
            echo.
        ) else (
            echo [OK] Da cai dat PyAudio thanh cong qua pipwin.
        )
    ) else (
        echo [OK] Da cai dat PyAudio thanh cong qua pip.
    )
) else (
    echo [OK] PyAudio da duoc cai dat.
)

:: Kiểm tra lại PyAudio
python -c "import pyaudio; print('[OK] PyAudio hoat dong binh thuong.')" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [CANH BAO] PyAudio khong hoat dong! Chuc nang nhan dang giong noi se khong lam viec.
    echo Hay cai dat PyAudio thu cong hoac su dung Python 3.13 tro xuong.
    echo.
)

:: Bỏ ẩn các cảnh báo quan trọng khi chạy chương trình
set PYTHONWARNINGS=ignore::DeprecationWarning

:: Chạy chương trình chính
echo.
echo Dang khoi dong chuong trinh...
python -W ignore::DeprecationWarning main.py

:: Chờ để người dùng xem được kết quả
echo.
echo Chuong trinh da ket thuc.
pause