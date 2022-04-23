from config import *

# In summary, approximately codes from lines 112 - 408, 446 - 408 are necessary
# - Siya Guo, 04/22

'''
 <WOW Back-end Version 2.0,  Add interaction with front-end>
 <04/13/2022> employee.py
    API in employee.py is only available to employee
'''

###################### -- EMPLOYEE SELECT -- ######################
'''
    WOW employee fetch all order information
    This is select * from SJD_ORDER
'''

@app.route('/checkout')
# not sure whether it is complete page or checkout page at the moment - Siya Guo, 04/22
# @app.route('/Api/GetOrderList')
def order_fetchall():
    query_result = db.get_list('SJD_ORDER', '*')
    return jsonify(query_result)


'''
    WOW employee fetch all individual customer information
    This is select * from SJD_IND_CUSTOMER
'''

@app.route('register')
# get information from registration page? - Siya Guo, 04/22
# @app.route('/Api/GetIndCustomerList')
def ind_cust_fetchall():
    # Join SJD_CUSTOMER & SJD_IND_CUSTOMER
    sql = 'select * from SJD_IND_CUSTOMER a join SJD_CUSTOMER b using (cust_customer_id)'
    query_result = db.get_sql_res(sql)
    return jsonify(query_result)


'''
    WOW employee fetch all corporate customer information
    This is select * from SJD_CORP_CUSTOMER
'''

# Question: why would the employee needs personal information from customers?
# - Siya Guo, 04/22


@app.route('/Api/GetCorpCustomerList')
def corp_cust_fetchall():
    # Join SJD_CUSTOMER & SJD_CORP_CUSTOMER
    sql = 'select * from SJD_CORP_CUSTOMER a join SJD_CUSTOMER b using (cust_customer_id)'
    query_result = db.get_sql_res(sql)
    return jsonify(query_result)

# Question: why would the employee needs to check the coupon information? Shouldn't that
# be operated by the backend automatically?
# - Siya Guo, 04/22

'''
    WOW employee fetch all individual coupon information
    This is select * from SJD_IND_COUPON
'''

@app.route('/Api/GetIndCouponList')
def ind_coupon_fetchall():
    # Join SJD_COUPON & SJD_IND_COUPON
    sql = 'select * from SJD_IND_COUPON a join SJD_COUPON b using (coupon_id)'
    query_result = db.get_sql_res(sql)
    return jsonify(query_result)


'''
    WOW employee fetch all corporate coupon information
    This is select * from SJD_CORP_COUPON
'''


@app.route('/Api/GetCorpCouponList')
def corp_coupon_fetchall():
    # Join SJD_COUPON & SJD_CORP_COUPON
    sql = 'select * from SJD_CORP_COUPON a join SJD_COUPON b using (coupon_id)'
    query_result = db.get_sql_res(sql)
    return jsonify(query_result)


'''
    WOW employee fetch all invoice information
    This is select * from SJD_INVOICE
'''

# Question: if an employee has access to any customer's payment information,
# there would be serious problems and I don't believe above operations are needed.
# - Siya Guo, 04/22

@app.route('/Api/GetPaymentList')
def payment_fetchall():
    query_result = db.get_list('SJD_PAYMENT', '*')
    return jsonify(query_result)


@app.route('/Api/GetInvoiceList')
def invoice_fetchall():
    query_result = db.get_list('SJD_INVOICE', '*')
    return jsonify(query_result)


'''
    WOW employee fetch all payment information
    This is select * from SJD_PAYMENT
'''

###################### -- EMPLOYEE  INSERT -- ######################
'''
    WOW employee add a new vehicle class record
    This is insert into SJD_VEH_CLASS value(...)
    Fetch c_id, over_m_f, rental_r, c_name from front-end
    Front-end use POST method send data to back-end api
'''

@app.route('/records', methods=['POST'])
# @app.route('/Api/InsertVehicleClass', methods=['POST'])
def vehicle_class_insert():
    new_data = request.get_json()
    # this class_id is that variable name in js file
    new_id = new_data['class_id']
    new_omf = new_data['over_milage_fee']
    new_rental = new_data['rental_rate']
    new_name = "'" + new_data['class_name'] + "'"
    data = [new_id, new_omf, new_rental, new_name]
    table_name = "SJD_VEH_CLASS"
    col_value = ','.join(data)
    try:
        db.insert_row(table_name, col_value)
        # This 'result' is named in front-end
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


