'''
 <WOW Back-end Version 2.0,  Add interaction with front-end, No concurrent and attack injection>
 <04/21/2022> api.py
    WOW system APIs in app.py
'''
from config import *

'''
    WOW employee or customer fetch all vehicle class information
    This is select * from SJD_VEH_CLASS
'''
@app.route('/Api/GetVehicleClassList')
def vehicle_class_fetchall():
    query_result = db.get_list('SJD_VEH_CLASS','*')
    return jsonify(query_result)

'''
    WOW employee or customer fetch all vehicle information
    This is select * from SJD_VEHICLES
'''
@app.route('/Api/GetVehiclesList')
def vehicle_fetchall():
    query_result = db.get_list('SJD_VEHICLES','*')
    return jsonify(query_result)

'''
    WOW employee or customer fetch all office information
    This is select * from SJD_OFFICE
'''
@app.route('/Api/GetOfficeList')
def office_fetchall():
    query_result = db.get_list('SJD_OFFICE','*')
    return jsonify(query_result)

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
@app.route('/Api/GetOrderList')
def order_fetchall():
    query_result = db.get_list('SJD_ORDER','*')
    return jsonify(query_result)

'''
    WOW employee fetch all individual customer information
    This is select * from SJD_IND_CUSTOMER
'''
@app.route('/Api/GetIndCustomerList')
def ind_cust_fetchall():
    # Join SJD_CUSTOMER & SJD_IND_CUSTOMER
    sql = 'select * from SJD_IND_CUSTOMER a join SJD_CUSTOMER b using (cust_customer_id)'
    query_result = db.get_sql_res(sql)
    return jsonify(query_result)

'''
    WOW employee fetch all corporate customer information
    This is select * from SJD_CORP_CUSTOMER
'''
@app.route('/Api/GetCorpCustomerList')
def corp_cust_fetchall():
    # Join SJD_CUSTOMER & SJD_CORP_CUSTOMER
    sql = 'select * from SJD_CORP_CUSTOMER a join SJD_CUSTOMER b using (cust_customer_id)'
    query_result = db.get_sql_res(sql)
    return jsonify(query_result)

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
@app.route('/Api/GetInvoiceList')
def invoice_fetchall():
    query_result = db.get_list('SJD_INVOICE','*')
    return jsonify(query_result)

'''
    WOW employee fetch all payment information
    This is select * from SJD_PAYMENT
'''
@app.route('/Api/GetPaymentList')
def payment_fetchall():
    query_result = db.get_list('SJD_PAYMENT','*')
    return jsonify(query_result)

'''
    WOW employee fetch all neighborhood residents information
    This is select * from SJD_NEIGHBORHOOD_RESIDENTS
'''
@app.route('/Api/GetNeighborList')
def neighborhood_fetchall():
    query_result = db.get_list('SJD_NEIGHBORHOOD_RESIDENTS','*')
    return jsonify(query_result)

###################### -- EMPLOYEE  INSERT -- ######################
'''
    WOW employee add a new vehicle class record
    This is insert into SJD_VEH_CLASS value(...)
    Fetch c_id, over_m_f, rental_r, c_name from front-end
    Front-end use POST method send data to back-end api
'''
@app.route('/Api/InsertVehicleClass',methods=['POST'])
def vehicle_class_insert():
    new_data = request.get_json()
    # this class_id is that variable name in js file
    new_id = new_data['class_id']
    new_omf = new_data['over_milage_fee']
    new_rental = new_data['rental_rate']
    new_name = "'" + new_data['class_name'] + "'"
    data = [new_id,new_omf,new_rental,new_name]
    table_name = "SJD_VEH_CLASS"
    col_value = ','.join(data)
    try:
        db.insert_row(table_name,col_value)
        # This 'result' is named in front-end
        return jsonify({'result':True})
    except Exception as ex:
        print(ex)
        return jsonify({'result':False})

