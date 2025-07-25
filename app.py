import streamlit as st
from pdf2image import convert_from_bytes
from PIL import ImageChops

st.set_page_config(page_title="Testa bilddiff", layout="wide")
st.title("🧪 Testa pixeljämförelse mellan två PDF:er")

file1 = st.file_uploader("Ladda upp version A (PDF)", type=["pdf"])
file2 = st.file_uploader("Ladda upp version B (PDF)", type=["pdf"])

def compare_pdfs_bytes(pdf_a_bytes, pdf_b_bytes):
    st.markdown("🔍 Kör jämförelse…")
    images_a = convert_from_bytes(pdf_a_bytes, dpi=300)
    images_b = convert_from_bytes(pdf_b_bytes, dpi=300)

    for i, (img_a, img_b) in enumerate(zip(images_a, images_b)):
        img_a = img_a.convert("RGB")
        img_b = img_b.convert("RGB")
        if img_a.size != img_b.size:
            st.error(f"Sida {i+1}: Olika storlek")
            continue

        diff = ImageChops.difference(img_a, img_b)
        diff_score = sum(sum(px) for px in diff.getdata())

        st.markdown(f"### Sida {i+1}")
        st.write(f"🔬 Diff-score: `{diff_score}`")
        if diff_score > 0:
            col1, col2 = st.columns(2)
            col1.image(img_a, caption="Version A")
            col2.image(img_b, caption="Version B")
            st.image(diff, caption="🔍 Visuell skillnad (diff)")
        else:
            st.success("Ingen visuell skillnad")

if file1 and file2:
    compare_pdfs_bytes(file1.read(), file2.read())
