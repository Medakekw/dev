from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageEnhance
import io


pdf_path = input('Where is your pdf located?')
reader = PdfReader(pdf_path)
writer = PdfWriter()


def enhance_image_quality(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)  # Enhance sharpness
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)  # Enhance contrast
    output = io.BytesIO()
    image.save(output, format='PNG')
    return output.getvalue()

for page_num in range(len(reader.pages)):
    page = reader.pages[page_num]
    # Extract images from the page, if any
    try:
        page_images = page['/Resources']['/XObject'].get('/Im', {})
        if isinstance(page_images, dict):
            for img_key, img_obj in page_images.items():
                img_data = img_obj.getData()
                enhanced_img = enhance_image_quality(img_data)
                img_obj._data = enhanced_img  
    except Exception as e:
        continue
    writer.add_page(page)

enhanced_pdf_path = input("Where do you want to save the enhanced pdf?")
with open(enhanced_pdf_path, 'wb') as f:
    writer.write(f)

enhanced_pdf_path