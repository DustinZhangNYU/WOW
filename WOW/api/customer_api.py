from flask import jsonify
from config import *

'''
 <WOW Back-end Version 2.0,  Add interaction with front-end>
 <04/13/2022> customer.py
    API in customer.py is only available to customer
'''

###################### -- CUSTOMER RENT RETURN and PAY -- ######################
'''
If the vehicle is already rented, it should be updated in the backend side
- the website would only display results that has already been filtered
- VIN already checked with functions
- Siya Guo, 04/22

    WOW customers rent a car
    Inter a vehicle's vin
    Check if this vehicle is available (这个列我们Database里还没有,先暂时命名为available)
    If available, Update this vehicle to be unavailable
    Update customer's borrowed car record, to trace, customer rent this car from which office on which date,..., 
    (这个追踪未完成订单的表我们database里还没有), 在代码里先暂时命名为 SJD_NOT_FINISHED_ORDER,这个表主键应该是（customer_id,vin）
'''

# following codes should be in the backend folder and doesn't need to interact with frontend
# start_odometer and daily_odometer_limit should be predefined in the database - no interaction with customer
# - Siya Guo, 04/22


@app.route('/Api/Pickup', methods=['POST'])
def pickup():
    data = request.get_json()
    vin_val = "'" + data['vin'] + "'"
    select_col = "available, office_id"
    where = "vin = " + vin_val
    table_name = "SJD_VEHICLES"
    query_result = db.get_one(table_name, select_col, where)
    if query_result != None and query_result['available'] == 'Y':
        # This car is available now
        set = "available = 'N'"
        db.update_row(table_name, set, where)
        pickup_office = query_result['office_id']
        cust_id = data['cust_customer_id']
        pickup_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Default start_odometers are zero
        start_odometer = 0
        # 这是用户自己输入的吗？或者方便实现可以把所有订单的daily_odometer都设置成一个固定的值
        daily_odometer_limit = data['daily_odometer_limit']

        # 用一张另外的 SJD_NOT_FINISHED_ORDER 表先暂时几下谁在哪里什么时候租了哪台车，这台车此时的start_odometers和这个待完成订单的daily_odometer_limit值
        col_data = [cust_id, str(pickup_office), "'" + str(pickup_date) + "'", vin_val, str(start_odometer),
                    daily_odometer_limit]
        col_val = ','.join(col_data)
        last_rec_id = db.insert_row("SJD_NOT_FINISHED_ORDER", col_val)
        return jsonify({'result': True})
    else:
        # This car is not available now
        return jsonify({'result': False})


# Validation not based on time - the customer would not input dates of the coupon,
# instead, the customer would only input coupon id, the backend should check dates
# according to the id
# Thus, following codes should be in the backend folder instead of the API folder
# - Siya Guo, 04/22


'''
    Check if individual coupon is valid
    If l_time is in [start_t,end_t]
'''


def compare_time(l_time, start_t, end_t):
    s_time = time.mktime(time.strptime(start_t, '%Y-%m-%d %H:%M:%S'))
    e_time = time.mktime(time.strptime(end_t, '%Y-%m-%d %H:%M:%S'))
    log_time = time.mktime(time.strptime(l_time, '%Y-%m-%d'))
    if (float(log_time) >= float(s_time)) and (float(log_time) <= float(e_time)):
        return True
    return False


'''
    WOW customers return a car and pay for the service
    Update this vehicle to be available
    Update this vehicle's office_id based on the dropoff location
    Check if this customer use a coupon and check if it's a validate coupon
    If it's an individual coupon then delete the coupon from DB
    Update Order table and trigger will automatically create invoice
    Delete corresponding record in SJD_NOT_FINISHED_ORDER table
    Update Payment table
'''

# Question: shouldn't the coupon be deleted from the database when the customer placed the order
# instead of when returning the car?
# I don't believe the NOT_FINISHED_ORDER is necessary - could add a separate page for the customer,
# where the customer is logged in and can return the car, then we can only changed the rented attribute
#
# - Siya Guo, 04/22


