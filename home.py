import os
import streamlit as st
import tempfile
import uuid
from PIL import Image
from imgconverter import ImageConverter

# Cấu hình trang
st.set_page_config(
    page_icon='🔄',
    page_title='File Converter - Designed by oce',
    layout="wide", initial_sidebar_state="auto"
)
st.markdown(
    """
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    """,
    unsafe_allow_html=True
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
                file_ext = file_uploaded.name.split('.')[-1]
                temp_path = os.path.join(tempfile.gettempdir(), f"oceconvert_{uuid.uuid4()}.{file_ext}")

                with open(temp_path, 'wb') as f:
                    f.write(file_uploaded.getbuffer())

                success, result = ImageConverter.file_convert(temp_path, output)

                if os.path.exists(temp_path):
                    os.remove(temp_path)

                if success and os.path.exists(result):
                    st.success('Hoàn thành')
                    mime_map = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}
                    mime_type = mime_map.get(output.lower(), f'image/{output.lower()}')

                    with open(result, 'rb') as f:
                        st.download_button(label='Tải xuống', data=f, file_name=os.path.basename(result), mime=mime_type)
                    
                    os.remove(result)
                else:
                    st.error('Đã xảy ra lỗi, có thể file không hỗ trợ cho định dạng nay, vui lòng thử lại hoặc chuyển sang định dạng khác')

with tab2:
    st.header('Chuyển đổi tài liệu')
    st.info('Under construction')

with tab3:
    st.header('Chuyển đổi âm thanh')
    st.info('Under construction')

with tab4:
    st.header('Chuyển đổi video')
    st.info('Under construction')
