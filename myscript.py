import re
from PIL import Image, ImageEnhance
import pytesseract
import cv2
import numpy as np

def preprocess_image(img_path):
    """Apply preprocessing effects to enhance OCR"""
    # 1. Open image
    img = Image.open(img_path)
    
    # 2. Brighten image (1.5x)
    brightener = ImageEnhance.Brightness(img)
    img = brightener.enhance(1.5)
    
    # 3. Convert to grayscale
    gray = img.convert("L")
    
    # 4. Binarization (threshold at 128)
    binary = gray.point(lambda p: 255 if p > 128 else 0)
    
    # 5. Denoising with median blur
    binary_np = np.array(binary)
    denoised = cv2.medianBlur(binary_np, 3)
    
    return Image.fromarray(denoised)

def extract_and_print_invoice_data(img_path):
    """Process single image and print extracted data"""
    # Preprocess the image
    processed_img = preprocess_image(img_path)
    
    # Perform OCR
    raw_text = pytesseract.image_to_string(processed_img)
    
    
    # Initialize data dictionary
    data = {
        'Invoice Number': None,
        'Date': None,
        'VAT Amount': None,
        'Net Worth': None,
        'Gross Worth': None,
        'Seller Tax ID': None,
        'Client Tax ID': None,
        'IBAN': None,
        'Seller City': None,
        'Client City': None,
        'Seller State': None,
        'Client State': None,
        'Seller ZIP': None,
        'Client ZIP': None,
        'Seller Address': None,
        'Client Address': None,
        'Seller Name': None,
        'Client Name': None
    }

    try:
        # 1. Invoice number
        invoice_match = re.search(r'Invoice no: (\d{8})', raw_text)
        if invoice_match:
            data['Invoice Number'] = invoice_match.group(1)
        
        # 2. Date
        date_match = re.search(r'\d{1,2}/\d{2}/\d{4}', raw_text)
        if date_match:
            data['Date'] = date_match.group()
        
        # 3. Financial info
        money_values = re.findall(r'\$\s*([\s\d]+,\d{2})', raw_text)
        if len(money_values) >= 3:
            data['VAT Amount'] = money_values[0]
            data['Net Worth'] = money_values[1]
            data['Gross Worth'] = money_values[2]
        
        # 4. Tax IDs
        tax_ids = re.findall(r'Tax Id:\s*(\d+-\d{2}-\d+)', raw_text)
        if len(tax_ids) >= 2:
            data['Seller Tax ID'] = tax_ids[0]
            data['Client Tax ID'] = tax_ids[1]
        
        # 5. IBAN
        iban_match = re.search(r'IBAN:\s*(\w+)', raw_text)
        if iban_match:
            data['IBAN'] = iban_match.group(1)
        
        # 6. Cities
        cities = re.findall(r'^([a-zA-Z\s]+),\s*[A-Z]{2}', raw_text, re.MULTILINE)
        if len(cities) >= 2:
            data['Seller City'] = cities[0]
            data['Client City'] = cities[1]
        
        # 7. States
        states = re.findall(r',\s*([A-Z]{2})\s*\d{5}', raw_text)
        if len(states) >= 2:
            data['Seller State'] = states[0]
            data['Client State'] = states[1]
        
        # 8. ZIP Codes
        zips = re.findall(r'[A-Z]{2}\s*(\d{5})$', raw_text, re.MULTILINE)
        if len(zips) >= 2:
            data['Seller ZIP'] = zips[0]
            data['Client ZIP'] = zips[1]
        
        # 9. Addresses
        addresses = re.findall(r'\n+(\d{3,}[^\n]+)\n*', raw_text, re.MULTILINE)
        if len(addresses) >= 2:
            data['Seller Address'] = addresses[0]
            data['Client Address'] = addresses[1]
        
        # 10. Names
        seller_name = re.findall(r'Seller:[\n]+([a-zA-Z-,\s*]+)[\n]+', raw_text)
        if seller_name:
            data['Seller Name'] = seller_name[0].strip()
        
        client_name = re.findall(r'Client:[\n]+([a-zA-Z-,\s*]+)[\n]+', raw_text)
        if client_name:
            data['Client Name'] = client_name[0].strip()
            
    except Exception as e:
        print(f"Error during extraction: {str(e)}")
    
    # Print all extracted data
    for field, value in data.items():
        print(f"{field:15}: {value if value else 'Not Found'}")

# Example usage
if __name__ == "__main__":
    # Path to your invoice image
    IMAGE_PATH = "Processed_images/invoice_984.pdf0.jpg"  # Replace with your image path
    
    # Process the image and print results
    extract_and_print_invoice_data(IMAGE_PATH)