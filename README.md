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
## Usage on sample bill

1. Navigate to the directory containing the script:
   ```bash
   cd pdf_numeric_extract
   ```
2. Run app.py
   ```bash 
   python app.py
   ```

## Usage

```python
from pdf_extractor import PDFTextExtractor, TextParser

# Initialize the extractor with your PDF file
pdf_extractor = PDFTextExtractor('bill.pdf', 'output_folder')

# Extract text from all pages
extracted_text = pdf_extractor.extract_text()

# Combine all pages' text
full_text = '\n'.join(extracted_text)

# Parse the extracted text
parsed_data = TextParser.parse(full_text)

# Access the parsed data
print("Prices:", parsed_data["prices"])
print("Dates:", parsed_data["dates"])
print("Other Numbers:", parsed_data["others"])
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

Additionally, it now includes an LLM-powered parsing method.

## Output Format

The traditional parser returns a dictionary with the following structure:
```python
{
    "prices": [float],        # List of extracted price values
    "dates": [str],          # List of extracted dates
    "others": [str]          # List of other numeric values
}
```
Additionaly the LLM augmented response looks like this on the example bill.pdf

```python
{'prices': [{'total_amount_due': 108.82}, {'previous_balance': 103.61}, {'comcast_paydirect': -103.61}, {'new_charges': 108.82}, {'thank_you': 93.84}, {'other_charges_and_credits': 8.53}, {'taxes_surcharges_fees': 6.45}, {'total_new_charges': 108.82}, {'sarview_detal_total_amount_due': 108.82}, {'additional_outlet_01_08_to_07_video_prices': 9.95}, {'xfinity_tv': 93.84}, {'broadcast_tv_fee': 5.0}, {'franchise_related_cost': 0.53}, {'total_other_charges_credits': 8.53}, {'state_sales_tax': 0.02}, {'franchise_fee': 6.35}, {'federal_council_regulatory_fee': 0.08}, {'total_taxes_surcharges_fees': 6.45}], 'dates': [{'billing_date': '12/28/15'}, {'auto_pay': '01/12/16'}, {'autopay_payment': '01/12/16'}], 'others': [{'contact_us_url': 'https://www.xfinity.com'}, {'call_phone_number': '(1) 800-934-6489'}, {'payment_time': 'quick and convenient'}, {'copyright_symbol': '©'}, {'box_number': '6505'}, {'location': 'CHELMSFORD MA 01824-0000'}, {'call_to_request_monthly_bill_in_spanish_at': ''}, {'live_chat_link': '855-270-0379'}, {'phone_number': '+1 (555) 123-4567'}, {'contact_type': 'residential'}, {'business_type': 'real_estate'}]}
```

As you can see the result now has relevant field names for each value.
The LLM (Qwen/Qwen2.5-0.5B-Instruct) parses each line of text extracted by the OCR to reduce hallucinations and increase accuracy. Here's the prompt used to achieve the cleaning functionality
```python
prompt = f"""
    Extract the numerical value from the following unstructured text and convert it into a structured JSON format. 
    - The key should be a descriptive field name based on the text, written in snake_case.
    - The value should be the corresponding numerical value (as a float or integer).
    - Ensure the output is in this format: {{ "field_name": value }}

    Examples:
    1. Text: "Installation Charge - - - 150.00 is applicable for new connections."
   Output: {{ "installation_charge": 150.00 }}

    2. Text: "Late Payment Penalty ---------> 50 Only if paid after due date."
    Output: {{ "late_payment_penalty": 50 }}

    3. Text: "Electricity Duty: 7.25 is levied as per government norms."
    Output: {{ "electricity_duty": 7.25 }}

    4. Text: "Monthly Rental ========== 1200 per month for the plan."
    Output: {{ "monthly_rental": 1200 }}

    6. Text: "Due Date 12/28/15, please pay by this date."
    Output: {{ "due_date": "12/28/15" }}

    7. Text: "The total bill amount is $499.99, thank you for shopping with us."
    Output: {{ "total_bill_amount": 499.99 }}

    8. Text: "Phone Number: +1 (555) 123-4567 is registered with your account."
    Output: {{ "phone_number": "+1 (555) 123-4567" }}

    Now process the following text and generate the structured JSON format:

    Text: "{x}"
    """
```
There are some hallucinations and inaccuracy in the final result still due to a small model being used. The assignment was written by keeping in mind that it will probably be run on a standard computer and not on production grade GPUs. Proprietary models are not used either although a small experiment I conducted with claude produced good results.