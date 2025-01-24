import os

def gst_amount(amt: int, gst_rate: float):
    '''
    Formula seperate price of a product 
    into without gst and base price
    '''
    if not (isinstance(amt, (float,int)) and isinstance(gst_rate, float)):
        return f"AMOUNT: {amt} or GST: {gst_rate} values not appropriate"
    gst_amt = amt - (amt * (100/(100 + gst_rate*100)))
    pre_gst_amt = amt - gst_amt
    return round(pre_gst_amt, 2), round(gst_amt, 2)


product_group_1 = ['Bail Kolhu Mustard Oil', 'Bail Kolhu Mustard Oil', 'Bail Kolhu Mustard Oil', 'Bail Kolhu Mustard Oil', 'Bail Kolhu Mustard Oil', 'Bail Kolhu Mustard Oil', 'Bail Kolhu Mustard Oil', 'Nourish Refined Sunflower Oil', 'Nourish Refined Sunflower Oil', 'Nourish Refined Sunflower Oil', 'Nourish Refined Sunflower Oil', 'Nourish Refined Sunflower Oil', 'Nourish Refined Sunflower Oil', 'Nourish Refined Groundnut Oil', 'Nourish Refined Groundnut Oil', 'Nourish Arhar Dal', 'Nourish Arhar Dal', 'Nourish Chana Dal', 'Nourish Chana Dal', 'Nourish Urad Dhuli Dal', 'Nourish Urad Dhuli Dal', 'Nourish Urad Chilka Dal', 'Nourish Urad Chilka Dal', 'Nourish Urad Sabut', 'Nourish Urad Sabut', 'Nourish Moong Dhuli Dal', 'Nourish Moong Dhuli Dal', 'Nourish Moong Chilka Dal', 'Nourish Moong Chilka Dal', 'Nourish Moong Sabut', 'Nourish Moong Sabut', 'Nourish Desi Masoor', 'Nourish Desi Masoor', 'Nourish Masoor Malka', 'Nourish Masoor Malka', 'Nourish Malka Sabut', 'Nourish Malka Sabut', 'Nourish Rajma Chitra', 'Nourish Rajma Chitra', 'Nourish Rajma Lal', 'Nourish Rajma Lal ', 'Nourish Desi Chana', 'Nourish Desi Chana', 'Nourish Kabuli Chana', 'Nourish Kabuli Chana', 'Nourish Maharani Mixed Dal', 'Nourish Roasted Dalia', 'Nourish Roasted Dalia', 'Nourish Roasted Dalia', 'Nourish Lobia', 'Nourish Flaxseed', 'Nourish Chana Besan', 'Nourish Chana Besan', 'Nourish Chana Besan', 'Nourish Maida ', 'Nourish Maida ', 'Nourish Sooji', 'Nourish Chakki Fresh Atta (Red)', 'Nourish Chakki Fresh Atta (Red)', 'Nourish Multigrain Atta', 'Nourish Multigrain Atta', 'Nourish Basmati Rice', 'Nourish Classic Rice', 'Nourish  Royal Rice', 'Nourish  Classic Rice', 'Nourish  Royal Rice', 'Nourish Platinum Rice', 'Nourish Silver Rice', 'Nourish Kalonji', 'Nourish Moti Elaichi', 'Nourish Hari Elaichi', 'Nourish Tej Patta', 'Nourish Jaivtri', 'Nourish Kali Mirch', 'Nourish Ajwain', 
                   'Nourish Pink Rock Salt (Sendha Namak)', 'Nourish Pink Rock Salt (Sendha Namak)', 'Nourish Pink Rock Salt (Sendha Namak)', 'Nourish Phool Makhana', 'Nourish Jeera', 'Nourish Barik Saunf', 'Nourish Moti Saunf', 'Nourish Methi Dana', 'Nourish Sabut Dhania', 'Nourish Black Salt (Kala Namak)', 'Nourish Black Salt (Kala Namak)', 'Nourish Rai (Mustard Seed)', 'Nourish Kasoori Methi', 'Nourish Laung Sabut', 'Nourish Dal Chini', 'Nourish Desi Ghee', 'Nourish Desi Ghee', 'Nourish Desi Ghee', 'Nourish Macaroni', 'Nourish Macaroni', 'Nourish Macaroni', 'Nourish Vermicelli', 'Nourish Vermicelli', 'Nourish Vermicelli', 'Nourish Roasted Vermicelli', 'Nourish Pasta', 'Nourish Pasta', 'Nourish Pasta', 'Nourish Poha', 'Nourish Tea', 'Nourish Cashew', 'Nourish Walnut', 'Nourish Raisins', 'Nourish Almond', 'Nourish Pistachio', 'Nourish Chia Seeds', 'Nourish Sunflower Seeds ', 'Nourish Pumpkin Seeds ', 'Nourish Gond Katira '],

product_group_2 = 'Nourish Pink Rock Salt (Sendha Namak)', 'Nourish Pink Rock Salt (Sendha Namak)', 'Nourish Pink Rock Salt (Sendha Namak)'