'''
    WOW employee add a new vehicle record
    This is insert into SJD_VEHICLES value(...)
'''

@app.route('/records', methods=['POST'])
# @app.route('/Api/InsertVehicle', methods=['POST'])
def vehicle_insert():
    new_data = request.get_json()
    new_make = "'" + new_data['make'] + "'"
    new_model = "'" + new_data['model'] + "'"
    new_year = "'" + new_data['year'] + "'"
    new_vin = "'" + new_data['vin'] + "'"
    new_plt = "'" + new_data['lic_plt_num'] + "'"
    new_cid = new_data['class_id']
    new_office = new_data['office_id']
    data = [new_make, new_model, new_year, new_vin, new_plt, new_cid, new_office]
    col_val = ','.join(data)
    table_name = "SJD_VEHICLES"
    try:
        db.insert_row(table_name, col_val)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


'''
    WOW employee add a new office record
    This is insert into SJD_OFFICE value(...)
'''

@app.route('/records', methods=['POST'])
# @app.route('/Api/InsertOffice', methods=['POST'])
def office_insert():
    new_data = request.get_json()
    new_id = new_data['office_id']
    new_cou = "'" + new_data['add_country'] + "'"
    new_st = "'" + new_data['add_state'] + "'"
    new_str = "'" + new_data['add_street'] + "'"
    new_unit = "'" + new_data['add_unit'] + "'"
    new_zip = "'" + new_data['add_zipcode'] + "'"
    new_ph = "'" + new_data['phone_number'] + "'"
    new_ci = "'" + new_data['add_city'] + "'"
    data = [new_id, new_cou, new_st, new_str, new_unit, new_zip, new_ph, new_ci]
    col_val = ','.join(data)
    table_name = "SJD_OFFICE"
    try:
        db.insert_row(table_name, col_val)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


'''
    WOW employee add a new coupon record
    This is insert into SJD_COUPON value(...)
'''

@app.route('/records', methods=['POST'])
# @app.route('/Api/InsertCoupon', methods=['POST'])
def coupon_insert():
    # Also need to insert SJD_IND_COUPON or SJD_CORP_COUPON in this function
    new_data = request.get_json()
    new_id = new_data['coupon_id']
    new_am = new_data['discount_amount']
    new_type = "'" + new_data['coupon_type'] + "'"
    data = [new_id, new_am, new_type]
    col_val = ','.join(data)
    table_name = "SJD_COUPON"
    try:
        db.insert_row(table_name, col_val)
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})

    if new_type == "'I'":
        # Individual
        new_exp = "'" + new_data['expiration_date'] + "'"
        new_start = "'" + new_data['start_date'] + "'"
        data_i = [new_id, new_exp, new_start]
        col_val_i = ','.join(data_i)
        table_name_i = "SJD_IND_COUPON"
        try:
            db.insert_row(table_name_i, col_val_i)
        except Exception as ex:
            print(ex)
            return jsonify({'result': False})

    if new_type == "'C'":
        # Corprate
        new_company = "'" + new_data['company_name'] + "'"
        data_c = [new_id, new_company]
        col_val_c = ','.join(data_c)
        table_name_c = "SJD_CORP_COUPON"
        try:
            db.insert_row(table_name_c, col_val_c)
            return jsonify({'result': True})
        except Exception as ex:
            print(ex)
            return jsonify({'result': False})


###################### -- EMPLOYEE  DELETE -- ######################
'''
    WOW employee delete a vehicle class
    This is delete SJD_VEH_CLASS <where(...)---optional>
    Fetch con_id, con_omf,con_rental,con_name from front-end
'''

@app.route('/records', methods=['POST'])
# @app.route('/Api/DeleteVehicleClass', methods=['POST'])
def vehicle_class_delete():
    condition_json = request.get_json()
    table_name = "SJD_VEH_CLASS"
    con_id = condition_json['class_id']
    con_omf = condition_json['over_milage_fee']
    con_rental = condition_json['rental_rate']
    con_name = "'" + condition_json['class_name'] + "'"
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
    try:
        last_id = db.delete_row(table_name, where)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


'''
    WOW employee delete a vehicle
    This is delete SJD_VEHICLE <where(...)---optional>
'''