'''
    WOW employee add a new vehicle record
    This is insert into SJD_VEHICLES value(...)
'''
@app.route('/Api/InsertVehicle',methods=['POST'])
def vehicle_insert():
    new_data = request.get_json()
    new_make = "'" + new_data['make'] + "'"
    new_model = "'" + new_data['model'] + "'"
    new_year = "'" + new_data['year'] + "'"
    new_vin = "'" + new_data['vin'] + "'"
    new_plt = "'" + new_data['lic_plt_num'] + "'"
    new_cid = new_data['class_id']
    new_office = new_data['office_id']
    data = [new_make,new_model,new_year,new_vin,new_plt,new_cid,new_office]
    col_val = ','.join(data)
    table_name = "SJD_VEHICLES"
    try:
        db.insert_row(table_name,col_val)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})

'''
    WOW employee add a new office record
    This is insert into SJD_OFFICE value(...)
'''
@app.route('/Api/InsertOffice',methods=['POST'])
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
    data = [new_id,new_cou,new_st,new_str,new_unit,new_zip,new_ph,new_ci]
    col_val = ','.join(data)
    table_name = "SJD_OFFICE"
    try:
        db.insert_row(table_name,col_val)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})

'''
    WOW employee add a new coupon record
    This is insert into SJD_COUPON value(...)
'''
@app.route('/Api/InsertCoupon',methods=['POST'])
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
        db.insert_row(table_name,col_val)
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})

    if new_type == "'I'":
        # Individual
        new_exp = "'" + new_data['expiration_date'] + "'"
        new_start = "'" + new_data['start_date'] + "'"
        data_i = [new_id,new_exp,new_start]
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
        data_c = [new_id,new_company]
        col_val_c = ','.join(data_c)
        table_name_c = "SJD_CORP_COUPON"
        try:
            db.insert_row(table_name_c, col_val_c)
            return jsonify({'result': True})
        except Exception as ex:
            print(ex)
            return jsonify({'result': False})

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
@app.route('/Api/DeleteVehicleClass',methods=['POST'])
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
        last_id = db.delete_row(table_name,where)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})

'''
    WOW employee delete a vehicle
    This is delete SJD_VEHICLE <where(...)---optional>
'''
@app.route('/Api/DeleteVehicle',methods=['POST'])
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
        last_id = db.delete_row(table_name,where)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})

'''
    WOW employee delete an office
    This is delete SJD_OFFICE <where(...)---optional>
'''
@app.route('/Api/DeleteOffice',methods=['POST'])
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
        last_id = db.delete_row(table_name,where)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})

'''
    WOW employee delete a customer
    This is delete SJD_CUSTOMER <where(...)---optional>
    Customer deletion is only based on customer_id column
'''
@app.route('/Api/DeleteCustomer',methods=['POST'])
def customer_delete():
    # According to the delete rule, need to delete corresponding record in IND_CUSTOMER or CORP_CUSTOMER first
    # Then delete it in CUSTOMER table
    condition_json = request.get_json()
    table_name = "SJD_CUSTOMER"
    # Check customer type
    con_id = condition_json['cust_customer_id']
    select_col = "cust_cust_type"
    where = "cust_customer_id = " + con_id
    query_result = db.get_one(table_name,select_col,where)
    # Delete IND_CUSTOMER
    if query_result != None and query_result['cust_cust_type'] == 'I':
        last_id_i = db.delete_row("SJD_IND_CUSTOMER", where)
    # Delete CORP_CUSTOMER
    if query_result != None and query_result['cust_cust_type'] == 'C':
        last_id_c = db.delete_row("SJD_CORP_CUSTOMER", where)
    # Delete CUSTOMER
    try:
        last_id = db.delete_row(table_name,where)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})

'''
    WOW employee delete a coupon
    This is delete SJD_COUPON <where(...)---optional>
    Coupon deletion is only based on coupon_id column
'''
@app.route('/Api/DeleteCoupon',methods=['POST'])
def coupon_delete():
    # According to the delete rule, need to delete corresponding record in IND_COUPON or CORP_COUPON first
    # Then delete it in COUPON table
    condition_json = request.get_json()
    table_name = "SJD_COUPON"
    # Check customer type
    con_id = condition_json['coupon_id']
    select_col = "coupon_type"
    where = "coupon_id = " + con_id
    query_result = db.get_one(table_name,select_col,where)
    # Delete IND_COUPON
    if query_result != None and query_result['coupon_type'] == 'I':
        last_id_i = db.delete_row("SJD_IND_COUPON", where)
    # Delete CORP_COUPON
    if query_result != None and query_result['coupon_type'] == 'C':
        last_id_c = db.delete_row("SJD_CORP_COUPON", where)
    # Delete COUPON
    try:
        last_id = db.delete_row(table_name,where)
        return jsonify({'result': True})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})

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
    Update only based on class_id
