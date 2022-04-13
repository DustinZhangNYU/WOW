'''
 <WOW Back-end Version 1.0,  No interaction with front-end now, only database operation>
 <04/13/2022> customer.py
    API in customer.py is only available to customer
'''

from classes import *
from config import *

# Rent a car
def pickup():
    # Inter a vehicle's vin
    # Check if this vehicle is available (这个列我们Database里还没有)
    # If available, Update this vehicle to be unavailable
    # Update customer's borrowed car record, to trace,  customer rent this car from which office on which date,..., (这个追踪未完成订单的表我们database里还没有）
    pass

# Return a car and pay for the service
def dropoff():
    # Update this vehicle to be available
    # Update this vehicle's office_id based on the dropoff location
    # Check if this customer use a coupon and check if it's a validate coupon
    # If it's an individual coupon then delete the coupon from DB
    # Update Order table and trigger will automatically create invoice
    # Update Payment table
    pass

###################### -- CUSTOMER SELECT THEIR PERSONAL INFORMATION -- ######################
'''
    Fetch customer's personal information, return value to front-end and display to user
    <where customer_id = ... --mandatory>
'''
def fetch_customer():
    pass

'''
    Fetch customer's coupons
    <where customer_id = ... --mandatory>
'''
def fetch_coupon():
    # Check if this customer is a corporate customer
    # If no then cannot fetch coupon information
    pass

'''
    Fetch customer's invoice
    <where invoice_id = ... --mandatory>
'''
def fetch_invoice():
    pass

'''
    Fetch customer's payment history
    <where payment_id = ... --mandatory>
'''
def fetch_payment():
    pass

'''
    Fetch customer's order history
    <where customer_id = ... --mandatory>
'''
def fetch_order():
    pass

###################### -- CUSTOMER UPDATE THEIR PERSONAL INFORMATION -- ######################
'''
    Update customer's personal information
    This is update customer/ind_customer/corp_customer set ... <where customer_id = ... --mandatory>
'''
def personal_cust_update():
    pass
