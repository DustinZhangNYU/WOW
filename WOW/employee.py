'''
 <WOW Back-end Version 1.0,  No interaction with front-end now, only database operation>
 <04/13/2022> employee.py
    API in employee.py is only available to employee
'''
from config import *
from classes import *

###################### -- EMPLOYEE SELECT -- ######################
'''
    WOW employee fetch all order information
    This is select * from SJD_ORDER
'''
def order_fetchall():
    order = Order()
    query_result = db.get_list('SJD_ORDER','*')
    for i,row, in enumerate(query_result):
        order.order_id.append(row['order_id'])
        order.pickup_date.append(row['pickup_date'])
        order.pickup_loc.append(row['pickup_office_id'])
        order.dropoff_date.append(row['dropoff_date'])
        order.dropoff_loc.append(row['dropoff_office_id'])
        order.start_odometer.append(row['start_odometer'])
        order.end_odometer.append(row['end_odometer'])
        order.daily_odometer_limit.append(row['daily_odometer_limit'])
        order.vin.append(row['vin'])
        order.corp_coupon_id.append(row['corp_coupon_id'])
        order.ind_coupon_id.append(row['ind_coupon_id'])
        order.customer_id.append(row['cust_customer_id'])
    return order

'''
    WOW employee fetch all individual customer information
    This is select * from SJD_IND_CUSTOMER
'''
def ind_cust_fetchall():
    # Join SJD_CUSTOMER & SJD_IND_CUSTOMER
    pass

'''
    WOW employee fetch all corporate customer information
    This is select * from SJD_CORP_CUSTOMER
'''
def corp_cust_fetchall():
    # Join SJD_CUSTOMER & SJD_CORP_CUSTOMER
    pass

'''
    WOW employee fetch all individual coupon information
    This is select * from SJD_IND_COUPON
'''
def ind_coupon_fetchall():
    # Join SJD_COUPON & SJD_IND_COUPON
    pass

'''
    WOW employee fetch all corporate coupon information
    This is select * from SJD_CORP_COUPON
'''
def corp_coupon_fetchall():
    # Join SJD_COUPON & SJD_CORP_COUPON
    pass

'''
    WOW employee fetch all invoice information
    This is select * from SJD_INVOICE
'''
def invoice_fetchall():
    invoice = Invoice()
    query_result = db.get_list('SJD_INVOICE','*')
    for i,row, in enumerate(query_result):
        invoice.id.append(row['invoice_id'])
        invoice.date.append(row['invoice_date'])
        invoice.amount.append(row['invoice_amount'])
        invoice.order_id.append(row['order_id'])
    return invoice

'''
    WOW employee fetch all payment information
    This is select * from SJD_PAYMENT
'''
def payment_fetchall():
    payment = Payment()
    query_result = db.get_list('SJD_PAYMENT','*')
    for i,row, in enumerate(query_result):
        payment.id.append(row['payment_id'])
        payment.date.append(row['payment_date'])
        payment.method.append(row['payment_methtod'])
        payment.card_number.append(row['card_number'])
        payment.invoice_id.append(row['invoice_id'])
    return payment

'''
    WOW employee fetch all neighborhood residents information
    This is select * from SJD_NEIGHBORHOOD_RESIDENTS
'''
def neighborhood_fetchall():
    neighborhood = Neighborhood()
    query_result = db.get_list('SJD_NEIGHBORHOOD_RESIDENTS','*')
    for i,row, in enumerate(query_result):
        neighborhood.id.append(row['neighbor_id'])
        neighborhood.country.append(row['add_country'])
        neighborhood.state.append(row['add_state'])
        neighborhood.street.append(row['add_street'])
        neighborhood.apt.append(row['add_apt'])
        neighborhood.zipcode.append(row['add_zipcode'])
        neighborhood.email.append(row['email_address'])
        neighborhood.phone_number.append(row['phone_number'])
        neighborhood.city.append(row['add_city'])
    return neighborhood

###################### -- EMPLOYEE  INSERT -- ######################
'''
    WOW employee add a new vehicle class record
    This is insert into SJD_VEH_CLASS value(...)
    Fetch c_id, over_m_f, rental_r, c_name from front-end
'''
def vehicle_class_insert():
    c_id = "..."
    over_m_f = "..."
    rental_r = "..."
    c_name = "..."
    data = [c_id,over_m_f,rental_r,c_name]
    table_name = "SJD_VEH_CLASS"
    col_value = ','.join(data)
    try:
        db.insert_row(table_name,col_value)
    except Exception as ex:
        print("Insert Error:" + ex)

'''
    WOW employee add a new vehicle record
    This is insert into SJD_VEHICLES value(...)
'''
def vehicle_insert():
    pass