'''
@app.route('/Api/UpdateVehicleClass',methods=['POST'])
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
            db.update_row(table_name,set,where)
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
@app.route('/Api/UpdateVehicle',methods=['POST'])
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
        query_result = db.get_one("SJD_VEH_CLASS",select_col,select_where)
        # Exist
        if query_result != None:
            set = "class_id=" + new_cid
    elif len(new_office) != 0:
        # Update FK, Check if it exists in parent table
        select_col = "*"
        select_where = "office_id = " + new_office
        query_result = db.get_one("SJD_OFFICE",select_col,select_where)
        # Exist
        if query_result != None:
            set = "office_id=" + new_office
    con_vin = "'" + update_json['vin'] + "'"
    where = ""
    if len(con_vin) != 0:
        where = "vin = " + con_vin
    try:
        if len(set) != 0:
            db.update_row(table_name,set,where)
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
@app.route('/Api/UpdateOffice',methods=['POST'])
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
            db.update_row(table_name,set,where)
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
@app.route('/Api/UpdateCoupon',methods=['POST'])
def coupon_update():
    update_json = request.get_json()
    table_name = "SJD_COUPON"
    new_amount = update_json['discount_amount']
    # 其实是可以修改coupon的类型的吗？ 有点不确定
    new_type = update_json['coupon_type']
    set = ""
    if len(new_amount) != 0:
        set = "discount_amount=" + new_amount
    elif len(new_type) != 0 and new_type in ['C','I']:
        new_type = "'" + new_type + "'"
        set = "coupon_type=" + new_type

    con_id = update_json['coupon_id']
    where = ""
    if len(con_id) != 0:
        where = "coupon_id = " + con_id
    try:
        if len(set) != 0:
            db.update_row(table_name,set,where)
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
@app.route('/Api/UpdateIndCoupon',methods=['POST'])
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
            db.update_row(table_name,set,where)
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
@app.route('/Api/UpdateCorpCoupon',methods=['POST'])
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
            db.update_row(table_name,set,where)
            return jsonify({'result': True})
        else:
            return jsonify({'result': False})
    except Exception as ex:
        print(ex)
        return jsonify({'result': False})

'''
    WOW employee update neighborhood information
    This is update SJD_NEIGHBORHOOD_RESIDENTS set ... <where ... -optional>
    But not support update primary key column
'''
def neighborhood_update():
    pass


'''
 <WOW Back-end Version 2.0,  Add interaction with front-end>
 <04/13/2022> customer.py
    API in customer.py is only available to customer
'''

###################### -- CUSTOMER RENT RETURN and PAY -- ######################
'''
    WOW customers rent a car
    Inter a vehicle's vin
    Check if this vehicle is available (这个列我们Database里还没有,先暂时命名为available)
    If available, Update this vehicle to be unavailable
    Update customer's borrowed car record, to trace, customer rent this car from which office on which date,..., 
    (这个追踪未完成订单的表我们database里还没有), 在代码里先暂时命名为 SJD_NOT_FINISHED_ORDER,这个表主键应该是（customer_id,vin）