@app.route('/records', methods=['POST'])
# @app.route('/Api/DeleteVehicle', methods=['POST'])
def vehicle_delete():
    condition_json = request.get_json()
    table_name = "SJD_VEHICLES"
    con_make = condition_json['make']
    con_model = condition_json['model']
    con_year = condition_json['year']
    con_vin = condition_json['vin']
    con_plt = condition_json['lic_plt_num']
    con_cid = condition_json['class_id']
    con_office = condition_json['office_id']
    condition = []
    if len(con_make) != 0:
        con_make = "'" + con_make + "'"
        condition.append("make = " + con_make)
    if len(con_model) != 0:
        con_model = "'" + con_model + "'"
        condition.append("model = " + con_model)
    if len(con_year) != 0:
        con_year = "'" + con_year + "'"
        condition.append("year = " + con_year)
    if len(con_vin) != 0:
        con_vin = "'" + con_vin + "'"
        condition.append("vin = " + con_vin)
    if len(con_plt) != 0:
        con_plt = "'" + con_plt + "'"
        condition.append("lic_plt_num = " + con_plt)
    if len(con_cid) != 0:
        condition.append("class_id = " + con_cid)
    if len(con_office) != 0:
        condition.append("office_id = " + con_office)
    where = ' and '.join(condition)
    try:
        last_id = db.delete_row(table_name, where)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


'''
    WOW employee delete an office
    This is delete SJD_OFFICE <where(...)---optional>
'''

@app.route('/records', methods=['POST'])
# @app.route('/Api/DeleteOffice', methods=['POST'])
def office_delete():
    condition_json = request.get_json()
    table_name = "SJD_OFFICE"
    con_id = condition_json['office_id']
    con_cou = condition_json['add_country']
    con_st = condition_json['add_state']
    con_str = condition_json['add_street']
    con_unit = condition_json['add_unit']
    con_zip = condition_json['add_zipcode']
    con_ph = condition_json['phone_number']
    con_city = condition_json['add_city']
    condition = []
    if len(con_id) != 0:
        condition.append("office_id = " + con_id)
    if len(con_cou) != 0:
        con_cou = "'" + con_cou + "'"
        condition.append("add_country = " + con_cou)
    if len(con_st) != 0:
        con_st = "'" + con_st + "'"
        condition.append("add_state = " + con_st)
    if len(con_str) != 0:
        con_str = "'" + con_str + "'"
        condition.append("add_street = " + con_str)
    if len(con_unit) != 0:
        con_unit = "'" + con_unit + "'"
        condition.append("add_unit = " + con_unit)
    if len(con_zip) != 0:
        con_zip = "'" + con_zip + "'"
        condition.append("add_zipcode = " + con_zip)
    if len(con_ph) != 0:
        con_ph = "'" + con_ph + "'"
        condition.append("phone_number = " + con_ph)
    if len(con_city) != 0:
        con_city = "'" + con_city + "'"
        condition.append("add_city = " + con_city)
    where = ' and '.join(condition)
    try:
        last_id = db.delete_row(table_name, where)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


'''
    WOW employee delete a customer
    This is delete SJD_CUSTOMER <where(...)---optional>
    Customer deletion is only based on customer_id column
'''

@app.route('/records', methods=['POST'])
# @app.route('/Api/DeleteCustomer', methods=['POST'])
def customer_delete():
    # According to the delete rule, need to delete corresponding record in IND_CUSTOMER or CORP_CUSTOMER first
    # Then delete it in CUSTOMER table
    condition_json = request.get_json()
    table_name = "SJD_CUSTOMER"
    # Check customer type
    con_id = condition_json['cust_customer_id']
    select_col = "cust_cust_type"
    where = "cust_customer_id = " + con_id
    query_result = db.get_one(table_name, select_col, where)
    # Delete IND_CUSTOMER
    if query_result != None and query_result['cust_cust_type'] == 'I':
        last_id_i = db.delete_row("SJD_IND_CUSTOMER", where)
    # Delete CORP_CUSTOMER
    if query_result != None and query_result['cust_cust_type'] == 'C':
        last_id_c = db.delete_row("SJD_CORP_CUSTOMER", where)
    # Delete CUSTOMER
    try:
        last_id = db.delete_row(table_name, where)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})

# Deleting coupons should be done automatically after it is used or expired - no action required from employee
# - Siya Guo, 04/22

'''
    WOW employee delete a coupon
    This is delete SJD_COUPON <where(...)---optional>
    Coupon deletion is only based on coupon_id column
'''

