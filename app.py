import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageChops
import io

st.set_page_config(page_title="PDF-bildjämförelse utan Poppler", layout="wide")
st.title("🧪 Jämför två PDF:er (pixel-för-pixel)")

file1 = st.file_uploader("Ladda upp version A (PDF)", type=["pdf"])
file2 = st.file_uploader("Ladda upp version B (PDF)", type=["pdf"])

def pdf_to_images(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        images.append(img)
    return images

def compare_images(img1, img2):
    diff = ImageChops.difference(img1, img2)
    diff_score = sum(sum(p) for p in diff.getdata())
    return diff, diff_score

if file1 and file2:
    st.info("Kör jämförelse... detta kan ta någon sekund")
    images_a = pdf_to_images(file1.read())
    images_b = pdf_to_images(file2.read())

    num_pages = min(len(images_a), len(images_b))
    for i in range(num_pages):
        img_a = images_a[i]
        img_b = images_b[i]

        st.subheader(f"Sida {i+1}")
        if img_a.size != img_b.size:
            st.error("❌ Olika storlek på sidor")
            continue

        diff_img, score = compare_images(img_a, img_b)
        st.write(f"🔬 Diff-score: `{score}`")

        if score > 0:
            col1, col2 = st.columns(2)
            col1.image(img_a, caption="Version A")
            col2.image(img_b, caption="Version B")
            st.image(diff_img, caption="🔍 Skillnader")
        else:
            st.success("Ingen visuell skillnad")
