from fastapi import FastAPI
import PyPDF2
import os  # Import os for file checking

app = FastAPI()

def extract_pdf_form_fields(pdf_path):
    """Extract form fields from a PDF, with error handling for missing files."""
    if not os.path.exists(pdf_path):
        return {"error": f"File not found: {pdf_path}"}

    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        # Extract form fields
        fields = reader.get_fields()
        if fields:
            form_fields = {
                key: (value.get('/V', 'N/A') if isinstance(value, dict) else 'N/A')
                for key, value in fields.items()
            }
            return form_fields
        else:
            return {"message": "No form fields found in the PDF"}

# ✅ Corrected file path (remove "file:///" and use proper spacing)
pdf_file_path = "C:/Users/swapn/OneDrive/Desktop/FastAPI/task2/5000-3008 Medical Certification Form.pdf"

# Extract form fields and values
fields = extract_pdf_form_fields(pdf_file_path)

# Print results
if isinstance(fields, dict) and "error" in fields:
    print(fields["error"])
else:
    for name, value in fields.items():
        print(f"{name}: {value}")
