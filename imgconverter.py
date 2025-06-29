from PIL import Image
import os

class ImageConverter:
    @staticmethod
    def get_file_format_supported():
        return ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp']
    @staticmethod
    def file_convert(input, output):
        try:
            if output.lower() not in ImageConverter.get_file_format_supported():
                return False, "Rất tiếc, định dạng file không hỗ trợ"
            img = Image.open(input)
            out_path = os.path.splitext(input)[0] + f'.{output.lower()}'
            img.save(out_path)
            return True, out_path
        except Exception as e:
            return False, str(e)