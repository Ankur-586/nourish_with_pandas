import pandas as pd
from datetime import datetime

from utils import gst_amount, get_path


excel_file_path = r'D:\0-convert_price\excel_file\Master Sheet (GST Rate).xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl',  index_col=0)

# The "subset" Remove rows where all columns are NaN
df = df.dropna(how='all', inplace=False, subset=['MRP'])

# Remove rows where all columns are Unnamed:+
df = df.drop('Unnamed: 7', axis=1)

for index, row in df.iterrows():
    # print(f"S.No: {index}, Row:\n{row}")
    product_price = row['MRP']
    gst_rate = row['Gst']
    pre_gst_amt, total_gst = gst_amount(product_price, gst_rate)
    df.at[index, 'Amount Before Tax'] = pre_gst_amt
    df.at[index, 'Total GST'] = total_gst
df.to_excel(f'excel_file\updated_price\cleaned_files.xlsx', index=False)

# -----------------------------------------------------------------------------------


import pandas as pd

from utils import gst_amount, get_masterData

# get gst data
gst_data = get_masterData()

excel_file_path = r'D:\0-convert_price\excel_file\MRP New Update (08-01-25).xlsx'

df = pd.read_excel(excel_file_path, engine='openpyxl',  index_col=None, skiprows = lambda x: x in [0, 1])

# The "subset" Remove rows where all columns are NaN
df = df.dropna(how='all', inplace=False, subset=['MRP/-'])

# Remove rows where all columns are Unnamed:+
df = df.drop('Unnamed: 6', axis=1)

# Create a lookup set for faster brand name matching
gst_5_percent_brands = {product[0] for product in gst_data['GST 5%']}
gst_0_percent_brands = {product[0] for product in gst_data['GST 0%']}
gst_12_percent_brands = {product[0] for product in gst_data['GST 12%']}

for index, row in df.iterrows():
    
    brand_name = row['Brand Name'].strip()
    price = row['MRP/-']
    if brand_name in gst_5_percent_brands:
        df.at[index, 'GST'] = '5%'
        product_price = price
        gst_rate = 5.0
        pre_gst_amt, total_gst = gst_amount(product_price, gst_rate)
        df.at[index, 'Amount Before Tax'] = pre_gst_amt
        df.at[index, 'Total GST'] = total_gst
        # print(f"Brand '{brand_name}', {price}, {pre_gst_amt}, {gst_rate} is present in GST 5%")
    elif brand_name in gst_0_percent_brands:
        df.at[index, 'GST'] = '0%'
        product_price = price
        gst_rate = 0.0
        pre_gst_amt, total_gst = gst_amount(product_price, gst_rate)
        df.at[index, 'Amount Before Tax'] = pre_gst_amt
        df.at[index, 'Total GST'] = total_gst
        # print(f"Brand '{brand_name}', {price} is present in GST 0%")
    elif brand_name in gst_12_percent_brands:
        df.at[index, 'GST'] = '12%'
        product_price = price
        gst_rate = 12.0
        pre_gst_amt, total_gst = gst_amount(product_price, gst_rate)
        df.at[index, 'Amount Before Tax'] = pre_gst_amt
        df.at[index, 'Total GST'] = total_gst
        # print(f"Brand '{brand_name}', {price} is present in GST 12%")
    else:
        print(f"Brand '{brand_name}' is NOT found in any GST group")

output_file_path = r'excel_file\updated_price\cleaned_files.xlsx'
df.to_excel(output_file_path, index=False)
print(f"File saved to: {output_file_path}")
# ------------------------------------------
excel_file_path = r'excel_file\MRP New Update (07-01-25).xlsx'
# excel_file_path = r'D:\0-convert_price\excel_file\MRP New Update (07-01-25).xlsx' 
out_date = fetch_date(excel_file_path)

df = pd.read_excel(excel_file_path, engine='openpyxl',  index_col=None, skiprows = lambda x: x in [0, 1])

# The "subset" Remove rows where all columns are NaN
df = df.dropna(how='all', inplace=False, subset=['MRP/-'])

# Remove rows where all columns are Unnamed:+
df = df.drop('Unnamed: 6', axis=1)

# Create a lookup set for faster brand name matching
gst_5_percent_brands = {product[0] for product in gst_data['GST 5%']}
gst_0_percent_brands = {product[0] for product in gst_data['GST 0%']}
gst_12_percent_brands = {product[0] for product in gst_data['GST 12%']}

for index, row in df.iterrows():
    
    brand_name = row['Brand Name'].strip()
    price = row['MRP/-']
    if brand_name in gst_5_percent_brands:
        df.at[index, 'GST'] = '5%'
        product_price = price
        gst_rate = 5.0
        pre_gst_amt, total_gst = gst_amount(product_price, gst_rate)
        df.at[index, 'Amount Before Tax'] = pre_gst_amt
        df.at[index, 'Total GST'] = total_gst
        # print(f"Brand '{brand_name}', {price}, {pre_gst_amt}, {gst_rate} is present in GST 5%")
    elif brand_name in gst_0_percent_brands:
        df.at[index, 'GST'] = '0%'
        product_price = price
        gst_rate = 0.0
        pre_gst_amt, total_gst = gst_amount(product_price, gst_rate)
        df.at[index, 'Amount Before Tax'] = pre_gst_amt
        df.at[index, 'Total GST'] = total_gst
        # print(f"Brand '{brand_name}', {price} is present in GST 0%")
    elif brand_name in gst_12_percent_brands:
        df.at[index, 'GST'] = '12%'
        product_price = price
        gst_rate = 12.0
        pre_gst_amt, total_gst = gst_amount(product_price, gst_rate)
        df.at[index, 'Amount Before Tax'] = pre_gst_amt
        df.at[index, 'Total GST'] = total_gst
        # print(f"Brand '{brand_name}', {price} is present in GST 12%")
    else:
        print(f"Brand '{brand_name}' is NOT found in any GST group")

