import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="4x6 Shipping Label Cropper", page_icon="📦", layout="centered")

st.title("📦 4x6 Thermal Label Cropper")
st.write("Apni PDF upload karein aur instant 4x6 thermal printable PDF download karein.")

uploaded_file = st.file_uploader("Merged PDF File Choose Karein", type=["pdf"])

if uploaded_file is not None:
    st.info(f"File Uploaded: **{uploaded_file.name}**")
    
    if st.button("Crop & Process Labels", type="primary"):
        with st.spinner("Labels Crop Ho Rahe Hain..."):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            total_pages = len(doc)  # doc close hone se pehle count store kar liya
            new_doc = fitz.open()

            TARGET_WIDTH = 4 * 72   # 288 pt
            TARGET_HEIGHT = 6 * 72  # 432 pt

            for page_num in range(total_pages):
                page = doc[page_num]
                page.set_rotation(0)
                rect = page.rect

                crop_box = fitz.Rect(
                    rect.width * 0.32,
                    rect.height * 0.03,
                    rect.width * 0.68,
                    rect.height * 0.46
                )

                new_page = new_doc.new_page(width=TARGET_WIDTH, height=TARGET_HEIGHT)
                new_page.show_pdf_page(
                    fitz.Rect(0, 0, TARGET_WIDTH, TARGET_HEIGHT),
                    doc,
                    page_num,
                    clip=crop_box
                )

            output_buffer = io.BytesIO()
            new_doc.save(output_buffer)
            new_doc.close()
            doc.close()

            st.success(f"✅ Total {total_pages} Labels Process Ho Gaye!")
            
            st.download_button(
                label="⬇️ Final 4x6 PDF Download Karein",
                data=output_buffer.getvalue(),
                file_name=f"4x6_{uploaded_file.name}",
                mime="application/pdf"
            )