@app.route('/Api/Dropoff', methods=['POST'])
def dropoff():
    data = request.get_json()
    cust_id = data['cust_customer_id']
    res = db.get_one("SJD_NOT_FINISHED_ORDER", "vin",
                     "cust_customer_id = " + cust_id)
    vin_val = "'" + res['vin'] + "'"
    # vin_val = "'" + data['vin'] + "'"
    cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
    table_name = "SJD_VEHICLES"
    set = "available = 'Y'"
    where = "vin = " + vin_val
    db.update_row(table_name, set, where)

    dropoff_office = data['dropoff_office_id']
    set = "office_id = " + dropoff_office
    db.update_row(table_name, set, where)

    # If this is a corporate type customer, then cannot use individual coupon, True: I, False: C
    # Corporate user will use company coupon automatically
    use_corp_coupon = "NULL"
    check_cust_type = True
    res = db.get_one("SJD_CUSTOMER", "cust_cust_type",
                     "cust_customer_id = " + cust_id)
    if res['cust_cust_type'] == 'C':
        check_cust_type = False
        res = db.get_one("SJD_CORP_CUSTOMER", "coupon_id",
                         "cust_customer_id = " + cust_id)
        use_corp_coupon = res['coupon_id']

    use_coupon = data['coupon_id']
    if len(use_coupon) != 0 and check_cust_type == True:
        # Individual customer choose to use a coupon
        ctype = db.get_one("SJD_COUPON", "coupon_type",
                           "coupon_id = " + use_coupon)
        if ctype['coupon_type'] == 'I':
            # This is an individual coupon
            res = db.get_one(
                "SJD_IND_COUPON", "expiration_date,start_date", "coupon_id = " + use_coupon)
            check_date = compare_time(str(cur_date), str(
                res['start_date']), str(res['expiration_date']))
            # if check_date == True:
            # Because this coupon is used, thus delete it from database
            # db.delete_row("SJD_IND_COUPON","coupon_id = "+use_coupon)
            # db.delete_row("SJD_COUPON","coupon_id = "+use_coupon)
            if check_date == False:
                use_coupon = "NULL"
    else:
        # Individual customer choose not to use a coupon
        use_coupon = "NULL"

    end_odometer = data['end_odometer']
    sql = "select count(*) from SJD_ORDER"
    query_result = db.get_sql_res(sql)
    order_id = query_result[0]['count(*)'] + 1

    res = db.get_one("SJD_NOT_FINISHED_ORDER", "*",
                     "cust_customer_id = " + cust_id + " and vin = " + vin_val)
    col_data = [str(order_id), "'" + str(res['pickup_date']) + "'", str(res['pickup_office_id']),
                "'" + str(cur_date) + "'", str(res['start_odometer']
                                               ), end_odometer, str(res['daily_odometer_limit']),
                vin_val, dropoff_office, str(use_corp_coupon), use_coupon, cust_id]
    col_val = ','.join(col_data)
    db.insert_row("SJD_ORDER", col_val)

    sql = "select count(*) from SJD_PAYMENT"
    query_result = db.get_sql_res(sql)
    pay_id = query_result[0]['count(*)'] + 1
    pay_method = "'" + data['payment_method'] + "'"
    card_no = "'" + data['card_number'] + "'"
    res = db.get_one("SJD_INVOICE", "invoice_id",
                     "order_id = " + str(order_id))
    col_data = [str(pay_id), "'" + str(cur_date) + "'",
                pay_method, card_no, str(res['invoice_id'])]
    col_val = ','.join(col_data)
    last_id = db.insert_row("SJD_PAYMENT", col_val)
    last_id = db.delete_row("SJD_NOT_FINISHED_ORDER",
                            "cust_customer_id = " + cust_id + " and vin = " + vin_val)
    return jsonify({'result': True})


###################### -- CUSTOMER SELECT THEIR PERSONAL INFORMATION -- ######################
'''
    Fetch customer's personal information, return value to front-end and display to user
    <where customer_id = ... --mandatory>
'''
# Home page for the user not
# -home page for user: customer information, coupon id (multiple), payment, order, invoice?
# Made slight changes to the order of following codes according to chronological order that a
# customer would follow
#
# The following information could only be accessed within login sessions.

# - Siya Guo, 04/22


@app.route("/user-profile")
# @app.route('/Api/FetchCustomer')
def fetch_customer():
    data = request.get_json()
    cust_id = data['cust_customer_id']
    res = db.get_one("SJD_CUSTOMER", "cust_cust_type",
                     "cust_customer_id = " + cust_id)
    query_result = None
    if res['cust_cust_type'] == 'I':
        sql = "select * from SJD_CUSTOMER join SJD_IND_CUSTOMER using (cust_customer_id) where cust_customer_id = " + cust_id
        query_result = db.get_sql_res(sql)
    if res['cust_cust_type'] == 'C':
        sql = "select * from SJD_CUSTOMER join SJD_CORP_CUSTOMER using (cust_customer_id) where cust_customer_id = " + cust_id
        query_result = db.get_sql_res(sql)
    return jsonify(query_result)