@app.route('/Api/DeleteCoupon', methods=['POST'])
def coupon_delete():
    # According to the delete rule, need to delete corresponding record in IND_COUPON or CORP_COUPON first
    # Then delete it in COUPON table
    condition_json = request.get_json()
    table_name = "SJD_COUPON"
    # Check customer type
    con_id = condition_json['coupon_id']
    select_col = "coupon_type"
    where = "coupon_id = " + con_id
    query_result = db.get_one(table_name, select_col, where)
    # Delete IND_COUPON
    if query_result != None and query_result['coupon_type'] == 'I':
        last_id_i = db.delete_row("SJD_IND_COUPON", where)
    # Delete CORP_COUPON
    if query_result != None and query_result['coupon_type'] == 'C':
        last_id_c = db.delete_row("SJD_CORP_COUPON", where)
    # Delete COUPON
    try:
        last_id = db.delete_row(table_name, where)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})



###################### -- EMPLOYEE  UPDATE -- ######################
'''
    WOW employee update vehicle class information
    This is update SJD_VEH_CLASS set ... <where ... -optional>
    But not support update class_id value(PK)
    Update only based on class_id
'''

@app.route('/records', methods=['POST'])
# @app.route('/Api/UpdateVehicleClass', methods=['POST'])
def vehicle_class_update():
    update_json = request.get_json()
    table_name = "SJD_VEH_CLASS"
    new_omf = update_json['over_milage_fee']
    new_rental = update_json['rental_rate']
    new_name = update_json['class_name']
    set = ""
    if len(new_omf) != 0:
        set = "over_milage_fee=" + new_omf
    elif len(new_rental) != 0:
        set = "rental_rate=" + new_rental
    elif len(new_name) != 0:
        new_name = "'" + update_json['class_name'] + "'"
        set = "class_name=" + new_name
    con_id = update_json['class_id']
    where = ""
    if len(con_id) != 0:
        where = "class_id = " + con_id
    try:
        if len(set) != 0:
            db.update_row(table_name, set, where)
            return jsonify({'result': True})
        else:
            return jsonify({'result': False})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


'''
    WOW employee update vehicle information
    This is update SJD_VEHICLE set ... <where ... -optional>
    But not support update primary key column
    Update only based on vin
'''

@app.route('/records', methods=['POST'])
# @app.route('/Api/UpdateVehicle', methods=['POST'])
def vehicle_update():
    update_json = request.get_json()
    table_name = "SJD_VEHICLES"
    new_make = update_json['make']
    new_model = update_json['model']
    new_year = update_json['year']
    new_plt = update_json['lic_plt_num']
    new_cid = update_json['class_id']
    new_office = update_json['office_id']
    set = ""
    if len(new_make) != 0:
        new_make = "'" + new_make + "'"
        set = "make=" + new_make
    elif len(new_model) != 0:
        new_model = "'" + new_model + "'"
        set = "model=" + new_model
    elif len(new_year) != 0:
        new_year = "'" + new_year + "'"
        set = "year=" + new_year
    elif len(new_plt) != 0:
        new_plt = "'" + new_plt + "'"
        set = "lic_plt_num=" + new_plt
    elif len(new_cid) != 0:
        # Update FK, Check if it exists in parent table
        select_col = "*"
        select_where = "class_id = " + new_cid
        query_result = db.get_one("SJD_VEH_CLASS", select_col, select_where)
        # Exist
        if query_result != None:
            set = "class_id=" + new_cid
    elif len(new_office) != 0:
        # Update FK, Check if it exists in parent table
        select_col = "*"
        select_where = "office_id = " + new_office
        query_result = db.get_one("SJD_OFFICE", select_col, select_where)
        # Exist
        if query_result != None:
            set = "office_id=" + new_office
    con_vin = "'" + update_json['vin'] + "'"
    where = ""
    if len(con_vin) != 0:
        where = "vin = " + con_vin
    try:
        if len(set) != 0:
            db.update_row(table_name, set, where)
            return jsonify({'result': True})
        else:
            return jsonify({'result': False})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


'''
    WOW employee update office information
    This is update SJD_OFFICE set ... <where ... -optional>
    But not support update primary key column
    Update only based on office_id
'''