if out_date is None:
    output_file_path = f'excel_file/updated_price/MRP New Update ({current_date}).xlsx'
else:
    output_file_path = f'excel_file/updated_price/MRP New Update ({out_date}).xlsx'
    
df.to_excel(output_file_path, index=False)
print(f"File saved to: {output_file_path}")
# ------------------------------------------------------------
'''
# Define file path
excel_file_path = r'D:\0-convert_price\MRP New Update (08-01-25).xlsx'

# Read Excel File
df = pd.read_excel(excel_file_path, engine='openpyxl', index_col=None, skiprows=lambda x: x in [0, 1])

# Drop rows where all columns are NaN in 'MRP/-'
df = df.dropna(how='all', inplace=False, subset=['MRP/-'])

# Drop the unnecessary 'Unnamed: 6' column
df = df.drop('Unnamed: 6', axis=1)

# Get GST data
gst_data = get_masterData()

# Create a lookup set for faster brand name matching
gst_5_percent_brands = {product[0] for product in gst_data['GST 5%']}
gst_0_percent_brands = {product[0] for product in gst_data['GST 0%']}
gst_12_percent_brands = {product[0] for product in gst_data['GST 12%']}

def apply_gst(row):
    brand_name = row['Brand Name'].strip()
    price = row['MRP/-']
    
    if brand_name in gst_5_percent_brands:
        gst_rate = 5.0
        gst_group = 'GST 5%'
    elif brand_name in gst_0_percent_brands:
        gst_rate = 0.0
        gst_group = 'GST 0%'
    elif brand_name in gst_12_percent_brands:
        gst_rate = 12.0
        gst_group = 'GST 12%'
    else:
        print(f"Brand '{brand_name}' is NOT found in any GST group")
        return row
    
    # Calculate GST amounts
    product_price = price
    pre_gst_amt, total_gst = gst_amount(product_price, gst_rate)
    
    # Update row with calculated values
    row['GST'] = gst_group
    row['Amount Before Tax'] = pre_gst_amt
    row['Total GST'] = total_gst
    return row

# Apply the function to each row (vectorized)
df = df.apply(apply_gst, axis=1)

# Define output path
output_file_path = r'excel_file\updated_price\cleaned_files.xlsx'

# Save the updated DataFrame to a new Excel file
df.to_excel(output_file_path, index=False)
print(f"File saved to: {output_file_path}")
'''
# ------------------------------------------------

import pandas as pd, datetime

from utils import gst_amount, get_masterData, fetch_date, compare_excel_files, read_filePath

def apply_gst(row, gst_5_percent_brands, gst_0_percent_brands, gst_12_percent_brands):
    """Apply GST calculation based on the brand and MRP."""
    brand_name = row['Brand Name'].strip()
    price = row['MRP/-']
    
    # Determine GST rate based on brand name
    if brand_name in gst_5_percent_brands:
        gst_rate = 5.0
        gst_group = 'GST 5%'
    elif brand_name in gst_0_percent_brands:
        gst_rate = 0.0
        gst_group = 'GST 0%'
    elif brand_name in gst_12_percent_brands:
        gst_rate = 12.0
        gst_group = 'GST 12%'
    else:
        print(f"Brand '{brand_name}' is NOT found in any GST group")
        return row
    
    # Calculate GST amounts
    pre_gst_amt, total_gst = gst_amount(price, gst_rate)
    
    # Update row with calculated values
    row['GST'] = gst_group
    row['Amount Before Tax'] = pre_gst_amt
    row['Total GST'] = total_gst
    return row

def process_gst_data():
    """Process the GST data from an Excel file and save the updated file."""
    
    # Get today's date and time
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    
    # Define file path
    initial_excel_file_path = read_filePath()
    
    # Fetch date from the file path
    out_date = fetch_date(initial_excel_file_path)
    
    # Read Excel file, skipping the first two rows
    df = pd.read_excel(initial_excel_file_path, engine='openpyxl', index_col=None, skiprows=lambda x: x in [0, 1])
    
    # Drop rows where all columns in 'MRP/-' are NaN
    df = df.dropna(how='all', inplace=False, subset=['MRP/-'])
    
    # Drop the unnecessary 'Unnamed: 6' column
    df = df.drop('Unnamed: 6', axis=1)
    
    # Get GST data for various categories
    gst_data = get_masterData()
    gst_5_percent_brands = {product[0] for product in gst_data['GST 5%']}
    gst_0_percent_brands = {product[0] for product in gst_data['GST 0%']}
    gst_12_percent_brands = {product[0] for product in gst_data['GST 12%']}
    
    # Apply GST calculation function to each row in the DataFrame
    df = df.apply(apply_gst, axis=1, gst_5_percent_brands=gst_5_percent_brands,
                  gst_0_percent_brands=gst_0_percent_brands, gst_12_percent_brands=gst_12_percent_brands)
    
    # Determine output file path
    if out_date is None:
        output_file_path = f'excel_file/updated_price/MRP New Update ({current_date}).xlsx'
    else:
        output_file_path = f'excel_file/updated_price/MRP New Update ({out_date}).xlsx'
    
    # Save the updated DataFrame to Excel
    df.to_excel(output_file_path, index=False)
    
    # Print success message with file path
    print(f"File saved to: {output_file_path}")

# Call the function to process the data
process_gst_data()