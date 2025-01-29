import re, pandas as pd, shutil, os
from pathlib import Path
from datetime import datetime

import tkinter as tk
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
def compare_excel_files():
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
def get_last_modified_time(file_path):
    '''
    This function give the Modified date of the excel file.
    '''
    try:
        formatted_date = os.path.getmtime(file_path)
        return datetime.fromtimestamp(formatted_date).strftime('%d-%m-%y %H:%M:%S')
    except FileNotFoundError:
        return None  # If the file doesn't exist
# --------------------------------------------------------------------------------------------------------------
def create_directories(excel_file_folder):
    subdirs = ['updated_price']
    excel_file_folder.mkdir(parents=True, exist_ok=True)
    for subdir in subdirs:
        (excel_file_folder / subdir).mkdir(parents=True, exist_ok=True)

def collect_file_info(excel_file_folder):
    files = list(excel_file_folder.glob('*.xlsx'))
    file_info = []
    for file in files:
        # Exclude files inside the "Update_price" folder
        if "Update_price" not in file.parts:
            # Store the file path and file name as a tuple in the list
            file_info.append({
                'File Path': file,
                'File Name': file.name
            })
    return file_info

def read_filePath():
    excel_file_folder = Path('excel_file')
    create_directories(excel_file_folder)
    
    file_info = collect_file_info(excel_file_folder)
    if len(file_info) == 0:
        print("File Doesn't Exist. Please Select the File!!")
        selected_file = askopenfilename(title="Select an Excel File", initialdir=excel_file_folder, 
                        filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if selected_file:
            print(f"Selected file: {selected_file}")
            shutil.copy(selected_file, excel_file_folder)
            file_info = collect_file_info(excel_file_folder)
            return file_info[0]['File Path']
        else:
            print('File Selection Failed. Try Again!!')
    else:
        print('File Exists! Please Proceed Further')
        return file_info[-1]
        
        
# --------------------------------------------------------------------------------------------------------------



