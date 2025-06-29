import os
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from docx import Document
import pandas as pd

class FileConverter:
    def __init__(self):
        self.supported_conversations = {
            'image': ['jpg', 'png', 'bmp', 'gif'],
        }