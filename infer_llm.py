from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from tqdm import tqdm
import re



model_name = "Qwen/Qwen2.5-0.5B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
   torch_dtype=torch.float16,
   device_map="auto"
    
)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def check_pattern(text):
    # Define the patterns for prices and dates
    prices_pattern = r'-?\d+\.\d{2}'
    dates_pattern = r'\d{2}/\d{2}/\d{2,4}|\w{3,9}\s\d{1,2},\s\d{4}'
    splitted = text.split()

    # Search for prices and dates in the text
    has_price = any(re.findall(prices_pattern, i) for i in splitted)
    has_date = any(re.findall(dates_pattern, i) for i in splitted)
    has_10_digits = lambda x: len([i for i in x if i.isdigit()]) >= 10

    # Check if the text contains either a price or a date
    if has_price or has_date or has_10_digits(text):
        return True
    return False




def clean_line(x):
    prompt = f"""
    Extract the numerical value from the following unstructured text and convert it into a structured JSON format. 
    - The key should be a descriptive field name based on the text, written in snake_case.
    - The value should be the corresponding numerical value (as a float or integer).
    - The value should be accurate
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
    Output: {{ "registered_phone_number": "+1 (555) 123-4567" }}

    Now process the following text and generate the structured JSON format:

    Text: "{x}"
    """

    messages = [
        {"role": "system", "content": "You are an AI assistant and you're supposed to convert this unstructured text into a structured JSON format."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    input_ids = model_inputs.input_ids
    generated_ids = input_ids

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=200
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return response


def run_llm_on_text(bill_text):
    
    
    bill_text = [i for i in bill_text if check_pattern(i)]
    #chunks = len(bill_text) // 
    #bill_text = [bill_text[i:i+chunks] for i in range(0,len(bill_text),chunks)]
    response_dict = {}
    for line in tqdm(bill_text):
        try:
            resp = clean_line(line)
            resp = resp.replace('```','').replace('json','').strip()
            resp = eval(resp)
            if type(resp) == dict:
                for i in resp:
                    if type(resp[i]) == int or type(resp[i]) == str or type(resp[i]) == float:
                        #check_pattern(str(resp[i]))
                        response_dict[i] = resp[i]
        except:
            pass


    return response_dict


