import os
import warnings

# Tắt cảnh báo từ pydub
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub.utils")

# Chỉ định đường dẫn đến FFmpeg
ffmpeg_path = r"C:\ffmpeg\bin"

# Thêm đường dẫn FFmpeg vào đầu PATH
os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]
