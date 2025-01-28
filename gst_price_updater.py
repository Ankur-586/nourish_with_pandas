import pandas as pd, datetime

from utils import gst_amount, get_masterData, fetch_date, compare_excel_files

# get today's date and time
current_date = datetime.datetime.now().strftime("%d-%m-%Y")

# get gst data
gst_data = get_masterData()

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