'''
@app.route('/Api/Pickup',methods=['POST'])
def pickup():
    data = request.get_json()
    vin_val = "'" + data['vin'] + "'"
    select_col = "available, office_id"
    where = "vin = " + vin_val
    table_name = "SJD_VEHICLES"
    query_result = db.get_one(table_name,select_col,where)
    if query_result != None and query_result['available'] == 'Y':
        # This car is available now
        set = "available = 'N'"
        db.update_row(table_name,set,where)
        pickup_office = query_result['office_id']
        cust_id = data['cust_customer_id']
        pickup_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Default start_odometers are zero
        start_odometer = 0
        # 这是用户自己输入的吗？或者方便实现可以把所有订单的daily_odometer都设置成一个固定的值
        daily_odometer_limit = data['daily_odometer_limit']

        # 用一张另外的 SJD_NOT_FINISHED_ORDER 表先暂时几下谁在哪里什么时候租了哪台车，这台车此时的start_odometers和这个待完成订单的daily_odometer_limit值
        col_data = [cust_id,str(pickup_office),"'"+str(pickup_date)+"'",vin_val,str(start_odometer),daily_odometer_limit]
        col_val = ','.join(col_data)
        last_rec_id = db.insert_row("SJD_NOT_FINISHED_ORDER",col_val)
        return jsonify({'result': True})
    else:
        # This car is not available now
        return jsonify({'result':False})

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
@app.route('/Api/Dropoff',methods=['POST'])
def dropoff():
    data = request.get_json()
    cust_id = data['cust_customer_id']
    res = db.get_one("SJD_NOT_FINISHED_ORDER", "vin", "cust_customer_id = " + cust_id)
    vin_val = "'" + res['vin'] + "'"
    #vin_val = "'" + data['vin'] + "'"
    cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
    table_name = "SJD_VEHICLES"
    set = "available = 'Y'"
    where = "vin = " + vin_val
    db.update_row(table_name,set,where)

    dropoff_office = data['dropoff_office_id']
    set = "office_id = " + dropoff_office
    db.update_row(table_name, set, where)

    # If this is a corporate type customer, then cannot use individual coupon, True: I, False: C
    # Corporate user will use company coupon automatically
    use_corp_coupon = "NULL"
    check_cust_type = True
    res = db.get_one("SJD_CUSTOMER", "cust_cust_type", "cust_customer_id = " + cust_id)
    if res['cust_cust_type'] == 'C':
        check_cust_type = False
        res = db.get_one("SJD_CORP_CUSTOMER", "coupon_id", "cust_customer_id = " + cust_id)
        use_corp_coupon = res['coupon_id']

    use_coupon = data['coupon_id']
    if len(use_coupon) != 0 and check_cust_type == True:
        # Individual customer choose to use a coupon
        ctype = db.get_one("SJD_COUPON", "coupon_type", "coupon_id = " + use_coupon)
        if ctype['coupon_type'] == 'I':
            # This is an individual coupon
            res = db.get_one("SJD_IND_COUPON","expiration_date,start_date","coupon_id = "+use_coupon)
            check_date = compare_time(str(cur_date),str(res['start_date']),str(res['expiration_date']))
            #if check_date == True:
                # Because this coupon is used, thus delete it from database
                #db.delete_row("SJD_IND_COUPON","coupon_id = "+use_coupon)
                #db.delete_row("SJD_COUPON","coupon_id = "+use_coupon)
            if check_date == False:
                use_coupon = "NULL"
    else:
        # Individual customer choose not to use a coupon
        use_coupon = "NULL"

    end_odometer = data['end_odometer']
    sql = "select count(*) from SJD_ORDER"
    query_result = db.get_sql_res(sql)
    order_id = query_result[0]['count(*)'] + 1

    res = db.get_one("SJD_NOT_FINISHED_ORDER","*","cust_customer_id = "+cust_id+" and vin = "+vin_val)
    col_data = [str(order_id),"'"+str(res['pickup_date'])+"'",str(res['pickup_office_id']),"'"+str(cur_date)+"'",str(res['start_odometer']),end_odometer,str(res['daily_odometer_limit']),
                vin_val,dropoff_office,str(use_corp_coupon),use_coupon,cust_id]
    col_val = ','.join(col_data)
    db.insert_row("SJD_ORDER",col_val)

    sql = "select count(*) from SJD_PAYMENT"
    query_result = db.get_sql_res(sql)
    pay_id = query_result[0]['count(*)'] + 1
    pay_method = "'" + data['payment_method'] + "'"
    card_no = "'" + data['card_number'] + "'"
    res = db.get_one("SJD_INVOICE", "invoice_id", "order_id = " + str(order_id))
    col_data = [str(pay_id),"'"+str(cur_date)+"'",pay_method,card_no,str(res['invoice_id'])]
    col_val = ','.join(col_data)
    last_id = db.insert_row("SJD_PAYMENT",col_val)
    last_id = db.delete_row("SJD_NOT_FINISHED_ORDER", "cust_customer_id = " + cust_id + " and vin = " + vin_val)
    return jsonify({'result': True})

###################### -- CUSTOMER SELECT THEIR PERSONAL INFORMATION -- ######################
'''
    Fetch customer's personal information, return value to front-end and display to user
    <where customer_id = ... --mandatory>
