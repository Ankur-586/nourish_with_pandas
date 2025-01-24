
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


productGroup1_GST_5percent = [
    ('Bail Kolhu Mustard Oil', '15 Ltr '), ('Bail Kolhu Mustard Oil', '5 L '), ('Bail Kolhu Mustard Oil', '2 L '), ('Bail Kolhu Mustard Oil', '1 L '), 
    ('Bail Kolhu Mustard Oil', '1 L '), ('Bail Kolhu Mustard Oil', '500ml '), ('Bail Kolhu Mustard Oil', '200ml '), ('Nourish Refined Sunflower Oil', '15 Ltr '), 
    ('Nourish Refined Sunflower Oil', '5 L '), ('Nourish Refined Sunflower Oil', '2 L '), ('Nourish Refined Sunflower Oil', '1 L '), ('Nourish Refined Sunflower Oil', '1 L '),
    ('Nourish Refined Sunflower Oil', '500ml '), ('Nourish Refined Groundnut Oil', '1 L'), ('Nourish Refined Groundnut Oil', '500ml '), ('Nourish Arhar Dal', '1 Kg.'),
    ('Nourish Arhar Dal', '500 gm'), ('Nourish Chana Dal', '1 Kg.'), ('Nourish Chana Dal', '500 gm'), ('Nourish Urad Dhuli Dal', '1 Kg.'), ('Nourish Urad Dhuli Dal', '500 gm'), 
    ('Nourish Urad Chilka Dal', '1 Kg.'), ('Nourish Urad Chilka Dal', '500 gm'), ('Nourish Urad Sabut', '1 Kg.'), ('Nourish Urad Sabut', '500 gm'), 
    ('Nourish Moong Dhuli Dal', '1 Kg.'), ('Nourish Moong Dhuli Dal', '500 gm'), ('Nourish Moong Chilka Dal', '1 Kg.'), ('Nourish Moong Chilka Dal', '500 gm'), 
    ('Nourish Moong Sabut', '1 Kg.'), ('Nourish Moong Sabut', '500 gm'), ('Nourish Desi Masoor', '1 Kg.'), ('Nourish Desi Masoor', '500 gm'), ('Nourish Masoor Malka', '1 Kg.'), 
    ('Nourish Masoor Malka', '500 gm'), ('Nourish Malka Sabut', '1 Kg.'), ('Nourish Malka Sabut', '500 gm'), ('Nourish Rajma Chitra', '1 Kg.'), ('Nourish Rajma Chitra', '500 gm'), 
    ('Nourish Rajma Lal', '1 Kg.'), ('Nourish Rajma Lal ', '500 gm'), ('Nourish Desi Chana', '1 Kg.'), ('Nourish Desi Chana', '500 gm'), ('Nourish Kabuli Chana', '1 Kg.'), 
    ('Nourish Kabuli Chana', '500 gm'), ('Nourish Maharani Mixed Dal', '500 gm'), ('Nourish Roasted Dalia', '1 Kg.'), ('Nourish Roasted Dalia', '500 gm'), 
    ('Nourish Roasted Dalia', '200 gm'), ('Nourish Lobia', '500 gm'), ('Nourish Flaxseed', '200 gm'), ('Nourish Chana Besan', '1 Kg.'), ('Nourish Chana Besan', '500 gm'),
    ('Nourish Chana Besan', '200 gm'), ('Nourish Maida ', '1 Kg '), ('Nourish Maida ', '500 gm'), ('Nourish Sooji', '500 gm'), ('Nourish Chakki Fresh Atta (Red)', '10 Kg'),
    ('Nourish Chakki Fresh Atta (Red)', '5 Kg'), ('Nourish Multigrain Atta', '1 Kg.'), ('Nourish Multigrain Atta', '5 Kg'), ('Nourish Basmati Rice', '1 Kg.'),
    ('Nourish Classic Rice', '1 Kg.'), ('Nourish  Royal Rice', '1 Kg.'), ('Nourish  Classic Rice', '5 Kg'), ('Nourish  Royal Rice', '5 Kg'), ('Nourish Platinum Rice', '5 Kg'),
    ('Nourish Silver Rice', '5 Kg'), ('Nourish Kalonji', '100 gm'), ('Nourish Moti Elaichi', '50 gm'), ('Nourish Hari Elaichi', '50 gm'), ('Nourish Tej Patta', '50 gm'),
    ('Nourish Jaivtri', '25 gm'), ('Nourish Kali Mirch', '100 gm'), ('Nourish Ajwain', '100 gm'), ('Nourish Phool Makhana', '50 gm'), ('Nourish Jeera', '100 gm'),
    ('Nourish Barik Saunf', '100 gm'), ('Nourish Moti Saunf', '100 gm'), ('Nourish Methi Dana', '100 gm'), ('Nourish Sabut Dhania', '100 gm'),
    ('Nourish Rai (Mustard Seed)', '100 gm'), ('Nourish Kasoori Methi', '25 gm'), ('Nourish Laung Sabut', '50 gm'), ('Nourish Dal Chini', '50 gm'),
    ('Nourish Vermicelli', '200 gm'), ('Nourish Vermicelli', '450 gm'), ('Nourish Vermicelli', '100 gm'), ('Nourish Roasted Vermicelli', '400 gm'),
    ('Nourish Poha', '500 gm'), ('Nourish Tea', '250 gm'), ('Nourish Cashew', '250 gm'), ('Nourish Walnut', '250 gm'), ('Nourish Raisins', '250 gm'),
    ('Nourish Chia Seeds', '250 gm'), ('Nourish Sunflower Seeds ', '250 gm'), ('Nourish Gond Katira ', '50 gm')
    ]
                   
productGroup2_GST_0percent = [
    ('Nourish Pink Rock Salt (Sendha Namak)', '200 gm'), ('Nourish Pink Rock Salt (Sendha Namak)', '500 gm'), ('Nourish Pink Rock Salt (Sendha Namak)', '1 Kg'), 
    ('Nourish Black Salt (Kala Namak)', '200 gm'), ('Nourish Black Salt (Kala Namak)', '500 gm')
    ]

productGroup3_GST_12percent = [
    ('Nourish Desi Ghee', '1 L'), ('Nourish Desi Ghee', '500 ml'), ('Nourish Desi Ghee', '200 ml'),('Nourish Macaroni', '200 gm'), ('Nourish Macaroni', '450 gm'),
    ('Nourish Macaroni', '85 gm'),('Nourish Pasta', '200 gm'), ('Nourish Pasta', '450 gm'), ('Nourish Pasta', '85 gm'),('Nourish Almond', '250 gm'), 
    ('Nourish Pistachio', '250 gm'), ('Nourish Pumpkin Seeds ', '250 gm'),
    ]

def get_masterData():
    data = {}
    data.update({
            'GST 5%': productGroup1_GST_5percent,
            'GST 0%': productGroup2_GST_0percent,
            'GST 12%': productGroup3_GST_12percent
        })
    return data
