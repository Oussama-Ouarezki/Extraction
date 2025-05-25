import streamlit as st
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
import pandas as pd
from io import BytesIO
import faulthandler
import sqlite3
from sqlite3 import Error

st.set_page_config(page_title="Invoice OCR Extractor", layout="wide")
faulthandler.enable()

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # for windows only

# CSS styling
st.markdown(""" <style>
.stApp {
background-color: #ADD8E6;
}
div[data-testid="stFileUploader"] {
background-color: #E0F2FF;
padding: 1.5rem;
border-radius: 10px;
border: 2px solid #90CAF9;
}
.button-link {
    display: inline-block;
    padding: 0.5rem 1rem;
    background-color: #4CAF50;
    color: white;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    border-radius: 4px;
    cursor: pointer;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# OCR zones
ZONES = {
    "header": (0, 20, 1600, 280),
    "seller_info": (0, 281, 674, 750),
    "client_info": (674, 281, 1600, 750),
    "body_content": (0, 750, 1600, 2290)
}

def create_connection():
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect('invoices.db')
        return conn
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return conn

def create_tables(conn):
    """ Create database tables based on the schema """
    try:
        c = conn.cursor()
        
        # Create Sellers table
        c.execute('''CREATE TABLE IF NOT EXISTS Sellers
                     (tax_id TEXT PRIMARY KEY,
                      name TEXT NOT NULL,
                      address TEXT,
                      city TEXT,
                      state TEXT,
                      zip_code TEXT,
                      iban TEXT)''')
        
        # Create Clients table
        c.execute('''CREATE TABLE IF NOT EXISTS Clients
                     (tax_id TEXT PRIMARY KEY,
                      name TEXT NOT NULL,
                      address TEXT,
                      city TEXT,
                      state TEXT,
                      zip_code TEXT)''')
        
        # Create Invoices table
        c.execute('''CREATE TABLE IF NOT EXISTS Invoices
                     (invoice_number TEXT PRIMARY KEY,
                      date TEXT,
                      net_worth REAL,
                      vat REAL,
                      gross_worth REAL,
                      client_tax_id TEXT,
                      seller_tax_id TEXT,
                      source_file TEXT,
                      FOREIGN KEY (client_tax_id) REFERENCES Clients (tax_id),
                      FOREIGN KEY (seller_tax_id) REFERENCES Sellers (tax_id))''')
        
        conn.commit()
    except Error as e:
        st.error(f"Error creating tables: {e}")

def insert_data(conn, data):
    """ Insert extracted data into the database """
    try:
        c = conn.cursor()
        
        # Insert or ignore seller
        c.execute('''INSERT OR IGNORE INTO Sellers 
                     (tax_id, name, address, city, state, zip_code, iban)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (data['tax_id_1'], data['seller_name'], data['seller_address'],
                   data['seller_city'], data['seller_state'], data['seller_zip'],
                   data['iban']))
        
        # Insert or ignore client
        c.execute('''INSERT OR IGNORE INTO Clients 
                     (tax_id, name, address, city, state, zip_code)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (data['tax_id_2'], data['client_name'], data['client_address'],
                   data['client_city'], data['client_state'], data['client_zip']))
        
        # Insert invoice
        c.execute('''INSERT OR REPLACE INTO Invoices
                     (invoice_number, date, net_worth, vat, gross_worth,
                      client_tax_id, seller_tax_id, source_file)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data['invoice_number'], data['date'], data['net_worth'],
                   data['vat'], data['gross_worth'], data['tax_id_2'],
                   data['tax_id_1'], data['source_file']))
        
        conn.commit()
    except Error as e:
        st.error(f"Error inserting data: {e}")

def preprocess_image(image):
    """ Image preprocessing for better OCR results """
    image = image.convert('L')
    image = image.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    image = image.point(lambda x: 0 if x < 140 else 255)
    return image

def extract_zone_text(img, zone_coords):
    """ Extract text from a specific zone of the image """
    zone_img = img.crop(zone_coords)
    zone_img = preprocess_image(zone_img)
    config = '--psm 6 --oem 3'
    text = pytesseract.image_to_string(zone_img, config=config)
    return text.strip()

def extract_data(raw_text):
    """ Extract structured data from OCR text """
    data = {}
    
    # Invoice number
    match = re.search(r'(\d{8})\n', raw_text)
    data['invoice_number'] = match.group(1) if match else None

    # Date
    match = re.search(r'\d{1,2}/\d{2}/\d{4}', raw_text)
    data['date'] = match.group(0) if match else None

    # Financial data
    financial_matches = re.findall(r'Total\s*\$\s*([\d\s]+,\d{2})', raw_text)
    if financial_matches:
        cleaned = financial_matches[0].strip().replace(" ", "").replace(",", ".")
        try:
            data['net_worth'] = float(cleaned)
        except ValueError:
            data['net_worth'] = None
    else:
        data['net_worth'] = None

    # Tax IDs
    tax_matches = re.findall(r'Tax Id:\s*(\d+-\d{2,3}-\d+)', raw_text)
    data['tax_id_1'] = tax_matches[0] if len(tax_matches) > 0 else None
    data['tax_id_2'] = tax_matches[1] if len(tax_matches) > 1 else None

    # IBAN
    match = re.search(r'IBAN:\s*(\w+)', raw_text)
    data['iban'] = match.group(1) if match else None

    # Location data
    loc_matches = re.findall(r'\n([a-zA-Z\s]+),?\s*([A-Z]{2})\s*(\d{5})\n', raw_text)
    if loc_matches:
        data['seller_city'] = loc_matches[0][0] if len(loc_matches) > 0 else None
        data['seller_state'] = loc_matches[0][1] if len(loc_matches) > 0 else None
        data['seller_zip'] = loc_matches[0][2] if len(loc_matches) > 0 else None
        data['client_city'] = loc_matches[-1][0] if len(loc_matches) > 1 else None
        data['client_state'] = loc_matches[-1][1] if len(loc_matches) > 1 else None
        data['client_zip'] = loc_matches[-1][2] if len(loc_matches) > 1 else None

    # Seller info
    match = re.findall(r'Seller:\n+([A-Za-z\s,-]+)\n+([A-Za-z0-9\s,.]+)', raw_text)
    if match:
        data['seller_name'] = match[0][0]
        data['seller_address'] = match[0][1]
    else:
        data['seller_name'] = None
        data['seller_address'] = None

    # Client info
    match = re.findall(r'Client:\n+([A-Za-z\s,-]+)\n+([A-Za-z0-9\s,.]+)', raw_text)
    if match:
        data['client_name'] = match[0][0]
        data['client_address'] = match[0][1]
    else:
        data['client_name'] = None
        data['client_address'] = None

    return data

def process_image(img):
    """ Process image through all zones """
    extracted_text = ""
    for zone_name, coords in ZONES.items():
        zone_text = extract_zone_text(img, coords)
        extracted_text += f"\n\n=== {zone_name.upper()} ===\n{zone_text}"
    return extracted_text.strip()

# Main Streamlit app
st.title("📄 Invoice OCR Data Extractor")

# Initialize database
conn = create_connection()
if conn is not None:
    create_tables(conn)

with st.expander("ℹ️ About This App", expanded=False):
    st.markdown("""
    This application extracts data from invoice images using OCR technology. 
    It processes the following information:
    - Invoice numbers and dates
    - Seller and client details
    - Financial information (net worth, VAT, gross worth)
    
    The extracted data is stored in a SQLite database and can be downloaded as CSV or SQL.
    """)

uploaded_files = st.file_uploader("Upload Invoice Images (JPG, PNG, etc.)",
                                 type=["jpg", "png", "jpeg"],
                                 accept_multiple_files=True)

if uploaded_files:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    for i, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing image {i+1}/{len(uploaded_files)}: {uploaded_file.name}")
        progress_bar.progress((i) / len(uploaded_files))
        
        try:
            image = Image.open(BytesIO(uploaded_file.read()))
            text = process_image(image)
            extracted = extract_data(text)
            extracted['source_file'] = uploaded_file.name
            
            # Calculate VAT and gross worth
            if extracted['net_worth'] is not None:
                extracted['vat'] = round(extracted['net_worth'] * 0.1, 2)
                extracted['gross_worth'] = round(extracted['net_worth'] + extracted['vat'], 2)
            else:
                extracted['vat'] = None
                extracted['gross_worth'] = None
            
            results.append(extracted)
            
            # Insert into database
            if conn is not None:
                insert_data(conn, extracted)
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
    
    progress_bar.progress(1.0)
    status_text.text("Processing complete!")
    
    df = pd.DataFrame(results)
    
    st.subheader("📋 Extracted Invoice Data")
    st.dataframe(df)
    
    # Show raw text option

    # Download buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="invoice_data.csv",
            mime="text/csv",
        )
    
    with col2:
        if conn is not None:
            # Export database to SQL file
            with open('invoices_db_dump.sql', 'w') as f:
                for line in conn.iterdump():
                    f.write(f'{line}\n')
            
            with open('invoices_db_dump.sql', 'rb') as f:
                st.download_button(
                    label="💾 Download Database",
                    data=f,
                    file_name="invoices_db_dump.sql",
                    mime="application/sql",
                )
    
    with col3:
        st.markdown(
            '<a href="https://sqliteonline.com/" target="_blank" class="button-link">📊 Open in SQLite Online</a>',
            unsafe_allow_html=True
        )

# Close database connection
if conn is not None:
    conn.close()