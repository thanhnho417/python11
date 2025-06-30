from pydub import AudioSegment
import os
import tempfile
import uuid

class AudioConverter:
    @staticmethod
    def get_audio_file_supported():
        return ['mp3', 'flac', 'wav', 'ogg']

    @staticmethod
    def convert(input, input_format, output_format, output_path=None):
        try:
            if input_format.lower() not in AudioConverter.get_audio_file_supported():
                return False, 'Xin lỗi, định dạng file không hỗ trợ'

            audio = AudioSegment.from_file(input, format=input_format)

            if output_path is None:
                temp_dir = tempfile.gettempdir()
                output_path = os.path.join(
                    temp_dir, f'ocefileconverter-{uuid.uuid4()}.{output_format}'
                )

            audio.export(output_path, format=output_format)

            return True, output_path  # ✅ Trả về đường dẫn file thay vì object
        except Exception as e:
            return False, str(e)