'''
    Fetch customer's coupons
    <where customer_id = ... --mandatory>
    If fetch error then return None
'''


@app.route("/user-profile")
# @app.route('/Api/FetchCoupon')
def fetch_coupon():
    # Check if this customer is a corporate customer
    # If no then cannot fetch coupon information
    data = request.get_json()
    # 感觉这个cust_id应该是customer 成功login的时候把登录时用的id存入一个后端变量里，否则用户随便在前端输入别人的id也可以查到别人的coupon信息
    cust_id = data['cust_customer_id']
    res = db.get_one("SJD_CUSTOMER", "cust_cust_type",
                     "cust_customer_id = " + cust_id)
    if res['cust_cust_type'] == 'C':
        res = db.get_one("SJD_CORP_CUSTOMER", "coupon_id",
                         "cust_customer_id = " + cust_id)
        sql = "select * from SJD_CORP_COUPON join SJD_COUPON using (coupon_id) where coupon_id = {}".format(
            str(res['coupon_id']))
        query_result = db.get_sql_res(sql)
        return jsonify(query_result)
    else:
        return None


'''
    Fetch all payment history of customer
    <where payment_id = ... --mandatory>
'''


@app.route("/user-profile")
# @app.route('/Api/FetchPayment')
def fetch_payment():
    data = request.get_json()
    cust_id = data['cust_customer_id']
    orders = db.get_list("SJD_ORDER", "order_id",
                         "cust_customer_id = {}".format(cust_id))
    payments = []
    for i, row in enumerate(orders):
        cur_order_id = row['order_id']
        invoice = db.get_one("SJD_INVOICE", "*",
                             "order_id = {}".format(str(cur_order_id)))
        cur_payments = db.get_list(
            "SJD_PAYMENT", "*", "invoice_id = {}".format(str(invoice['invoice_id'])))
        for p in cur_payments:
            payments.append(p)
    if len(payments) == 0:
        return None
    return jsonify(payments)


'''
    Fetch customer's order history
    <where customer_id = ... --mandatory>
'''


@app.route("/user-profile")
# @app.route('/Api/FetchOrder')
def fetch_order():
    data = request.get_json()
    cust_id = data['cust_customer_id']
    orders = db.get_list(
        "SJD_ORDER", "*", "cust_customer_id = {}".format(cust_id))
    return jsonify(orders)


'''
    Fetch all invoices of customer
    <where invoice_id = ... --mandatory>
'''


@app.route("/user-profile")
# @app.route('/Api/FetchInvoice')
def fetch_invoice():
    data = request.get_json()
    cust_id = data['cust_customer_id']
    orders = db.get_list("SJD_ORDER", "order_id",
                         "cust_customer_id = {}".format(cust_id))
    invoices = []
    for i, row in enumerate(orders):
        cur_order_id = row['order_id']
        invoice = db.get_one("SJD_INVOICE", "*",
                             "order_id = {}".format(cur_order_id))
        invoices.append(invoice)
    if len(invoices) == 0:
        return None
    return jsonify(invoices)


###################### -- CUSTOMER UPDATE THEIR PERSONAL INFORMATION -- ######################
'''
    Update customer's personal information
    This is update customer/ind_customer/corp_customer set ... <where customer_id = ... --mandatory>
'''


