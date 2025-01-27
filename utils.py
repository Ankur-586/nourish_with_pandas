from master_data.product_with_gst import (productGroup1_GST_5percent, 
                                          productGroup2_GST_0percent, productGroup3_GST_12percent)


def gst_amount(amt: int, gst_rate: float):
    '''
    Formula seperate price of a product 
    into without gst and base price
    '''
    if not (isinstance(amt, (float,int)) and isinstance(gst_rate, float)):
        return f"AMOUNT: {amt} or GST: {gst_rate} values not appropriate"
    gst_amt = amt - (amt * (100/(100 + gst_rate)))
    pre_gst_amt = amt - gst_amt
    return round(pre_gst_amt, 2), round(gst_amt, 2)

def get_masterData():
    data = {}
    data.update({
            'GST 5%': productGroup1_GST_5percent,
            'GST 0%': productGroup2_GST_0percent,
            'GST 12%': productGroup3_GST_12percent
        })
    return data
