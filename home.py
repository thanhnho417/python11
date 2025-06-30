import os
import io
import uuid
import zipfile
import tempfile
import streamlit as st
from PIL import Image
from imgconverter import ImageConverter
from audioconverter import AudioConverter

# Cấu hình giao diện
st.set_page_config(
    page_title='File Converter - Designed by oce',
    page_icon='🔄',
    layout='wide'
)
st.title('File Converter - Công cụ chuyển đổi định dạng File')
st.subheader('Chọn chức năng')
tab1, tab2, tab3, tab4 = st.tabs(['Hình ảnh', 'Tài liệu', 'Âm thanh', 'Video'])

# -------------------- HÀM CHUYỂN ĐỔI CHUNG --------------------
def convert_and_zip(files, convert_func, output_ext, zip_filename, needs_input_ext=False):
    results = []

    for file in files:
        file_ext = os.path.splitext(file.name)[-1].lstrip('.')
        base_name = os.path.splitext(file.name)[0]
        temp_input = os.path.join(tempfile.gettempdir(), f'{uuid.uuid4()}.{file_ext}')

        with open(temp_input, 'wb') as f:
            f.write(file.getbuffer())

        if needs_input_ext:
            success, result_path = convert_func(temp_input, file_ext, output_ext)
        else:
            success, result_path = convert_func(temp_input, output_ext)

        if os.path.exists(temp_input):
            os.remove(temp_input)

        if success and os.path.exists(result_path):
            results.append((base_name, result_path))
        else:
            st.error(f'Lỗi chuyển đổi file: {file.name}')

    if results:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for base, path in results:
                zipf.write(path, arcname=f'{base}.{output_ext}')
                os.remove(path)
        zip_buffer.seek(0)
        st.success(f'Chuyển đổi thành công {len(results)} file.')
        st.download_button('Tải xuống', zip_buffer, file_name=zip_filename, mime='application/zip')
    else:
        st.error('Không có file nào được chuyển đổi thành công.')

# -------------------- TAB 1: HÌNH ẢNH --------------------
with tab1:
    st.header('Chuyển đổi hình ảnh')
    img_formats = ImageConverter.get_file_format_supported()
    img_files = st.file_uploader('Tải ảnh lên', type=img_formats, accept_multiple_files=True)

    if img_files:
        st.image(img_files, width=200, caption=[file.name for file in img_files])
        output_format = st.selectbox('Chọn định dạng đầu ra:', img_formats)
        if st.button('Chuyển đổi ảnh'):
            with st.spinner('Đang xử lý...'):
                convert_and_zip(
                    img_files,
                    ImageConverter.file_convert,
                    output_format,
                    zip_filename='converted_images.zip',
                    needs_input_ext=False
                )
    else:
        st.warning("Chưa có ảnh nào được tải lên.")

# -------------------- TAB 2: TÀI LIỆU --------------------
with tab2:
    st.header('Chuyển đổi tài liệu')
    st.warning('Tính năng đang phát triển, vui lòng quay lại sau.')

# -------------------- TAB 3: ÂM THANH --------------------
with tab3:
    st.header('Chuyển đổi âm thanh')
    audio_formats = AudioConverter.get_audio_file_supported()
    audio_files = st.file_uploader('Tải file âm thanh lên', type=audio_formats, accept_multiple_files=True)

    if audio_files:
        st.info('Tải lên thành công')
        audio_output = st.selectbox('Chọn định dạng đầu ra:', audio_formats)
        if st.button('Chuyển đổi âm thanh'):
            with st.spinner('Đang xử lý...'):
                convert_and_zip(
                    audio_files,
                    AudioConverter.convert,
                    audio_output,
                    zip_filename='converted_audio.zip',
                    needs_input_ext=True
                )
    else:
        st.warning("Chưa có file âm thanh nào được tải lên.")

# -------------------- TAB 4: VIDEO --------------------
with tab4:
    st.header('Chuyển đổi video')
    st.warning('Tính năng đang phát triển, vui lòng quay lại sau.')
