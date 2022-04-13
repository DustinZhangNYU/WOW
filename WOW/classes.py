'''
 <WOW Back-end Version 1.0, interaction with front-end now, only database operation>
 <04/13/2022> class.py
    Define class for each table in MySQL database
    Store query result into class object, each column in the table is stored as a list
    Query functions in app.py return class object back to front-end
    Front-end display object's attribute values
'''
class Vehicle_Classes():
    class_id = []
    over_milage_fee = []
    rental_rate = []
    class_name = []
    last_id = 0

class Vehicles():
    make = []
    model = []
    year = []
    vin = []
    lic_plt_num = []
    class_id = []
    office_id = []
    last_id = ""

class Office():
    id = []
    country = []
    state = []
    street = []
    unit = []
    zipcode = []
    phone_number = []
    city = []

# class Customer():

class IndCust():
    id = []
    country = []
    state = []
    street = []
    unit = []
    zipcode = []
    email = []
    phone_number = []
    type = []
    city = []
    last_name = []
    first_name = []
    dri_lic_num = []
    ins_com_name = []
    ins_pol_num = []
    middle_name = []

class CorCust():
    id = []
    country = []
    state = []
    street = []
    unit = []
    zipcode = []
    email = []
    phone_number = []
    type = []
    city = []
    corp_name = []
    regi_num = []
    emp_id = []
    coupon_id = []

#class Coupon():

class IndCoupon():
    id = []
    discount_amount = []
    type = []
    expiration_date = []
    start_date = []

class CorCoupon():
    id = []
    discount_amount = []
    type = []
    company_name = []

class Invoice():
    id = []
    date = []
    amount = []
    order_id = []

class Neighborhood():
    id = []
    country = []
    state = []
    street = []
    apt = []
    zipcode = []
    email = []
    phone_number = []
    city = []

class Order():
    order_id = []
    pickup_date = []
    pickup_loc = []
    dropoff_date = []
    dropoff_loc = []
    start_odometer = []
    end_odometer = []
    daily_odometer_limit = []
    vin = []
    corp_coupon_id = []
    ind_coupon_id = []
    customer_id = []

class Payment():
    id = []
    date = []
    method = []
    card_number = []
    invoice_id = []