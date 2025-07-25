from pdf2image import convert_from_path, convert_from_bytes
from PIL import ImageChops
import sys

def compare_pdfs(pdf_a_path, pdf_b_path, dpi=300):
    print("🔍 Konverterar PDF till bilder...")

    with open(pdf_a_path, "rb") as f1, open(pdf_b_path, "rb") as f2:
        images_a = convert_from_bytes(f1.read(), dpi=dpi)
        images_b = convert_from_bytes(f2.read(), dpi=dpi)

    num_pages = min(len(images_a), len(images_b))

    for i in range(num_pages):
        img_a = images_a[i].convert("RGB")
        img_b = images_b[i].convert("RGB")

        if img_a.size != img_b.size:
            print(f"Sida {i+1}: Olika storlek → Skillnad!")
            continue

        diff = ImageChops.difference(img_a, img_b)
        diff_score = sum(sum(pixel) for pixel in diff.getdata())
        print(f"Sida {i+1}: diff_score = {diff_score}")

        # Spara diffbild om det finns skillnad
        if diff_score > 0:
            print(f"⚠️ Skillnad hittad på sida {i+1}, sparar diffbild...")
            diff.save(f"diff_page_{i+1}.png")
            img_a.save(f"page_{i+1}_A.png")
            img_b.save(f"page_{i+1}_B.png")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Använd: python test_compare.py path_till_pdf_A path_till_pdf_B")
        sys.exit(1)

    compare_pdfs(sys.argv[1], sys.argv[2])

