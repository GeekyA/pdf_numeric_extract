# PDF Text Extractor and Parser

A Python utility for extracting text from PDF documents using OCR (Optical Character Recognition) and parsing specific data types like prices, dates, and numeric values.

## Features

- High-resolution PDF page extraction (655 DPI)
- OCR text extraction using Tesseract
- [Parsing the text into a structured format with an LLM](#output-format)
- Automated parsing of:
  - Price values
  - Dates in multiple formats
  - Numbers and numeric data
- Support for multi-page PDF documents
- Temporary image storage management

## Prerequisites

```bash
pip install pillow==11.0.0
pip install pytesseract==0.3.13
pip install PyMuPDF==1.24.13
pip install transformers==4.46.3
pip install accelerate==1.1.1
pip install tqdm==4.67.1
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

# Parse the extracted text using LLM
parsed_data = TextParser().parse(page_text)

# or parse the values without i.e LLMs without descriptive fields
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
Account Number

Billing Date 12/28/15
Total Amount Due $108.82

(com ca st SAMPLE CUSTOMER BILL

Auto Pay 01/12/16
Page 1 of 2
Contact us:@)www.xfinity.com (Q1-800-XFINITY (1-800-934-6489)

Monthly Statement Summary

Previous Balance | 103.61
| Comcast Paydirect - 12/12/15 -103.61
eae New Charges - see below 108.82
Total Amount Due $108.82
Auto Pay 01/12/16
News from Comcast
New Charges Summary

Thank you for your prompt payment. For quick and convenient ©) XFINITY TV 93.84

ways to manage your account, view and pay your bill, please
visit www.xfinity.com/myaccount Other Charges & Credits 8.53
Taxes, Surcharges & Fees 6.45
Total New Charges $108.82

Thank you for being a valued Comcast

customer!

(comcast Account Number
Auto Pay 01/12/16
Total Amount Due $108.82
BOX 6505 CHELMSFORD MA 01824-0000

Autopay Payment Will Be Made On '01/12/16'

COMCAST
PO BOX 1577
NEWARK NJ 07101-1577

SAMPLE CUSTOMER BILL

SAMPLE CUSTOMER BILL
i comcast Account Number

Billing Date 12/28/15
Servies Detail Total Amount Due $108.82
ervice Vetalls Auto Pay 01/12/16

Page 2 of 2

Contact us: (@) www.xfinity.com (91-800-xFINITY (1-800-934-6489)

CCD <i coi
Questions about your bill or service? Call Comcast at

Digital Starter 01/08 - 02/07 69.95 1-888-633-4266 with any question about your bill or problems

with any of your Comcast services. FOR RESIDENTIAL

CUSTOMERS: Billing disputes must be received within sixty

Includes: Digital Starter Programming,

Interactive Program Guide, And Music (60)days from the due date of this bill. After you have contacted
Choice, Expanded Basic Service, Limited us, if you are not satisfied with our resolution of a problem with
__Basic Service , Digital Converter& Remote. your video service, or, if you have a complaint regarding our
Additional Outlet 01/08 - 02/07 9.95 video prices, you may contact the MA Department of
= Telecommunications and Cable - Consumer Division, 1000
Digital Converter Washington St., Boston, MA 02118-6500. Call 617-305-3531 or
HD Technology Fee 01/08 - 02/07 9.95 800-392-6066 or Email: consumer.complaints@state.ma.us.

ae Smo a ee a eal The Local Franchise Authority for video service is the MA DTC

saiareiebaiaiins O06 - ano? 3.99 at the above address. The FCC ID for your town is: MA0117.
Digital Adapter
Total XFINITY TV $93.84 The Broadcast TV fee recovers a portion of the cost of

retransmitting television broadcast signals.

Other Charges & Credits Regional Sports Fee recovers a portion of the costs to transmit

certain regional sports networks.

Broadcast TV Fee 5.00
Regional SportsFee = = = = 3.00 Only XFINITY® gives you the First Bilingual Experience of its
Franchise Related Cost 0.53 kind. Call today to request your monthly bill in Spanish at
Sea eileen nee on eee Se ee 1-800-XFINITY.
Total Other Charges & Credits $8.53
Moving? Call 1-855-MOV-EDGE or visit
Taxes, Surcharges & Fees http://www.xfinity.com/moversedge today! The XFINITY Movers
Edge program makes it easy to stay connected to your TV,
TV Internet, and Voice service.
State Sales Tax 0.02
Franchise Fee 6.35
FCC Regulatory Fee 0.08
Total Taxes, Surcharges & Fees $6.45

For closed captioning concerns and other accessibility
issues affecting customers with disabilities, call
855-270-0379, go online for a live chat at
www.comcastsupport.com/accessibility or

email accessibility@comcast.com or write to Comcast Your nearest Comcast Service Center:
1701 John F Kennedy Bivd., Phila. PA 19103-2838 Newton - 300 Needham St., M-F 10am-6pm, Sat
Attn: K. Wilkinson, or fax: 1-888-612-7402. 9am-5pm;
Watertown - 104 Main St., M-F 9am-1:30pm, 2pm-5pm
Hearing/Speech Impaired Call 711 for Customer Service. (open 11am-5pm on the third Wednesday of each month)

SAMPLE CUSTOMER BILL

/Users/anshchadha/Library/Python/3.9/lib/python/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
  from .autonotebook import tqdm as notebook_tqdm
/Users/anshchadha/Library/Python/3.9/lib/python/site-packages/huggingface_hub/file_download.py:1150: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
/Users/anshchadha/Library/Python/3.9/lib/python/site-packages/huggingface_hub/file_download.py:1150: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
---------------------------------------------------------------------------
KeyboardInterrupt                         Traceback (most recent call last)
Cell In[3], line 5
      1 from transformers import AutoModelForCausalLM, AutoTokenizer
      3 model_name = "Qwen/Qwen2.5-1.5B-Instruct"
----> 5 model = AutoModelForCausalLM.from_pretrained(
      6     model_name,
      7     torch_dtype="auto",
      8     device_map="auto"
      9 )
     10 tokenizer = AutoTokenizer.from_pretrained(model_name)
     12 prompt = "Give me a short introduction to large language model."

File ~/Library/Python/3.9/lib/python/site-packages/transformers/models/auto/auto_factory.py:566, in _BaseAutoModelClass.from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs)
    564 elif type(config) in cls._model_mapping.keys():
    565     model_class = _get_model_class(config, cls._model_mapping)
--> 566     return model_class.from_pretrained(
    567         pretrained_model_name_or_path, *model_args, config=config, **hub_kwargs, **kwargs
    568     )
    569 raise ValueError(
    570     f"Unrecognized configuration class {config.__class__} for this kind of AutoModel: {cls.__name__}.\n"
    571     f"Model type should be one of {', '.join(c.__name__ for c in cls._model_mapping.keys())}."
    572 )

File ~/Library/Python/3.9/lib/python/site-packages/transformers/modeling_utils.py:3383, in PreTrainedModel.from_pretrained(cls, pretrained_model_name_or_path, config, cache_dir, ignore_mismatched_sizes, force_download, local_files_only, token, revision, use_safetensors, *model_args, **kwargs)
...
-> 1099         return self._sslobj.read(len, buffer)
   1100     else:
   1101         return self._sslobj.read(len)

KeyboardInterrupt: 
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[2], line 1
----> 1 parse(extracted[1])

NameError: name 'parse' is not defined
'Darwin'
{'prices': [{'total_amount_due': 108.82},
  {'previous_balance': 103.61},
  {'comcast_paydirect': -103.61},
  {'new_charges': 108.82},
  {'thank_you': 93.84},
  {'other_charges_and_credits': 8.53},
  {'taxes_surcharges_fees': 6.45},
  {'total_new_charges': 108.82},
  {'sarview_detal_total_amount_due': 108.82},
  {'additional_outlet_01_08_to_07_video_prices': 9.95},
  {'xfinity_tv': 93.84},
  {'broadcast_tv_fee': 5.0},
  {'franchise_related_cost': 0.53},
  {'total_other_charges_credits': 8.53},
  {'state_sales_tax': 0.02},
  {'franchise_fee': 6.35},
  {'federal_council_regulatory_fee': 0.08},
  {'total_taxes_surcharges_fees': 6.45}],
 'dates': [{'billing_date': '12/28/15'},
  {'auto_pay': '01/12/16'},
  {'autopay_payment': '01/12/16'}],
 'others': [{'contact_us_url': 'https://www.xfinity.com'},
  {'call_phone_number': '(1) 800-934-6489'},
  {'payment_time': 'quick and convenient'},
  {'copyright_symbol': '©'},
  {'box_number': '6505'},
  {'location': 'CHELMSFORD MA 01824-0000'},
  {'call_to_request_monthly_bill_in_spanish_at': ''},
  {'live_chat_link': '855-270-0379'},
  {'phone_number': '+1 (555) 123-4567'},
  {'contact_type': 'residential'},
  {'business_type': 'real_estate'}]}
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
Note: There are some hallucinations and inaccuracy in the final result still due to a small model being used. The assignment was written by keeping in mind that it will probably be run on a standard computer and not on production grade GPUs. Proprietary models are not used either although a small experiment I conducted with claude produced good results.
