import os
import streamlit as st
import tempfile
import uuid
from PIL import Image
from imgconverter import ImageConverter
import zipfile
import io
# Cấu hình trang
st.set_page_config(
    page_icon='🔄',
    page_title='File Converter - Designed by oce',
    layout="wide", initial_sidebar_state="auto"
)
st.title('File Converter - Công cụ chuyển đổi định dạng File')
st.subheader('Chọn chức năng')
tab1, tab2, tab3, tab4 = st.tabs(['Hình ảnh', 'Tài liệu', 'Âm thanh', 'Video'])

with tab1:
    st.header('Chuyển đổi hình ảnh')
    files_uploaded = st.file_uploader('Tải ảnh lên', type=ImageConverter.get_file_format_supported(), accept_multiple_files=True)

    if files_uploaded:
        cols = st.columns(len(files_uploaded))
        for col, file in zip(cols,files_uploaded):
            col.image(file, caption=file.name, width=200)
            
            
            
        output = st.selectbox('Chọn định dạng đầu ra cho tất cả ảnh:', ImageConverter.get_file_format_supported())
        if st.button('Chuyển đổi'):
            converted_file = []
            with st.spinner('Đang xử lí...'):
                mine_map = {
                    'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
                    'png': 'image/png', 'webp': 'image/webp'
                }
                
                for file in files_uploaded:
                    file_ext = file.name.split('.')[-1]
                    temp_input_path = os.path.join(tempfile.gettempdir(), f'oceconvert_{uuid.uuid4()}.{file_ext}')
                    
                    with open(temp_input_path, 'wb') as f:
                        f.write(file.getbuffer())
                    success, result_path = ImageConverter.file_convert(temp_input_path, output)
                    
                    if os.path.exists(temp_input_path):
                        os.remove(temp_input_path)
                        
                    if success and os.path.exists(result_path):
                        
                        mine_type = mine_map.get(output.lower(), f'image/{output.lower()}')
                        converted_file.append((os.path.splitext(file.name)[0], result_path))
                    else: st.error(f'Lỗi chuyển đổi file {file.name}')
                    
                if converted_file:
                    zip = io.BytesIO()
                    with zipfile.ZipFile(zip, 'w') as zipf:
                        for base, file_path in converted_file:
                            arcname = f'{base}.{output}'
                            zipf.write(file_path, arcname=arcname)
                            os.remove(file_path)
                    
                    zip.seek(0)
                    st.download_button(label='Tải xuống toàn bộ', data=zip, file_name='ocefileconverter.zip', mime='application/zip')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
with tab2:
    st.header('Chuyển đổi tài liệu')
    st.info('Under construction')

with tab3:
    st.header('Chuyển đổi âm thanh')
    st.info('Under construction')

with tab4:
    st.header('Chuyển đổi video')
    st.info('Under construction')
