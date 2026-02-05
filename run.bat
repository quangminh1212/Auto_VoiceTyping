@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo ===== CHUONG TRINH VOICETYPING =====
echo.

:: Sử dụng Python 3.13 cụ thể
set PYTHON_CMD=py -3.13
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI] Python 3.13 chua duoc cai dat!
    echo Hay cai dat tu: https://www.python.org/downloads/
    echo Hoac su dung: winget install Python.Python.3.13
    pause
    exit /b 1
)

:: Kiểm tra phiên bản Python
echo Dang kiem tra phien ban Python...
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYVER=%%i
echo Phien ban Python: %PYVER%

:: ===== KIỂM TRA VÀ TẠO LẠI VENV NẾU CẦN =====
set NEED_REBUILD=0

:: Kiểm tra venv có tồn tại không
if not exist venv\ (
    echo [INFO] Thu muc venv chua ton tai, se tao moi...
    set NEED_REBUILD=1
)

:: Kiểm tra venv có đúng phiên bản Python không
if exist venv\pyvenv.cfg (
    findstr /C:"3.13" venv\pyvenv.cfg >nul 2>&1
    if %errorlevel% neq 0 (
        echo [INFO] Venv dang dung phien ban Python khac, se tao lai...
        set NEED_REBUILD=1
    )
)

:: Nếu cần rebuild
if %NEED_REBUILD%==1 (
    echo.
    echo ====== DANG TAO LAI MOI TRUONG AO ======
    if exist venv\ (
        echo Dang xoa venv cu...
        rmdir /s /q venv
    )
    echo Dang tao venv moi voi Python 3.13...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo [LOI] Khong the tao moi truong ao.
        pause
        exit /b 1
    )
    echo [OK] Moi truong ao da duoc tao.
    echo ========================================
    echo.
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

:: ===== KIỂM TRA VÀ CẬP NHẬT DEPENDENCIES =====
echo Dang kiem tra dependencies...

:: Tạo hash của requirements.txt hiện tại
set "REQ_HASH_FILE=venv\.req_hash"
certutil -hashfile requirements.txt MD5 2>nul | findstr /v ":" > "%TEMP%\req_hash_new.txt"
set /p NEW_HASH=<"%TEMP%\req_hash_new.txt"

:: So sánh với hash cũ
set NEED_INSTALL=0
if not exist "%REQ_HASH_FILE%" (
    set NEED_INSTALL=1
) else (
    set /p OLD_HASH=<"%REQ_HASH_FILE%"
    if not "!NEW_HASH!"=="!OLD_HASH!" (
        echo [INFO] requirements.txt da thay doi, can cap nhat dependencies...
        set NEED_INSTALL=1
    )
)

:: Nếu cần rebuild hoặc requirements thay đổi
if %NEED_REBUILD%==1 set NEED_INSTALL=1

if %NEED_INSTALL%==1 (
    echo.
    echo ====== DANG CAI DAT DEPENDENCIES ======
    python -m pip install --quiet --upgrade pip >nul 2>nul
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [CANH BAO] Co loi khi cai dat dependencies.
    ) else (
        echo [OK] Tat ca dependencies da duoc cai dat.
        :: Lưu hash mới
        echo !NEW_HASH!> "%REQ_HASH_FILE%"
    )
    echo ========================================
    echo.
) else (
    echo [OK] Dependencies da duoc cai dat day du.
)

:: ===== XÓA CACHE PYTHON ĐỂ ĐẢM BẢO CODE MỚI =====
echo Dang xoa Python cache...
if exist backend\__pycache__ rmdir /s /q backend\__pycache__ 2>nul
if exist frontend\__pycache__ rmdir /s /q frontend\__pycache__ 2>nul
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
echo [OK] Cache da duoc xoa.

:: ===== KIỂM TRA THƯ VIỆN =====
echo.
echo Dang kiem tra cac thu vien chinh...
python -c "import pyaudio; print('[OK] PyAudio:', pyaudio.__version__)" 2>nul || echo [X] PyAudio khong hoat dong
python -c "import sounddevice; print('[OK] Sounddevice hoat dong')" 2>nul || echo [X] Sounddevice khong hoat dong
python -c "import PyQt5; print('[OK] PyQt5 hoat dong')" 2>nul || echo [X] PyQt5 khong hoat dong
python -c "import speech_recognition; print('[OK] SpeechRecognition hoat dong')" 2>nul || echo [X] SpeechRecognition khong hoat dong

:: ===== CHẠY CHƯƠNG TRÌNH =====
set PYTHONWARNINGS=ignore::DeprecationWarning
echo.
echo ====================================
echo VOICETYPING - San sang!
echo ------------------------------------
echo  Nhan giu Alt : Bat dau noi
echo  Tha Alt      : Ket thuc va paste
echo  Nut X        : Thoat ung dung
echo ====================================
echo.
python -W ignore::DeprecationWarning main.py

:: Chờ để người dùng xem được kết quả
echo.
echo Chuong trinh da ket thuc.
pause