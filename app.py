import streamlit as st
import fitz  # PyMuPDF
import io

# 1. Page Configuration & Layout
st.set_page_config(
    page_title="Flipkart 4x6 Label Cropper",
    page_icon="📦",
    layout="centered"
)

# 2. Custom CSS Styling (UI ko clean aur modern banane ke liye)
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2e7d32;
        font-weight: bold;
    }
    .sub-text {
        text-align: center;
        color: #555555;
        font-size: 16px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown("<h1 class='main-header'>📦 Flipkart Thermal Label Cropper</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Apni Bulk Shipping Labels PDF upload karein aur <b>4x6 inch</b> Thermal Sticker ready PDF download karein.</p>", unsafe_allow_html=True)

st.divider()

# 4. File Upload Section
uploaded_file = st.file_uploader("📂 Merged PDF File Upload Karein", type=["pdf"])

if uploaded_file is not None:
    st.success(f"📄 File Selected: **{uploaded_file.name}**")
    
    # Process Button
    if st.button("✂️ Crop & Generate 4x6 Labels", type="primary", use_container_width=True):
        with st.spinner("Labels Crop Ho Rahe Hain, Kripya Wait Karein..."):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            total_pages = len(doc)
            new_doc = fitz.open()

            # 4x6 inch standard thermal size in points
            TARGET_WIDTH = 4 * 72   # 288 pt
            TARGET_HEIGHT = 6 * 72  # 432 pt

            for page_num in range(total_pages):
                page = doc[page_num]
                page.set_rotation(0)
                rect = page.rect

                # Exact tested crop coordinates
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

            st.balloons()  # Success Animation
            st.success(f"🎉 Total **{total_pages}** Labels Successfully Process Ho Gaye!")
            
            st.download_button(
                label="⬇️ Download 4x6 Thermal PDF",
                data=output_buffer.getvalue(),
                file_name=f"Cropped_4x6_{uploaded_file.name}",
                mime="application/pdf",
                use_container_width=True
            )

# Sidebar Guidance
st.sidebar.title("📌 Instructions")
st.sidebar.info("""
1. Direct Flipkart / Merged PDF file upload karein.
2. **Crop & Generate** button par click karein.
3. Downloaded PDF ko direct 4x6 Thermal Printer se print karein.
""")