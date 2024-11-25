import os
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from infer_llm import run_llm_on_text

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
    
    @staticmethod
    def parse_llm_dict(data_dict):
        result = {
        "prices": [],
        "dates": [],
        "others": []
    }

        for key, value in data_dict.items():
            # Prices
            if isinstance(value, (float, int)) and round(value, 2) == value:
                result["prices"].append({key: float(value)})
            
            # Dates
            if isinstance(value, str) and ('/' in value or ',' in value):
                date_match = re.search(r'\d{2}/\d{2}/\d{2,4}|\w{3,9}\s\d{1,2},\s\d{4}', value)
                if date_match:
                    result["dates"].append({key: date_match.group()})
            
            # Others with numbers
        for key, value in data_dict.items():
            if isinstance(value, str):
                if {key: value} not in result['prices'] and {key: value} not in result['dates']:
                    result["others"].append({key: value})

        return result
    
    def parse_by_llm(self, text):
        resp = run_llm_on_text(page_text.splitlines())
        resp = self.parse_llm_dict(resp)
        return resp


# Usage example:
if __name__ == "__main__":
    pdf_extractor = PDFTextExtractor('bill.pdf')
    extracted_text = pdf_extractor.extract_text()
    page_text = '\n'.join(extracted_text)

    parsed_data = TextParser().parse_by_llm(page_text)
    print(parsed_data)