'''
@app.route('/Api/FetchCustomer')
def fetch_customer():
    data = request.get_json()
    cust_id = data['cust_customer_id']
    res = db.get_one("SJD_CUSTOMER","cust_cust_type","cust_customer_id = " + cust_id)
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
@app.route('/Api/FetchCoupon')
def fetch_coupon():
    # Check if this customer is a corporate customer
    # If no then cannot fetch coupon information
    data = request.get_json()
    # 感觉这个cust_id应该是costomer 成功login的时候把登录时用的id存入一个后端变量里，否则用户随便在前端输入别人的id也可以查到别人的coupon信息
    cust_id = data['cust_customer_id']
    res = db.get_one("SJD_CUSTOMER", "cust_cust_type", "cust_customer_id = " + cust_id)
    if res['cust_cust_type'] == 'C':
        res = db.get_one("SJD_CORP_CUSTOMER","coupon_id","cust_customer_id = " + cust_id)
        sql = "select * from SJD_CORP_COUPON join SJD_COUPON using (coupon_id) where coupon_id = {}".format(str(res['coupon_id']))
        query_result = db.get_sql_res(sql)
        return jsonify(query_result)
    else:
        return None

'''
    Fetch all invoices of customer
    <where invoice_id = ... --mandatory>
'''
@app.route('/Api/FetchInvoice')
def fetch_invoice():
    data = request.get_json()
    cust_id = data['cust_customer_id']
    orders = db.get_list("SJD_ORDER","order_id","cust_customer_id = {}".format(cust_id))
    invoices = []
    for i,row in enumerate(orders):
        cur_order_id = row['order_id']
        invoice = db.get_one("SJD_INVOICE","*","order_id = {}".format(cur_order_id))
        invoices.append(invoice)
    if len(invoices) == 0:
        return None
    return jsonify(invoices)

'''
    Fetch all payment history of customer
    <where payment_id = ... --mandatory>
'''
@app.route('/Api/FetchPayment')
def fetch_payment():
    data = request.get_json()
    cust_id = data['cust_customer_id']
    orders = db.get_list("SJD_ORDER","order_id","cust_customer_id = {}".format(cust_id))
    payments = []
    for i,row in enumerate(orders):
        cur_order_id = row['order_id']
        invoice = db.get_one("SJD_INVOICE","*","order_id = {}".format(str(cur_order_id)))
        cur_payments = db.get_list("SJD_PAYMENT","*","invoice_id = {}".format(str(invoice['invoice_id'])))
        for p in cur_payments:
            payments.append(p)
    if len(payments) == 0:
        return None
    return jsonify(payments)

'''
    Fetch customer's order history
    <where customer_id = ... --mandatory>
'''
@app.route('/Api/FetchOrder')
def fetch_order():
    data = request.get_json()
    cust_id = data['cust_customer_id']
    orders = db.get_list("SJD_ORDER","*","cust_customer_id = {}".format(cust_id))
    return jsonify(orders)

###################### -- CUSTOMER UPDATE THEIR PERSONAL INFORMATION -- ######################
'''
    Update customer's personal information
    This is update customer/ind_customer/corp_customer set ... <where customer_id = ... --mandatory>
'''
@app.route('/Api/UpdateCustomer',methods=['POST'])
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
    elif len(new_type) != 0 and new_type in ['C','I']:
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
        db.update_row("SJD_CUSTOMER",set,where)
        return jsonify({'result': True})

    res = db.get_one("SJD_CUSTOMER", "cust_cust_type", "cust_customer_id = " + con_id)
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
            res = db.get_one("SJD_CORP_COUPON","*","company_name = "+new_corp_name)
            if res != None:
                new_coupon = res['coupon_id']
                db.update_row("SJD_CORP_CUSTOMER","coupon_id = "+str(new_coupon),where)
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
