import pandas as pd

excel_file_path = r'D:\0-convert_price\MRP New Update (08-01-25).xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl',  index_col=None, skiprows = lambda x: x in [0, 1])

# The "subset" Remove rows where all columns are NaN
df = df.dropna(how='all', inplace=False, subset=['MRP/-'])

# Remove rows where all columns are Unnamed:+
df = df.drop('Unnamed: 6', axis=1)

data = {}
data.update({
        'serial_number': df['S.No'].to_list(),
        'product_names': df['Brand Name'].tolist(),
        'product_mrp': df['MRP/-'].to_list()
    })
print(data)
