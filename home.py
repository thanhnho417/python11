import os
import streamlit as st
import pandas as pd
from PIL import Image
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import ffmpeg
from imgconverter import ImageConverter
import pdfconverter
#Chương trình chính
st.set_page_config(
    page_icon='🔄',
    page_title='File Converter - Designed by oce',
    layout='wide'
)
st.title('File Converter - Công cụ chuyển đổi định dạng File')
st.subheader('Chọn chức năng')
tab1, tab2, tab3, tab4 = st.tabs(['Hình ảnh', 'Tài liệu', 'Âm thanh', 'Video'])


with tab1:
    st.header('Chuyển đổi hình ảnh')
    file_uploaded = st.file_uploader('Tải ảnh lên', type=ImageConverter.get_file_format_supported())
    if file_uploaded:
        st.image(file_uploaded, caption='Ảnh muốn chuyển đổi', width=200)
        output = st.selectbox('Chọn định dạng đầu ra:', ImageConverter.get_file_format_supported())
        if st.button('Chuyển đổi ảnh'):
            with st.spinner('Đang xử lí...'):
                temp_path = f'oceconvert'
                with open(temp_path, 'wb') as f:
                    f.write(file_uploaded.getbuffer())
                
                success, result = ImageConverter.file_convert(temp_path,output)

                os.remove(temp_path)

                if success:
                    st.success('Hoàn thành')
                    with open (result, 'rb') as f:
                        st.download_button(label='Tải xuống', data=f,file_name=os.path.basename(result), mime=f'image/{output.lower()}')
                    os.remove(result)
                else:
                    st.error('Đã xảy ra lỗi, vui lòng thử lại')


with tab2:
    st.header('Chuyển đổi tài liệu')
    st.info('Under construction')

with tab3:
    st.header('Chuyển đổi âm thanh')
    st.info('Under construction')

with tab4:
    st.header('Chuyển đổi video')
    st.info('Under construction')