@app.route('/user-profile', methods=['POST'])
# @app.route('/Api/UpdateCustomer', methods=['POST'])
def personal_cust_update():
    update_json = request.get_json()
    new_cou = update_json['cust_add_country']
    new_st = update_json['cust_add_state']
    new_str = update_json['cust_add_street']
    new_unit = update_json['cust_add_unit']
    new_zip = update_json['cust_add_zipcode']
    new_em = update_json['cust_email_address']
    new_ph = update_json['cust_phone_number']
    new_type = update_json['cust_cust_type']
    new_city = update_json['add_city']

    set = ""
    if len(new_cou) != 0:
        new_cou = "'" + new_cou + "'"
        set = "cust_add_country=" + new_cou
    elif len(new_st) != 0:
        new_st = "'" + new_st + "'"
        set = "cust_add_state=" + new_st
    elif len(new_str) != 0:
        new_str = "'" + new_str + "'"
        set = "cust_add_street=" + new_str
    elif len(new_unit) != 0:
        new_unit = "'" + new_unit + "'"
        set = "cust_add_unit=" + new_unit
    elif len(new_zip) != 0:
        new_zip = "'" + new_zip + "'"
        set = "cust_add_zipcode=" + new_zip
    elif len(new_em) != 0:
        new_em = "'" + new_em + "'"
        set = "cust_email_address=" + new_em
    elif len(new_ph) != 0:
        new_ph = "'" + new_ph + "'"
        set = "cust_phone_number=" + new_ph
    elif len(new_type) != 0 and new_type in ['C', 'I']:
        new_type = "'" + new_type + "'"
        set = "cust_cust_type=" + new_type
    elif len(new_city) != 0:
        new_city = "'" + new_city + "'"
        set = "cust_add_city=" + new_city

    con_id = update_json['cust_customer_id']
    if len(con_id) == 0:
        # Fail, because this customer doesn't input customer_id
        return jsonify({'result': False})
    where = "cust_customer_id = " + con_id

    # This means that a customer want to update an attribute in SJD_CUSTOMER
    if len(set) != 0:
        db.update_row("SJD_CUSTOMER", set, where)
        return jsonify({'result': True})

    res = db.get_one("SJD_CUSTOMER", "cust_cust_type",
                     "cust_customer_id = " + con_id)
    if res['cust_cust_type'] == 'I':
        new_lastn = update_json['last_name']
        new_firstn = update_json['first_name']
        new_dri = update_json['dri_lic_num']
        new_ins_com = update_json['ins_com_name']
        new_pol_num = update_json['ins_pol_num']
        new_middlen = update_json['middle_name']
        if len(new_lastn) != 0:
            new_lastn = "'" + new_lastn + "'"
            set = "last_name=" + new_lastn
        elif len(new_firstn) != 0:
            new_firstn = "'" + new_firstn + "'"
            set = "first_name=" + new_firstn
        elif len(new_dri) != 0:
            new_dri = "'" + new_dri + "'"
            set = "dri_lic_num=" + new_dri
        elif len(new_ins_com) != 0:
            new_ins_com = "'" + new_ins_com + "'"
            set = "ins_com_name=" + new_ins_com
        elif len(new_pol_num) != 0:
            new_pol_num = "'" + new_pol_num + "'"
            set = "ins_pol_num=" + new_pol_num
        elif len(new_middlen) != 0:
            new_middlen = "'" + new_middlen + "'"
            set = "middle_name=" + new_middlen
        # This means that an individual customer want to update an attribute in SJD_IND_CUSTOMER
        if len(set) != 0:
            db.update_row("SJD_IND_CUSTOMER", set, where)
            return jsonify({'result': True})
    elif res['cust_cust_type'] == 'C':
        new_corp_name = update_json['corp_name']
        new_regi = update_json['regi_num']
        new_emp_id = update_json['emp_id']
        if len(new_corp_name) != 0:
            new_corp_name = "'" + new_corp_name + "'"
            res = db.get_one("SJD_CORP_COUPON", "*",
                             "company_name = " + new_corp_name)
            if res != None:
                new_coupon = res['coupon_id']
                db.update_row("SJD_CORP_CUSTOMER",
                              "coupon_id = " + str(new_coupon), where)
                set = "corp_name=" + new_corp_name
            else:
                # Updated corporate name doesn't exist in database
                return jsonify({'result': False})
        elif len(new_regi) != 0:
            new_regi = "'" + new_regi + "'"
            set = "regi_num=" + new_regi
        elif len(new_emp_id) != 0:
            new_emp_id = "'" + new_emp_id + "'"
            set = "emp_id=" + new_emp_id
        # This means that a corporate customer want to update an attribute in SJD_CORP_CUSTOMER
        if len(set) != 0:
            db.update_row("SJD_CORP_CUSTOMER", set, where)
            return jsonify({'result': True})
    # This means that a corporate customer want to update an attribute in SJD_IND_CUSTOMER or an individual customer want to update an attribute in SJD_CORP_CUSTOMER
    return jsonify({'result': False})
