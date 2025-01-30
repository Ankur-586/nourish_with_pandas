import pandas as pd, datetime

from utils import gst_amount, get_masterData, fetch_date, compare_excel_files, read_filePath

# get today's date and time
current_date = datetime.datetime.now().strftime("%d-%m-%Y")

# Define file path
output = read_filePath()

if isinstance(output, tuple) and len(output) == 2:
    print('First')
elif isinstance(output, str):   
    # fetch date from the file
    out_date = fetch_date(output)

    # Read Excel File
    df = pd.read_excel(output, engine='openpyxl', index_col=None, skiprows=lambda x: x in [0, 1])

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

    if out_date is None:
        output_file_path = f'excel_file/updated_price/MRP New Update ({current_date}).xlsx'
    else:
        output_file_path = f'excel_file/updated_price/MRP New Update ({out_date}).xlsx'
        
    df.to_excel(output_file_path, index=False)
    print(f"File saved to: {output_file_path}")
else:
    print("Unexpected Output !!!")