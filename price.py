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


