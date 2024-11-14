import os
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

class PDFTextExtractor:
    def __init__(self, pdf_path, output_folder='temp'):
        self.pdf_path = pdf_path
        self.output_folder = output_folder
        self.text_by_page = []

    def extract_text(self):
        os.makedirs(self.output_folder, exist_ok=True)
        doc = fitz.open(self.pdf_path)

        # Hardcoding DPI to 655
        dpi = 655
        scale_factor = dpi / 72  # 72 is the default DPI
        
        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)  # Load page
            
            # Create transformation matrix with scaling based on DPI
            matrix = fitz.Matrix(scale_factor, scale_factor)
            
            # Render page to image with the scaling matrix
            pix = page.get_pixmap(matrix=matrix)
            
            image_path = os.path.join(self.output_folder, f'page_{page_number + 1}.png')
            pix.save(image_path)  # Save the image of the page

            # Use pytesseract to extract text from the image
            text = pytesseract.image_to_string(Image.open(image_path))
            self.text_by_page.append(text)
        
        return self.text_by_page

class TextParser:
    @staticmethod
    def tok_has_num(x):
        return any(c.isdigit() for c in x)

    @staticmethod
    def parse(text):
        prices_pattern = r'-?\d+\.\d{2}'
        dates_pattern = r'\d{2}/\d{2}/\d{2,4}|\w{3,9}\s\d{1,2},\s\d{4}'
        prices = [float(i) for i in re.findall(prices_pattern, text)]
        dates = set(re.findall(dates_pattern, text))
        price_set = set(map(str, prices))

        tokens = [i for i in text.split() if i not in dates and i not in price_set]
        others = [i for i in tokens if TextParser.tok_has_num(i) and '$' not in i]

        return {
            "prices": prices,
            "dates": list(dates),
            "others": list(set(others))
        }

# Usage example:
if __name__ == "__main__":
    pdf_extractor = PDFTextExtractor('bill.pdf', 'outs')
    extracted_text = pdf_extractor.extract_text()
    page_text = '\n'.join(extracted_text)

    parsed_data = TextParser.parse(page_text)
    print(parsed_data)
