'''
These are My Original code's. Do Not Delete

def read_filePath():
    excel_file_folder = Path('excel_file')
    subdirs = ['updated_price']
    excel_file_folder.mkdir(parents=True, exist_ok=True)
    for subdir in subdirs:
        (excel_file_folder / subdir).mkdir(parents=True, exist_ok=True)
    files = list(excel_file_folder.glob('**/*.xlsx'))
    if len(files) == 0:
        print("File Doesn't Exist. Please Select the File!!")
        root = tk.Tk()
        root.withdraw()
        selected_file = askopenfilename(title="Select an Excel File", initialdir=excel_file_folder, 
                        filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if selected_file:
            print(f"Selected file: {selected_file}")
            shutil.copy(selected_file, excel_file_folder)
            files = list(excel_file_folder.glob('**/*.xlsx'))
            file_info = []
            for file in files:                                                     
                # Store the file path and file name as a tuple in the list
                file_info.append({
                    'File Path': file,
                    'File Name': file.name
                })
            print(file_info)
        else:
            print('File Selection Failed. Try Again!!')
    else:
        print('File Exists! Please Proceed Further')
        file_info = []
        for file in files:                                                     
            # Store the file path and file name as a tuple in the list
            file_info.append({
                'File Path': file,
                'File Name': file.name
            })
        print(file_info)
--------------------------------------------------------------------------------------------------------------
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