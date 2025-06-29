import os
import subprocess
import tempfile
import streamlit as st
from PIL import Image
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import ffmpeg

# Thiết lập trang Streamlit
st.set_page_config(
    page_title="File Converter - Designed by oce",
    page_icon="🔄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==============================================
# PHẦN 1: CÁC LỚP CHUYỂN ĐỔI
# ==============================================

class ImageConverter:
    @staticmethod
    def get_supported_formats():
        return ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp']
    
    @staticmethod
    def convert(input_path, output_format):
        try:
            supported_formats = ImageConverter.get_supported_formats()
            if output_format.lower() not in supported_formats:
                return False, f"Định dạng {output_format} không được hỗ trợ. Hỗ trợ: {', '.join(supported_formats)}"
            
            with Image.open(input_path) as img:
                # Tạo file tạm cho output
                with tempfile.NamedTemporaryFile(suffix=f'.{output_format}', delete=False) as tmp_file:
                    output_path = tmp_file.name
                
                # Lưu ảnh với định dạng mới
                img.save(output_path)
                return True, output_path
        except Exception as e:
            return False, f"Lỗi khi chuyển đổi ảnh: {str(e)}"

class PdfConverter:
    @staticmethod
    def get_supported_conversions():
        return {
            'pdf_to_txt': 'Văn bản TXT',
            'pdf_to_docx': 'Tài liệu Word'
        }
    
    @staticmethod
    def pdf_to_txt(input_path):
        try:
            # Tạo file tạm cho output
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
                output_path = tmp_file.name
            
            with open(input_path, 'rb') as pdf_file:
                reader = PdfReader(pdf_file)
                text = "\n".join([page.extract_text() or "" for page in reader.pages])
                
                with open(output_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text)
            
            return True, output_path
        except Exception as e:
            return False, f"Lỗi khi chuyển đổi PDF sang TXT: {str(e)}"
    
    @staticmethod
    def pdf_to_docx(input_path):
        try:
            # Tạo file tạm cho output
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
                output_path = tmp_file.name
            
            doc = Document()
            with open(input_path, 'rb') as pdf_file:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    text = page.extract_text() or ""
                    doc.add_paragraph(text)
            
            doc.save(output_path)
            return True, output_path
        except Exception as e:
            return False, f"Lỗi khi chuyển đổi PDF sang DOCX: {str(e)}"

class DataConverter:
    @staticmethod
    def get_supported_formats():
        return ['csv', 'xlsx', 'json', 'xml']
    
    @staticmethod
    def convert(input_path, output_format):
        try:
            input_ext = os.path.splitext(input_path)[1][1:].lower()
            output_format = output_format.lower()
            supported_formats = DataConverter.get_supported_formats()
            
            if input_ext not in supported_formats:
                return False, f"Định dạng đầu vào {input_ext} không được hỗ trợ. Hỗ trợ: {', '.join(supported_formats)}"
            
            if output_format not in supported_formats:
                return False, f"Định dạng đầu ra {output_format} không được hỗ trợ. Hỗ trợ: {', '.join(supported_formats)}"
            
            # Đọc file đầu vào
            if input_ext == 'csv':
                df = pd.read_csv(input_path)
            elif input_ext in ['xls', 'xlsx']:
                df = pd.read_excel(input_path)
            elif input_ext == 'json':
                df = pd.read_json(input_path)
            elif input_ext == 'xml':
                df = pd.read_xml(input_path)
            
            # Tạo file tạm cho output
            with tempfile.NamedTemporaryFile(suffix=f'.{output_format}', delete=False) as tmp_file:
                output_path = tmp_file.name
            
            # Ghi file đầu ra
            if output_format == 'csv':
                df.to_csv(output_path, index=False)
            elif output_format == 'xlsx':
                df.to_excel(output_path, index=False)
            elif output_format == 'json':
                df.to_json(output_path, orient='records', indent=2)
            elif output_format == 'xml':
                df.to_xml(output_path, index=False)
            
            return True, output_path
        except Exception as e:
            return False, f"Lỗi khi chuyển đổi dữ liệu: {str(e)}"

class MediaConverter:
    @staticmethod
    def get_supported_formats():
        return {
            'audio': ['mp3', 'wav', 'aac', 'ogg', 'flac', 'm4a'],
            'video': ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm']
        }
    
    @staticmethod
    def check_ffmpeg_installed():
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    @staticmethod
    def convert(input_path, output_format):
        try:
            if not MediaConverter.check_ffmpeg_installed():
                return False, "FFmpeg chưa được cài đặt. Vui lòng cài đặt FFmpeg trước khi sử dụng."
            
            supported = MediaConverter.get_supported_formats()
            all_supported = supported['audio'] + supported['video']
            
            if output_format.lower() not in all_supported:
                return False, f"Định dạng {output_format} không được hỗ trợ. Hỗ trợ: {', '.join(all_supported)}"
            
            # Tạo file tạm cho output
            with tempfile.NamedTemporaryFile(suffix=f'.{output_format}', delete=False) as tmp_file:
                output_path = tmp_file.name
            
            # Thực hiện chuyển đổi
            (
                ffmpeg
                .input(input_path)
                .output(output_path)
                .run(overwrite_output=True, quiet=True)
            )
            
            return True, output_path
        except ffmpeg.Error as e:
            return False, f"Lỗi FFmpeg: {e.stderr.decode('utf-8')}"
        except Exception as e:
            return False, f"Lỗi khi chuyển đổi media: {str(e)}"
    
    @staticmethod
    def extract_audio(input_path, output_format='mp3'):
        try:
            if not MediaConverter.check_ffmpeg_installed():
                return False, "FFmpeg chưa được cài đặt. Vui lòng cài đặt FFmpeg trước khi sử dụng."
            
            if output_format.lower() not in MediaConverter.get_supported_formats()['audio']:
                return False, f"Định dạng audio {output_format} không được hỗ trợ."
            
            # Tạo file tạm cho output
            with tempfile.NamedTemporaryFile(suffix=f'.{output_format}', delete=False) as tmp_file:
                output_path = tmp_file.name
            
            # Thực hiện trích xuất audio
            (
                ffmpeg
                .input(input_path)
                .output(output_path, acodec='copy' if output_format in ['mp3', 'aac'] else None)
                .run(overwrite_output=True, quiet=True)
            )
            
            return True, output_path
        except ffmpeg.Error as e:
            return False, f"Lỗi FFmpeg: {e.stderr.decode('utf-8')}"
        except Exception as e:
            return False, f"Lỗi khi trích xuất audio: {str(e)}"

# ==============================================
# PHẦN 2: GIAO DIỆN STREAMLIT
# ==============================================

def main():
    # Tiêu đề ứng dụng
    st.title("🔄 Công Cụ Chuyển Đổi File Tất-trong-Một")
    st.markdown("""
    Chọn loại file bạn muốn chuyển đổi và làm theo hướng dẫn. 
    Công cụ hỗ trợ chuyển đổi hình ảnh, tài liệu, dữ liệu và đa phương tiện.
    """)
    
    # Sidebar với thông tin ứng dụng
    with st.sidebar:
        st.header("ℹ️ Thông tin")
        st.markdown("""
        **Các tính năng chính:**
        - 🖼️ Chuyển đổi hình ảnh (JPG, PNG, GIF, BMP, WEBP)
        - 📄 Chuyển đổi PDF (sang TXT hoặc DOCX)
        - 📊 Chuyển đổi dữ liệu (CSV, Excel, JSON, XML)
        - 🎵 Chuyển đổi đa phương tiện (audio/video)
        """)
        
        st.markdown("---")
        st.markdown("**Lưu ý quan trọng:**")
        st.markdown("- Đối với chuyển đổi đa phương tiện, cần cài đặt FFmpeg")
        st.markdown("- File tạm sẽ tự động xóa sau khi chuyển đổi")
        
        st.markdown("---")
        st.markdown("**Hướng dẫn cài đặt FFmpeg:**")
        st.markdown("- Windows: Tải từ [ffmpeg.org](https://ffmpeg.org/)")
        st.markdown("- MacOS: `brew install ffmpeg`")
        st.markdown("- Linux (Ubuntu/Debian): `sudo apt install ffmpeg`")
    
    # Tạo các tab chức năng
    tab1, tab2, tab3, tab4 = st.tabs([
        "🖼️ Hình Ảnh", 
        "📄 PDF", 
        "📊 Dữ Liệu", 
        "🎵 Đa Phương Tiện"
    ])
    
    # Tab chuyển đổi hình ảnh
    with tab1:
        st.header("Chuyển Đổi Hình Ảnh")
        st.markdown("Hỗ trợ chuyển đổi giữa các định dạng hình ảnh phổ biến.")
        
        uploaded_file = st.file_uploader(
            "Tải lên file ảnh", 
            type=ImageConverter.get_supported_formats(),
            key="image_uploader"
        )
        
        if uploaded_file:
            col1, col2 = st.columns(2)
            with col1:
                st.image(uploaded_file, caption="Ảnh đã tải lên", use_column_width=True)
            
            with col2:
                output_format = st.selectbox(
                    "Chọn định dạng đầu ra",
                    options=[f for f in ImageConverter.get_supported_formats() if f != uploaded_file.name.split('.')[-1].lower()],
                    key="image_output_format"
                )
                
                if st.button("🔄 Chuyển Đổi Ảnh", key="convert_image_btn"):
                    with st.spinner("Đang xử lý..."):
                        # Lưu file tạm
                        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                            temp_path = tmp_file.name
                            tmp_file.write(uploaded_file.getbuffer())
                        
                        # Thực hiện chuyển đổi
                        success, result = ImageConverter.convert(temp_path, output_format)
                        
                        # Xóa file tạm đầu vào
                        os.unlink(temp_path)
                        
                        if success:
                            st.success("✅ Chuyển đổi thành công!")
                            
                            # Hiển thị ảnh kết quả
                            try:
                                with Image.open(result) as img:
                                    st.image(img, caption=f"Ảnh đã chuyển đổi (.{output_format})", use_column_width=True)
                            except:
                                pass
                            
                            # Nút tải xuống
                            with open(result, "rb") as f:
                                st.download_button(
                                    label="⬇️ Tải file đã chuyển đổi",
                                    data=f,
                                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}.{output_format}",
                                    mime=f"image/{output_format.lower()}"
                                )
                            
                            # Xóa file kết quả
                            os.unlink(result)
                        else:
                            st.error(f"❌ {result}")
    
    # Tab chuyển đổi PDF
    with tab2:
        st.header("Chuyển Đổi PDF")
        st.markdown("Hỗ trợ chuyển đổi PDF sang các định dạng văn bản khác.")
        
        uploaded_pdf = st.file_uploader(
            "Tải lên file PDF", 
            type=["pdf"],
            key="pdf_uploader"
        )
        
        if uploaded_pdf:
            st.markdown(f"**File đã tải lên:** `{uploaded_pdf.name}`")
            
            conversion_type = st.radio(
                "Chọn loại chuyển đổi",
                options=list(PdfConverter.get_supported_conversions().values()),
                key="pdf_conversion_type"
            )
            
            if st.button("🔄 Chuyển Đổi PDF", key="convert_pdf_btn"):
                with st.spinner("Đang xử lý..."):
                    # Lưu file tạm
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        temp_path = tmp_file.name
                        tmp_file.write(uploaded_pdf.getbuffer())
                    
                    # Xác định loại chuyển đổi
                    conversions = PdfConverter.get_supported_conversions()
                    reverse_conversions = {v: k for k, v in conversions.items()}
                    conversion_key = reverse_conversions[conversion_type]
                    
                    # Thực hiện chuyển đổi
                    if conversion_key == "pdf_to_txt":
                        success, result = PdfConverter.pdf_to_txt(temp_path)
                        mime_type = "text/plain"
                        preview_content = open(result, 'r', encoding='utf-8').read(1000) + "..." if os.path.getsize(result) > 1000 else open(result, 'r', encoding='utf-8').read()
                    else:
                        success, result = PdfConverter.pdf_to_docx(temp_path)
                        mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        preview_content = "[Nội dung DOCX không thể xem trước]"
                    
                    # Xóa file tạm đầu vào
                    os.unlink(temp_path)
                    
                    if success:
                        st.success("✅ Chuyển đổi thành công!")
                        
                        # Hiển thị xem trước
                        with st.expander("Xem trước nội dung (phần đầu)"):
                            st.code(preview_content)
                        
                        # Nút tải xuống
                        with open(result, "rb") as f:
                            st.download_button(
                                label="⬇️ Tải file đã chuyển đổi",
                                data=f,
                                file_name=f"{os.path.splitext(uploaded_pdf.name)[0]}.{result.split('.')[-1]}",
                                mime=mime_type
                            )
                        
                        # Xóa file kết quả
                        os.unlink(result)
                    else:
                        st.error(f"❌ {result}")
    
    # Tab chuyển đổi dữ liệu
    with tab3:
        st.header("Chuyển Đổi Dữ Liệu")
        st.markdown("Hỗ trợ chuyển đổi giữa các định dạng dữ liệu phổ biến.")
        
        uploaded_data = st.file_uploader(
            "Tải lên file dữ liệu", 
            type=DataConverter.get_supported_formats(),
            key="data_uploader"
        )
        
        if uploaded_data:
            st.markdown(f"**File đã tải lên:** `{uploaded_data.name}`")
            
            input_ext = uploaded_data.name.split(".")[-1].lower()
            supported_output = [f for f in DataConverter.get_supported_formats() if f != input_ext]
            
            output_format = st.selectbox(
                "Chọn định dạng đầu ra",
                options=supported_output,
                key="data_output_format"
            )
            
            if st.button("🔄 Chuyển Đổi Dữ Liệu", key="convert_data_btn"):
                with st.spinner("Đang xử lý..."):
                    # Lưu file tạm
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        temp_path = tmp_file.name
                        tmp_file.write(uploaded_data.getbuffer())
                    
                    # Thực hiện chuyển đổi
                    success, result = DataConverter.convert(temp_path, output_format)
                    
                    # Xóa file tạm đầu vào
                    os.unlink(temp_path)
                    
                    if success:
                        st.success("✅ Chuyển đổi thành công!")
                        
                        # Hiển thị xem trước
                        try:
                            if output_format == 'csv':
                                preview_df = pd.read_csv(result)
                            elif output_format == 'xlsx':
                                preview_df = pd.read_excel(result)
                            elif output_format == 'json':
                                preview_df = pd.read_json(result)
                            elif output_format == 'xml':
                                preview_df = pd.read_xml(result)
                            
                            with st.expander("Xem trước dữ liệu (10 dòng đầu)"):
                                st.dataframe(preview_df.head(10))
                        except:
                            pass
                        
                        # Nút tải xuống
                        with open(result, "rb") as f:
                            st.download_button(
                                label="⬇️ Tải file đã chuyển đổi",
                                data=f,
                                file_name=f"{os.path.splitext(uploaded_data.name)[0]}.{output_format}",
                                mime={
                                    "csv": "text/csv",
                                    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    "json": "application/json",
                                    "xml": "application/xml"
                                }.get(output_format.lower(), "application/octet-stream")
                            )
                        
                        # Xóa file kết quả
                        os.unlink(result)
                    else:
                        st.error(f"❌ {result}")
    
    # Tab chuyển đổi đa phương tiện
    with tab4:
        st.header("Chuyển Đổi Đa Phương Tiện")
        st.markdown("Hỗ trợ chuyển đổi giữa các định dạng audio/video và trích xuất audio từ video.")
        
        if not MediaConverter.check_ffmpeg_installed():
            st.warning("⚠️ FFmpeg chưa được cài đặt. Chức năng này có thể không hoạt động.")
        
        uploaded_media = st.file_uploader(
            "Tải lên file đa phương tiện", 
            type=MediaConverter.get_supported_formats()['audio'] + MediaConverter.get_supported_formats()['video'],
            key="media_uploader"
        )
        
        if uploaded_media:
            st.markdown(f"**File đã tải lên:** `{uploaded_media.name}`")
            
            file_ext = uploaded_media.name.split(".")[-1].lower()
            is_video = file_ext in MediaConverter.get_supported_formats()['video']
            
            if is_video:
                st.video(uploaded_media)
                action = st.radio(
                    "Bạn muốn:",
                    options=["Chuyển đổi video sang định dạng khác", "Trích xuất audio từ video"],
                    key="media_action"
                )
            else:
                st.audio(uploaded_media)
                action = "Chuyển đổi audio sang định dạng khác"
            
            if "Trích xuất" in action:
                output_format = st.selectbox(
                    "Chọn định dạng audio đầu ra",
                    options=MediaConverter.get_supported_formats()['audio'],
                    key="audio_extract_format"
                )
            else:
                all_formats = MediaConverter.get_supported_formats()['audio'] + MediaConverter.get_supported_formats()['video']
                output_format = st.selectbox(
                    "Chọn định dạng đầu ra",
                    options=[f for f in all_formats if f != file_ext],
                    key="media_output_format"
                )
            
            if st.button("🔄 Chuyển Đổi", key="convert_media_btn"):
                with st.spinner("Đang xử lý..."):
                    # Lưu file tạm
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        temp_path = tmp_file.name
                        tmp_file.write(uploaded_media.getbuffer())
                    
                    # Thực hiện chuyển đổi
                    if "Trích xuất" in action:
                        success, result = MediaConverter.extract_audio(temp_path, output_format)
                        media_type = "audio"
                    else:
                        success, result = MediaConverter.convert(temp_path, output_format)
                        media_type = "video" if output_format in MediaConverter.get_supported_formats()['video'] else "audio"
                    
                    # Xóa file tạm đầu vào
                    os.unlink(temp_path)
                    
                    if success:
                        st.success("✅ Chuyển đổi thành công!")
                        
                        # Hiển thị xem trước
                        if media_type == "video":
                            st.video(result)
                        else:
                            st.audio(result)
                        
                        # Nút tải xuống
                        with open(result, "rb") as f:
                            st.download_button(
                                label="⬇️ Tải file đã chuyển đổi",
                                data=f,
                                file_name=f"{os.path.splitext(uploaded_media.name)[0]}.{output_format}",
                                mime={
                                    "mp3": "audio/mpeg",
                                    "wav": "audio/wav",
                                    "mp4": "video/mp4",
                                    "avi": "video/x-msvideo",
                                    "mov": "video/quicktime"
                                }.get(output_format.lower(), "application/octet-stream")
                            )
                        
                        # Xóa file kết quả
                        os.unlink(result)
                    else:
                        st.error(f"❌ {result}")

if __name__ == "__main__":
    main()