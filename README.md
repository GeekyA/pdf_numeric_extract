# PDF Text Extractor and Parser

A Python utility for extracting text from PDF documents using OCR (Optical Character Recognition) and parsing specific data types like prices, dates, and numeric values.

## Features

- High-resolution PDF page extraction (655 DPI)
- OCR text extraction using Tesseract
- Automated parsing of:
  - Price values
  - Dates in multiple formats
  - Numbers and numeric data
- Support for multi-page PDF documents
- Temporary image storage management

## Prerequisites

```bash
pip install pymupdf
pip install pytesseract
pip install Pillow
```

You must also have Tesseract OCR installed on your system:

- **Windows:** Download and install from [GitHub Tesseract Releases](https://github.com/UB-Mannheim/tesseract/wiki)
- **MacOS:** `brew install tesseract`
- **Linux:** `sudo apt-get install tesseract-ocr`

## Installation

1. Clone this repository or copy the script files to your project directory
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Open a terminal or command prompt.
   ```bash
   git clone https://github.com/GeekyA/pdf_numeric_extract.git
   ```
2. Navigate to the directory containing the script:
   ```bash
   cd pdf_numeric_extract
   ```
3. Run app.py
   ```bash
   python app.py
  ```


## Class Descriptions

### PDFTextExtractor

Handles the conversion of PDF pages to high-resolution images and performs OCR to extract text.

Parameters:
- `pdf_path`: Path to the PDF file
- `output_folder`: Directory for temporary image storage (default: 'temp', optional)

### TextParser

Provides static methods for parsing extracted text and identifying specific data types.

Parsed data includes:
- Prices (format: XX.XX)
- Dates (formats: MM/DD/YY, MM/DD/YYYY, Month DD, YYYY)
- Other numeric values

## Output Format

The parser returns a dictionary with the following structure:
```python
{
    "prices": [float],        # List of extracted price values
    "dates": [str],          # List of extracted dates
    "others": [str]          # List of other numeric values
}
```

## Notes

- The DPI is hardcoded to 655 for optimal OCR results
- Temporary images are saved in the specified output folder
- Make sure you have sufficient disk space for temporary image storage
- Larger PDFs may take longer to process due to high-resolution image conversion
