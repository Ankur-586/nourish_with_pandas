import re, pandas as pd, shutil, os, datetime as dt
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
    match_str = re.search(r'\((\d{2}-\d{2}-\d{2})\)', str(url))
    if match_str:
        date_str = match_str.group(1)
        return date_str
    else:
        return None
# ---------------------------------------------------------------------------------
def compare_excel_files(old_file_path, new_file_path):
    old_df = pd.read_excel(old_file_path, engine='openpyxl', skiprows=[0, 1]).dropna(how='all', subset=['MRP/-'])
    new_df = pd.read_excel(new_file_path, engine='openpyxl', skiprows=[0, 1]).dropna(how='all', subset=['MRP/-'])
    # Drop the 'Unnamed: 6' column directly after reading the data
    old_df = old_df.drop(columns=['Unnamed: 6'])
    new_df = new_df.drop(columns=['Unnamed: 6'])
    # Ensure the 'MRP Update Date ' columns are in datetime format
    old_df['MRP Update Date '] = pd.to_datetime(old_df['MRP Update Date ']).dt.strftime('%Y-%m-%d')
    new_df['MRP Update Date '] = pd.to_datetime(new_df['MRP Update Date ']).dt.strftime('%Y-%m-%d')
    # Filter out products from the second DataFrame (new_df) where the MRP Update Date is later than the old one
    # Merge on 'Brand Name' and 'Pack Size' and compare the 'MRP Update Date '
    if fetch_date(old_file_path) < fetch_date(new_file_path):
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
        return product_to_update_list, new_df, fetch_date(new_file_path)
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
# --------------------------------------------------------------------------------------------------------------
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
            return str(file_info[-1]['File Path'])
        else:
            print('File Selection Failed. Try Again!!')
    else:
        print("1 file already exists. Please Select another File to compare!!")
        selected_file = askopenfilename(title="Select an Excel File", initialdir=excel_file_folder, 
                        filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if selected_file:
            print(f"Selected file: {selected_file}")
            shutil.copy(selected_file, excel_file_folder)
            file_info = collect_file_info(excel_file_folder)
            old_file = file_info[-2]['File Path']
            lastest_file = file_info[-1]['File Path']
            return compare_excel_files(old_file, lastest_file)
        else:
            print('File Selection Failed. Try Again!!')
# --------------------------------------------------------------------------------------------------------------

''' ############################################ DIVIDER ####################################################'''
# ----------------------------------------------- START ---------------------------------------------------------
'''
Following Function are used for GUI window
''' 
def process_excel_file(selected_file):
    excel_file_folder = Path('excel_file')
    create_directories(excel_file_folder)

    file_info = collect_file_info(excel_file_folder)
    if len(file_info) == 0:
        print("File Doesn't Exist. Please Select the File!!")
        if selected_file:
            print(f"Selected file: {selected_file}")
            shutil.copy(selected_file, excel_file_folder)
            file_info = collect_file_info(excel_file_folder)
            return str(file_info[-1]['File Path'])
        else:
            print('File Selection Failed. Try Again!!')
    else:
        print("1 file already exists. Please Select another File to compare!!")
        if selected_file:
            print(f"Selected file: {selected_file}")
            shutil.copy(selected_file, excel_file_folder)
            file_info = collect_file_info(excel_file_folder)
            old_file = file_info[-2]['File Path']
            lastest_file = file_info[-1]['File Path']
            return compare_excel_files(old_file, lastest_file)
        else:
            print('File Selection Failed. Try Again!!')
            
def apply_gst_and_save(selected_file):
    current_date = dt.datetime.now().strftime("%d-%m-%Y")
    gst_data = get_masterData()
    output = process_excel_file(selected_file)
    out_date = fetch_date(selected_file)
    # Create a lookup set for faster brand name matching
    gst_5_percent_brands = {product[0] for product in gst_data['GST 5%']}
    gst_0_percent_brands = {product[0] for product in gst_data['GST 0%']}
    gst_12_percent_brands = {product[0] for product in gst_data['GST 12%']}

    if isinstance(output, tuple) and len(output) == 2:
        product_to_update, new_df = output
        
        product_to_update_set = {product[0] for product in product_to_update}
        
        for index, row in new_df.iterrows():
            brand_name = row['Brand Name'].strip()
            price = row['MRP/-']
            
            # Set the GST group based on the brand
            if brand_name in gst_5_percent_brands:
                new_df.at[index, 'GST'] = '5%'
                gst_rate = 5.0
            elif brand_name in gst_0_percent_brands:
                new_df.at[index, 'GST'] = '0%'
                gst_rate = 0.0
            elif brand_name in gst_12_percent_brands:
                new_df.at[index, 'GST'] = '12%'
                gst_rate = 12.0
            else:
                new_df.at[index, 'GST'] = 'Not Found'
                continue  # Skip GST calculation if brand is not found in any group

            # Only calculate GST for products in the product_to_update list
            if brand_name in product_to_update_set:
                pre_gst_amt, total_gst = gst_amount(price, gst_rate)
                new_df.at[index, 'Amount Before Tax'] = pre_gst_amt
                new_df.at[index, 'Total GST'] = total_gst
            else:
                # If product is not in product_to_update, no GST calculation
                new_df.at[index, 'Amount Before Tax'] = None
                new_df.at[index, 'Total GST'] = None

        if out_date is None:
            output_file_path = f'excel_file/updated_price/MRP New Update ({current_date}).xlsx'
        else:
            output_file_path = f'excel_file/updated_price/MRP New Update ({out_date}).xlsx'
        new_df.to_excel(output_file_path, index=False)
        print(f"Updated file saved to: {output_file_path}")
        return output_file_path
    
    elif isinstance(output, str):   
        # If output is a string (file path)
        out_date = fetch_date(output)
        df = pd.read_excel(output, engine='openpyxl', index_col=None, skiprows=[0, 1])

        # Drop rows where all columns are NaN in 'MRP/-'
        df = df.dropna(how='all', inplace=False, subset=['MRP/-'])

        # Drop unnecessary column
        df = df.drop('Unnamed: 6', axis=1)

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
            pre_gst_amt, total_gst = gst_amount(price, gst_rate)

            # Update row with calculated values
            row['GST'] = gst_group
            row['Amount Before Tax'] = pre_gst_amt
            row['Total GST'] = total_gst
            return row

        # Apply the function to each row (vectorized)
        df = df.apply(apply_gst, axis=1)

        # Determine output file path
        if out_date is None:
            output_file_path = f'excel_file/updated_price/MRP New Update ({current_date}).xlsx'
        else:
            output_file_path = f'excel_file/updated_price/MRP New Update ({out_date}).xlsx'
        
        df.to_excel(output_file_path, index=False)
        print(f"File saved to: {output_file_path}")
        return output_file_path

    else:
        print("Unexpected Output!!!")
        return None
# -------------------------------------------------- END ---------------------------------------------------------