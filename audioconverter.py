from pydub import AudioSegment
import os
class AudioConverter:
    @staticmethod
    def get_audio_file_supported():
        return ['mp3', 'flac', 'wav', 'ogg']
    
    @staticmethod
    def audioconverter(input,input_format, output_format, output_path='oceconveter-'):
        try:
            if input not in AudioConverter.get_audio_file_supported():
                return False, 'Xin lỗi, định dạng file không hỗ trợ'
            audio = AudioSegment.from_file(input, format=input_format)
            output_file = f'{output_path}.{output_format}'
            audio.export(output_file, format=output_format)
            
            return True, output_file
        except Exception as e:
            return False, str(e)