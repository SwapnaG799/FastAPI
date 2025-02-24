from fastapi import FastAPI
import pdfplumber

app=FastAPI()

def extract_text_from_pdf(pdf_path):
    """Extracts all text content from a PDF file."""
    extracted_text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() + "\n\n"  # Extract text from each page
    
    return extracted_text

# ✅ Path to the uploaded PDF
pdf_file_path = "C:/Users/swapn/OneDrive/Desktop/FastAPI/task2/DOEA - 701B-Comprehensive Assessment Form v1.pdf"

# ✅ Extract text from PDF
extracted_text = extract_text_from_pdf(pdf_file_path)


print(extracted_text)

with open("extracted_text.txt", "w", encoding="utf-8") as file:
    file.write(extracted_text)