'''
    WOW employee add a new office record
    This is insert into SJD_OFFICE value(...)
'''
def office_insert():
    pass

'''
    WOW employee add a new coupon record
    This is insert into SJD_COUPON value(...)
'''
def coupon_insert():
    # Also need to insert SJD_IND_COUPON or SJD_CORP_COUPON in this function
    pass

'''
    WOW employee add a new neighborhood record
    This is insert into SJD_NEIGHBORHOOD_RESIDENTS value(...)
'''
def neighborhood_insert():
    pass

###################### -- EMPLOYEE  DELETE -- ######################
'''
    WOW employee delete a vehicle class
    This is delete SJD_VEH_CLASS <where(...)---optional>
    Fetch con_id, con_omf,con_rental,con_name from front-end
'''
def vehicle_class_delete():
    table_name = "SJD_VEH_CLASS"
    con_id = ""
    con_omf = ""
    con_rental = ""
    con_name = ""
    condition = []
    if len(con_id) != 0:
        condition.append("class_id = " + con_id)
    if len(con_omf) != 0:
        condition.append("over_milage_fee = " + con_omf)
    if len(con_rental) != 0:
        condition.append("rental_rate = " + con_rental)
    if len(con_name) != 0:
        condition.append("class_name = " + con_name)
    where = ' and '.join(condition)
    last_id = db.delete_row(table_name,where)

'''
    WOW employee delete a vehicle
    This is delete SJD_VEHICLE <where(...)---optional>
'''
def vehicle_delete():
    pass

'''
    WOW employee delete an office
    This is delete SJD_OFFICE <where(...)---optional>
'''
def office_delete():
    pass

'''
    WOW employee delete a customer
    This is delete SJD_CUSTOMER <where(...)---optional>
'''
def customer_delete():
    # According to the delete rule, need to delete corresponding record in IND_CUSTOMER or CORP_CUSTOMER first
    # Then delete it in CUSTOMER table
    pass

'''
    WOW employee delete a coupon
    This is delete SJD_COUPON <where(...)---optional>
'''
def coupon_delete():
    # According to the delete rule, need to delete corresponding record in IND_COUPON or CORP_COUPON first
    # Then delete it in COUPON table
    pass

'''
    WOW employee delete a neighborhood
    This is delete SJD_NEIGHBORHOOD_RESIDENTS <where(...)---optional>
'''
def neighborhood_delete():
    pass

###################### -- EMPLOYEE  UPDATE -- ######################
'''
    WOW employee update vehicle class information
    This is update SJD_VEH_CLASS set ... <where ... -optional>
    But not support update class_id value(PK)
    Fetch new_omp, new_rental, new_name, con_id, con_omf,con_rental,con_name from front end
'''
def vehicle_class_update():
    table_name = "SJD_VEH_CLASS"
    new_omf = "..."
    new_rental = "..."
    new_name = "..."
    set = ""
    if len(new_omf) != 0:
        set = "over_milage_fee=" + new_omf
    elif len(new_rental) != 0:
        set = "rental_rate=" + new_rental
    elif len(new_name) != 0:
        set = "class_name=" + new_name
    con_id = "..."
    con_omf = "..."
    con_rental = "..."
    con_name = "..."
    condition = []
    if len(con_id) != 0:
        condition.append("class_id = " + con_id)
    if len(con_omf) != 0:
        condition.append("over_milage_fee = " + con_omf)
    if len(con_rental) != 0:
        condition.append("rental_rate = " + con_rental)
    if len(con_name) != 0:
        condition.append("class_name = " + con_name)
    where = ' and '.join(condition)
    db.update_row(table_name,set,where)

'''
    WOW employee update vehicle information
    This is update SJD_VEHICLE set ... <where ... -optional>
    But not support update primary key column
'''
def vehicle_update():
    pass

'''
    WOW employee update office information
    This is update SJD_OFFICE set ... <where ... -optional>
    But not support update primary key column
'''
def office_update():
    pass

'''
    WOW employee update coupon information
    This is update SJD_COUPON set ... <where ... -optional>
    But not support update primary key column
'''
def coupon_update():
    pass

'''
    WOW employee update individual coupon information
    This is update SJD_IND_COUPON set ... <where ... -optional>
    But not support update primary key column
'''
def ind_coupon_update():
    pass

'''
    WOW employee update corporate coupon information
    This is update SJD_CORP_COUPON set ... <where ... -optional>
    But not support update primary key column
'''
def corp_coupon_update():
    pass

'''
    WOW employee update neighborhood information
    This is update SJD_NEIGHBORHOOD_RESIDENTS set ... <where ... -optional>
    But not support update primary key column
'''
def neighborhood_update():
    pass

#db.close()

