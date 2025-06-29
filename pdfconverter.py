from PyPDF2 import PdfReader
from docx import Document
import os

class PdfConverter:
    @staticmethod
    def get_pdf_format_supported():
        return {
            'pdf_to_txt': 'Chuyển đổi PDF sang văn bản thuần (txt)',
            'pdf_to_docx': 'Chuyển đổi PDF sang Word (docx)'
        }
    
    @staticmethod
    def pdf_to_txt(input, output=None):
        try:
            if output is None:
                output = os.path.splitext(input)[0]+'.txt'
            
            with open(input, 'rb') as pdffile:
                reader = PdfReader(pdffile)
                text = '\n'.join([page.extract_text() for page in reader.pages])

                with open (output, 'w', encoding='UTF-8') as txtfile:
                    txtfile.write(text)
            
            return True, output
        except Exception as e:
            return False, str(e)