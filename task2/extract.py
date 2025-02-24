from fastapi import FastAPI, File
import PyPDF2
import os
from io import BytesIO
from PIL import Image

app = FastAPI()

def extract_pdf_data(pdf_path, image_folder="extracted_images"):
    """Extract form fields, text, and images from a PDF file."""
    extracted_data = {
        "form_fields": {},
        "text": "",
        "images": []
    }

    if not os.path.exists(pdf_path):
        return {"error": f"File not found: {pdf_path}"}

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        fields = reader.get_fields()
        if fields:
            extracted_data["form_fields"] = {
                key: (value.get('/V', 'N/A') if isinstance(value, dict) else 'N/A')
                for key, value in fields.items()
            }

        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_data["text"] += f"Page {page_num + 1}:\n{text}\n\n"

            if "/XObject" in page["/Resources"]:
                x_objects = page["/Resources"]["/XObject"].get_object()
                for obj in x_objects:
                    if x_objects[obj]["/Subtype"] == "/Image":
                        image_data = x_objects[obj]._data
                        image_ext = ".jpg" if x_objects[obj]["/ColorSpace"] == "/DeviceRGB" else ".png"
                        image_name = f"{image_folder}/image_{page_num+1}_{obj}{image_ext}"
                        
                        with open(image_name, "wb") as img_file:
                            img_file.write(image_data)

                        extracted_data["images"].append(image_name)

    return extracted_data

pdf_file_path = "C:/Users/swapn/OneDrive/Desktop/FastAPI/task2/5000-3008 Medical Certification Form.pdf"

pdf_data = extract_pdf_data(pdf_file_path)


with open("extracted_text.txt", "w", encoding="utf-8") as file:
    file.write(pdf_data["text"])

print(f"✅ Extracted text saved to extracted_text.txt")
print(f"✅ Extracted images saved in extracted_images folder")
print(f"✅ Form Fields: {pdf_data['form_fields']}")