@app.route('/records', methods=['POST'])
# @app.route('/Api/UpdateOffice', methods=['POST'])
def office_update():
    update_json = request.get_json()
    table_name = "SJD_OFFICE"
    new_cou = update_json['add_country']
    new_st = update_json['add_state']
    new_str = update_json['add_street']
    new_unit = update_json['add_unit']
    new_zip = update_json['add_zipcode']
    new_ph = update_json['phone_number']
    new_city = update_json['add_city']
    set = ""
    if len(new_cou) != 0:
        new_cou = "'" + new_cou + "'"
        set = "add_country=" + new_cou
    elif len(new_st) != 0:
        new_st = "'" + new_st + "'"
        set = "add_state=" + new_st
    elif len(new_str) != 0:
        new_str = "'" + new_str + "'"
        set = "add_street=" + new_str
    elif len(new_unit) != 0:
        new_unit = "'" + new_unit + "'"
        set = "add_unit=" + new_unit
    elif len(new_zip) != 0:
        new_zip = "'" + new_zip + "'"
        set = "add_zipcode=" + new_zip
    elif len(new_ph) != 0:
        new_ph = "'" + new_ph + "'"
        set = "phone_number=" + new_ph
    elif len(new_city) != 0:
        new_city = "'" + new_city + "'"
        set = "add_city=" + new_city
    con_id = update_json['office_id']
    where = ""
    if len(con_id) != 0:
        where = "office_id = " + con_id
    try:
        if len(set) != 0:
            db.update_row(table_name, set, where)
            return jsonify({'result': True})
        else:
            return jsonify({'result': False})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


'''
    WOW employee update coupon information
    This is update SJD_COUPON set ... <where ... -optional>
    But not support update primary key column
    Update only based on coupon_id
'''

#
# Question: shouldn't the coupon be sent automatically by promotion - no action required from employee
# no need to modify coupons, i guess?
# - Siya Guo, 04/22


@app.route('/Api/UpdateCoupon', methods=['POST'])
def coupon_update():
    update_json = request.get_json()
    table_name = "SJD_COUPON"
    new_amount = update_json['discount_amount']
    # 其实是可以修改coupon的类型的吗？ 有点不确定
    new_type = update_json['coupon_type']
    set = ""
    if len(new_amount) != 0:
        set = "discount_amount=" + new_amount
    elif len(new_type) != 0 and new_type in ['C', 'I']:
        new_type = "'" + new_type + "'"
        set = "coupon_type=" + new_type

    con_id = update_json['coupon_id']
    where = ""
    if len(con_id) != 0:
        where = "coupon_id = " + con_id
    try:
        if len(set) != 0:
            db.update_row(table_name, set, where)
            return jsonify({'result': True})
        else:
            return jsonify({'result': False})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


'''
    WOW employee update individual coupon information
    This is update SJD_IND_COUPON set ... <where ... -optional>
    But not support update primary key column
    Update only based on coupon_id
'''


@app.route('/Api/UpdateIndCoupon', methods=['POST'])
def ind_coupon_update():
    update_json = request.get_json()
    table_name = "SJD_IND_COUPON"
    new_exp = update_json['expiration_date']
    new_start = update_json['start_date']
    set = ""
    if len(new_exp) != 0:
        new_exp = "'" + new_exp + "'"
        set = "expiration_date=" + new_exp
    elif len(new_start) != 0:
        new_start = "'" + new_start + "'"
        set = "start_date=" + new_start
    con_id = update_json['coupon_id']
    where = ""
    if len(con_id) != 0:
        where = "coupon_id = " + con_id
    try:
        if len(set) != 0:
            db.update_row(table_name, set, where)
            return jsonify({'result': True})
        else:
            return jsonify({'result': False})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


'''
    WOW employee update corporate coupon information
    This is update SJD_CORP_COUPON set ... <where ... -optional>
    But not support update primary key column
    Update only based on coupon_id
'''


@app.route('/Api/UpdateCorpCoupon', methods=['POST'])
def corp_coupon_update():
    update_json = request.get_json()
    table_name = "SJD_CORP_COUPON"
    new_company = update_json['company_name']
    set = ""
    if len(new_company) != 0:
        new_company = "'" + new_company + "'"
        set = "company_name=" + new_company
    con_id = update_json['coupon_id']
    where = ""
    if len(con_id) != 0:
        where = "coupon_id = " + con_id
    try:
        if len(set) != 0:
            db.update_row(table_name, set, where)
            return jsonify({'result': True})
        else:
            return jsonify({'result': False})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})


