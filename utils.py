import re

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
    Convert the Gst lists to a dict
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
    match_str = re.search(r'\((\d{2}-\d{2}-\d{2})\)', url)
    if match_str:
        date_str = match_str.group(1)
        return date_str
    else:
        return None
    