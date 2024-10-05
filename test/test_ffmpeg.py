import os
import sys
from pydub import AudioSegment
import warnings

# Chỉ định đường dẫn đến FFmpeg
ffmpeg_path = r"C:\ffmpeg\bin"

# Thêm đường dẫn FFmpeg vào PATH
if ffmpeg_path not in os.environ["PATH"]:
    os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]

# Cấu hình pydub
AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffmpeg = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")

# Kiểm tra xem FFmpeg có tồn tại không
if not os.path.exists(AudioSegment.converter):
    print(f"Không tìm thấy FFmpeg tại {AudioSegment.converter}")
    sys.exit(1)

# Tắt cảnh báo từ pydub
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub.utils")

# Tạo một đoạn âm thanh trống để kiểm tra
audio = AudioSegment.silent(duration=1000)
audio.export("test.mp3", format="mp3")

print("FFmpeg hoạt động bình thường!")
