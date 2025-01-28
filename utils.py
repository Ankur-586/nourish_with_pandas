import re, pandas as pd
from pathlib import Path

from tkinter import Tk 
from tkinter.filedialog import askopenfilename

from master_data.product_with_gst import (productGroup1_GST_5percent, 
                                          productGroup2_GST_0percent, productGroup3_GST_12percent)


def gst_amount(amt: int, gst_rate: float):
    '''
    Formula to calculate Gst Price of a product
    '''
    if not (isinstance(amt, (float,int)) and isinstance(gst_rate, float)):
        return f"AMOUNT: {amt} or GST: {gst_rate} values not appropriate"
    gst_amt = amt - (amt * (100/(100 + gst_rate)))
    pre_gst_amt = amt - gst_amt
    return round(pre_gst_amt, 2), round(gst_amt, 2)
# ------------------------------------------------------------------------------
def get_masterData():
    '''
    Convert the Product lists to a dict And 
    product gets divided according to their 
    gst rate.
    '''
    data = {}
    data.update({
            'GST 5%': productGroup1_GST_5percent,
            'GST 0%': productGroup2_GST_0percent,
            'GST 12%': productGroup3_GST_12percent
        })
    return data
# ---------------------------------------------------------------------------------
def fetch_date(url):
    '''
    Fetch the date from the Excel url.
    '''
    match_str = re.search(r'\((\d{2}-\d{2}-\d{2})\)', url)
    if match_str:
        date_str = match_str.group(1)
        return date_str
    else:
        return None
# ---------------------------------------------------------------------------------
def compare_excel_files(url):
    old_file = r'D:\0-convert_price\excel_file\MRP New Update (07-01-25).xlsx'
    new_file = r'D:\0-convert_price\excel_file\MRP New Update (08-01-25).xlsx'
    # Read the Excel files into DataFrames, skipping the first two rows and handling missing values
    old_df = pd.read_excel(old_file, engine='openpyxl', skiprows=[0, 1]).dropna(how='all', subset=['MRP/-'])
    new_df = pd.read_excel(new_file, engine='openpyxl', skiprows=[0, 1]).dropna(how='all', subset=['MRP/-'])
    # Drop the 'Unnamed: 6' column directly after reading the data
    old_df = old_df.drop(columns=['Unnamed: 6'])
    new_df = new_df.drop(columns=['Unnamed: 6'])
    # Ensure the 'MRP Update Date ' columns are in datetime format
    old_df['MRP Update Date '] = pd.to_datetime(old_df['MRP Update Date ']).dt.strftime('%Y-%m-%d')
    new_df['MRP Update Date '] = pd.to_datetime(new_df['MRP Update Date ']).dt.strftime('%Y-%m-%d')
    # Filter out products from the second DataFrame (new_df) where the MRP Update Date is later than the old one
    # Merge on 'Brand Name' and 'Pack Size' and compare the 'MRP Update Date '
    if fetch_date(old_file) < fetch_date(new_file):
        merged_df = pd.merge(old_df[['Brand Name', 'Pack Size', 'MRP Update Date ']],
                            new_df[['Brand Name', 'Pack Size', 'MRP Update Date ']],
                            on=['Brand Name', 'Pack Size'],
                            suffixes=('_old', '_new'),
                            how='inner')
        # Filter for rows where the new MRP Update Date is later than the old one
        to_update_df = merged_df[merged_df['MRP Update Date _new'] > merged_df['MRP Update Date _old']]
        # Extract the relevant columns for products to update
        product_to_update = to_update_df[['Brand Name', 'Pack Size', 'MRP Update Date _new']]
        # Convert to a list of tuples, if desired
        product_to_update_list = list(product_to_update.itertuples(index=False, name=None))
        return product_to_update_list, new_df
    else:
        return None
# --------------------------------------------------------------------------------------------------------------
def read_filePath():
    excel_file_folder = Path('excel_file')
    subdirs = ['updated_price']
    excel_file_folder.mkdir(parents=True, exist_ok=True)
    for subdir in subdirs:
        (excel_file_folder / subdir).mkdir(parents=True, exist_ok=True)
    files = list(excel_file_folder.glob('**/*.xlsx'))
    file_info = []
    for file in files:                                                     
        # Store the file path and file name as a tuple in the list
        file_info.append({
            'File Path': file,
            'File Name': file.name
        })
    Tk().withdraw() 
    filename = askopenfilename() 
    print(filename)
read_filePath()
# --------------------------------------------------------------------------------------------------------------

'''
This is My code. Do Not Delete

def compare_excel_files():
    old_file = r'D:\0-convert_price\excel_file\MRP New Update (07-01-25).xlsx'
    new_file = r'D:\0-convert_price\excel_file\MRP New Update (08-01-25).xlsx'
    old_df = pd.read_excel(old_file, engine='openpyxl',  index_col=None, skiprows = lambda x: x in [0, 1]) \
        .dropna(how='all', inplace=False, subset=['MRP/-'])
    new_df = pd.read_excel(new_file, engine='openpyxl',  index_col=None, skiprows = lambda x: x in [0, 1]) \
        .dropna(how='all', inplace=False, subset=['MRP/-'])
    df1 = old_df.drop('Unnamed: 6', axis=1)
    df2 = new_df.drop('Unnamed: 6', axis=1)
    
    prod_1, prod_2, product_to_update = [], [], []
    for index, row in df1.iterrows():
        product = row['Brand Name']
        weight = row['Pack Size']
        update_date = row['MRP Update Date '].strftime('%Y-%m-%d')
        prod_1.append((product, weight, update_date))
    # print(prod_1)
    for index1, row1 in df2.iterrows():
        product = row1['Brand Name']
        weight = row1['Pack Size']
        update_date = row1['MRP Update Date '].strftime('%Y-%m-%d')
        prod_2.append((product, weight, update_date))
    # print(prod_2)
    for x, y in zip(prod_1, prod_2):
        if x[2] < y[2]:
            product_to_update.append(y)
    print(product_to_update)
compare_excel_files()
'''