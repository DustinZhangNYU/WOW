'''
 <WOW Database configuration Version >
 <04/21/2022> config.py
    Configuration file
'''
import hashlib
from flask import Flask, jsonify, request
# from flask_cors import cross_origin
import pymysql
import json
import os
from flask import *
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
    unset_jwt_cookies, jwt_required, JWTManager
import logging
import datetime
import time
import pymysql
import bcrypt
from pymysqlpool.pool import Pool

DB_CONFIG = {
    "pool_name": "wow_pool",
    "host": "35.225.81.63",
    "port": 3306,
    "user": "root",
    "password": "zxxzjs2012!",
    "db": "sjd_wow"
}

pool = Pool(host=DB_CONFIG['host'], port=DB_CONFIG['port'], user=DB_CONFIG['user'], db=DB_CONFIG['db'], password=DB_CONFIG['password'],
            min_size=1, max_size=10, timeout=30.0)
pool.init()


class SQLManager(object):
    def __init__(self):
        self.conn = None
        self.cursor = None

    # Establish a MySQL connection
    def connection(self):
        self.conn = pool.get_conn()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.conn.begin()

    # Fetch all rows from the select result
    def get_list(self, table_name, select_cols, where=None, args=None):
        if where != None and len(where) != 0:
            sql = "Select " + select_cols + " from " + table_name + " where " + where + ";"
        else:
            sql = "Select " + select_cols + " from " + table_name + ";"
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    # Fetch only first row from select result
    def get_one(self, table_name, select_cols, where=None, args=None):
        if where != None and len(where) != 0:
            sql = "Select " + select_cols + " from " + table_name + " where " + where + ";"
        else:
            sql = "Select " + select_cols + " from " + table_name + ";"
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    # Update record and auto commit
    def update_row(self, table_name, set, where=None, args=None):
        if where != None:
            sql = "Update " + table_name + " set " + set + " where " + where + ";"
        else:
            sql = "Update " + table_name + " set " + set + ";"
        self.cursor.execute(sql, args)
        # self.conn.commit()

    # Insert record into table and auto commit, also fetch the primary key value of current last row
    # Cursor.insert_id() can fetch current inserted row's id value
    def insert_row(self, table_name, col_value, args=None):
        sql = "Insert into " + table_name + " values (" + col_value + ");"
        self.cursor.execute(sql, args)
        # self.conn.commit()
        last_id = self.cursor.lastrowid
        return last_id

    # Delete record from table and auto commit, also fetch the primary key value of current last row
    def delete_row(self, table_name, where=None, args=None):
        if where != None and len(where) != 0:
            sql = "Delete from " + table_name + " where " + where + ";"
        else:
            sql = "Delete from " + table_name + ";"
        self.cursor.execute(sql, args)
        # self.conn.commit()
        #last_id = self.cursor.lastrowid
        # return last_id

    # Execute any kind of sql line such as JOIN ...
    def get_sql_res(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    # Close MySQL connection

    def close(self):
        if self.cursor != None:
            self.cursor.close()
        if self.conn != None:
            pool.release(self.conn)
            # self.conn.close()


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "sjd_tandon_2022_APDB"
jwt = JWTManager(app)

# @jwt.token_in_blocklist_loader
# def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
#     jti = jwt_payload["jti"]
#     sql = "Select token_id from sjd_jwt_revoked_token where token_val=%s"
#     db.cursor.execute(sql, (jti,))
#     token = db.cursor.fetchall()
#     print(token is None)
#     return False


@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"


###################### -- LOGIN REGISTER LOGOUT MODULE -- ######################
@app.route('/login-emp', methods=["POST"])
def loginEmp():
    db = SQLManager()
    db.connection()
    employee_account = request.json.get("employee_account", None)
    password = request.json.get("emlpoyee_password", None)
    sql = "select emlpoyee_password from sjd_employee where employee_account=%s"
    query = db.cursor.execute(sql, (employee_account,))
    query_result = db.cursor.fetchone()
    if query_result == None:
        message = {"Status": "400", "message": "Account Not Found"}
        resp = jsonify(message)
        resp.status_code = 400
        print("Email Not Found")
        db.conn.rollback()
        db.close()
        return resp
    passwordFromDB = query_result["emlpoyee_password"]
    if password != passwordFromDB:
        message = {"Status": "400", "message": "Incorrect Password"}
        resp = jsonify(message)
        resp.status_code = 400
        db.conn.rollback()
        db.close()
        return resp
    else:
        access_token = create_access_token(
            identity=employee_account, fresh=True)
        message = {"Status": "200", "message": "Employee Successfully Login!",
                   "access_token": access_token}
        resp = jsonify(message)
        resp.status_code = 200
        print("Successfully Login!")
        db.conn.commit()
        db.close()
        return resp


@app.route('/login', methods=["POST"])
def login():
    db = SQLManager()
    db.connection()
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    sql = "select cust_customer_id, cust_hash_password from sjd_customer where cust_email_address=%s"
    query = db.cursor.execute(sql, (email,))
    query_result = db.cursor.fetchone()
    if query_result == None:
        message = {"Status": "400", "message": "Email Not Found"}
        resp = jsonify(message)
        resp.status_code = 400
        print("Email Not Found")
        db.conn.rollback()
        db.close()
        return resp
    cust_id = query_result["cust_customer_id"]
    if verifyPassword(query_result["cust_hash_password"], password) == False:
        message = {"Status": "400", "message": "Password is incorrect"}
        resp = jsonify(message)
        resp.status_code = 400
        print("Password is incorrect")
        db.conn.rollback()
        db.close()
        return resp
    else:
        access_token = create_access_token(identity=cust_id, fresh=True)
        message = {"Status": "200", "message": "Successfully Login!",
                   "access_token": access_token}
        resp = jsonify(message)
        resp.status_code = 200
        print("Successfully Login!")
        db.conn.commit()
        db.close()
        return resp


def verifyPassword(hashedPassword, password):
    return bcrypt.checkpw(password.encode(), hashedPassword.encode())


@app.route('/register', methods=["POST"])
def register():
    db = SQLManager()
    db.connection()
    request_data = request.get_json()
    email = request_data['email']
    first_name = request_data['firstName']
    last_name = request_data["lastName"]
    password = request_data["password"]
    mobile_phone = request_data["mobile Phone"]
    dln = request_data["driver License Number"]  # Driver license number
    street = request_data["street"]
    unit = request_data["apt/Unit"]
    city = request_data["city"]
    state = request_data["state"]
    country = request_data["country"]
    zipcode = request_data["zipcode"]
    ins_company_name = request_data["ins_company_name"]
    ins_pol_num = request_data["ins_pol_num"]
    middle_name = request_data["middleName"]
    cust_type = request_data["cust_type"]
    # Acquire an X lock
    sql = 'select cust_hash_password from sjd_customer where cust_email_address = %s for update'
    hashpassword = generateSaltPassword(password)
    db.cursor.execute(sql, (email,))
    query_result = db.cursor.fetchone()
    if query_result != None:
        message = {"Status": "400", "message": "Email is Used"}
        resp = jsonify(message)
        resp.status_code = 400
        db.conn.rollback()
        db.close()
        return resp
    else:
        sql = "Insert INTO sjd_customer (cust_add_country, \
            cust_add_state,\
            cust_add_street,\
            cust_add_unit,\
            cust_add_zipcode,\
            cust_email_address,\
            cust_phone_number,\
            cust_cust_type,\
            cust_add_city, \
            cust_hash_password)\
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # insert into sjd_customer
        parameters = (country, state, street, unit, zipcode, email,
                      mobile_phone, cust_type, city, hashpassword)
        try:
            db.cursor.execute(sql, parameters)
        except Exception as ex:
            print(ex)
            message = {"Status": "400", "message": "Bad Data Insertion"}
            resp = jsonify(message)
            resp.status_code = 400
            db.conn.rollback()
            db.close()
            return resp
        sql = "select cust_customer_id from sjd_customer where cust_email_address=%s"
        db.cursor.execute(sql, (email,))
        query_result = db.cursor.fetchone()
        cust_id = query_result["cust_customer_id"]
        if(cust_type == "I"):
            sql = "Insert INTO sjd_ind_customer (cust_customer_id,\
                last_name,\
                first_name,\
                dri_lic_num,\
                ins_com_name,\
                ins_pol_num,\
                middle_name)\
                VALUES(%s,%s,%s,%s,%s,%s,%s)"
            parameters = (cust_id, last_name, first_name, dln,
                          ins_company_name, ins_pol_num, middle_name)
            try:
                db.cursor.execute(sql, parameters)
            except Exception as ex:
                print(ex)
                message = {"Status": "400", "message": "Bad Data Insertion"}
                resp = jsonify(message)
                resp.status_code = 400
                db.conn.rollback()
                db.close()
                return resp
        elif (cust_type == "C"):
            corp_name = request_data["corp_name"]
            regi_num = request_data["regi_num"]
            emp_id = request_data["emp_id"]
            sql = "Insert INTO sjd_corp_customer (cust_customer_id,\
                corp_name,\
                regi_num,\
                emp_id)\
                VALUES( %s, %s, %s, %s)"
            parameters = (cust_id, corp_name, regi_num, emp_id)
            try:
                db.cursor.execute(sql, parameters)
            except Exception as ex:
                print(ex)
                message = {"Status": "400", "message": "Bad Data Insertion"}
                resp = jsonify(message)
                resp.status_code = 400
                db.conn.rollback()
                db.close()
                return resp
        db.conn.commit()
        db.close()
        message = {"Status": "200", "message": "Successfully Registered"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp


def generateSaltPassword(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


'''
 <WOW Back-end Version 2.0,  Add interaction with front-end>
 <04/13/2022> employee.py
    API in employee.py is only available to employee
'''

###################### -- EMPLOYEE SELECT -- ######################

'''
    WOW employee or customer fetch all vehicle class information
    This is select * from SJD_VEH_CLASS
'''
@app.route('/Api/GetVehicleClassList')
def vehicle_class_fetchall():
    db = SQLManager()
    db.connection()
    query_result = db.get_list('SJD_VEH_CLASS', '*')
    db.close()
    return jsonify(query_result)


'''
    WOW employee or customer fetch all vehicle information
    This is select * from SJD_VEHICLES
'''
@app.route('/Api/GetVehiclesList')
def vehicle_fetchall():
    db = SQLManager()
    db.connection()
    query_result = db.get_list('SJD_VEHICLES', '*')
    db.close()
    return jsonify(query_result)


'''
    WOW employee or customer fetch all office information
    This is select * from SJD_OFFICE
'''
@app.route('/Api/GetOfficeList')
def office_fetchall():
    db = SQLManager()
    db.connection()
    query_result = db.get_list('SJD_OFFICE', '*')
    db.close()
    return jsonify(query_result)


'''
    WOW employee fetch all order information
    This is select * from SJD_ORDER
'''
@app.route('/Api/GetOrderList')
def order_fetchall():
    db = SQLManager()
    db.connection()
    query_result = db.get_list('SJD_ORDER', '*')
    db.close()
    return jsonify(query_result)


'''
    WOW employee fetch all individual customer information
    This is select * from SJD_IND_CUSTOMER
'''
@app.route('/Api/GetIndCustomerList')
def ind_cust_fetchall():
    # Join SJD_CUSTOMER & SJD_IND_CUSTOMER
    db = SQLManager()
    db.connection()
    sql = 'select * from SJD_IND_CUSTOMER a join SJD_CUSTOMER b using (cust_customer_id)'
    query_result = db.get_sql_res(sql)
    db.close()
    return jsonify(query_result)


'''
    WOW employee fetch all corporate customer information
    This is select * from SJD_CORP_CUSTOMER
'''
@app.route('/Api/GetCorpCustomerList')
def corp_cust_fetchall():
    db = SQLManager()
    db.connection()
    # Join SJD_CUSTOMER & SJD_CORP_CUSTOMER
    sql = 'select * from SJD_CORP_CUSTOMER a join SJD_CUSTOMER b using (cust_customer_id)'
    query_result = db.get_sql_res(sql)
    db.close()
    return jsonify(query_result)


'''
    WOW employee fetch all individual coupon information
    This is select * from SJD_IND_COUPON
'''
@app.route('/Api/GetIndCouponList')
def ind_coupon_fetchall():
    db = SQLManager()
    db.connection()
    # Join SJD_COUPON & SJD_IND_COUPON
    sql = 'select * from SJD_IND_COUPON a join SJD_COUPON b using (coupon_id)'
    query_result = db.get_sql_res(sql)
    db.close()
    return jsonify(query_result)


'''
    WOW employee fetch all corporate coupon information
    This is select * from SJD_CORP_COUPON
'''
@app.route('/Api/GetCorpCouponList')
def corp_coupon_fetchall():
    db = SQLManager()
    db.connection()
    # Join SJD_COUPON & SJD_CORP_COUPON
    sql = 'select * from SJD_CORP_COUPON a join SJD_COUPON b using (coupon_id)'
    query_result = db.get_sql_res(sql)
    db.close()
    return jsonify(query_result)


'''
    WOW employee fetch all invoice information
    This is select * from SJD_INVOICE
'''
@app.route('/Api/GetInvoiceList')
def invoice_fetchall():
    db = SQLManager()
    db.connection()
    query_result = db.get_list('SJD_INVOICE', '*')
    db.close()
    return jsonify(query_result)


'''
    WOW employee fetch all payment information
    This is select * from SJD_PAYMENT
'''
@app.route('/Api/GetPaymentList')
def payment_fetchall():
    db = SQLManager()
    db.connection()
    query_result = db.get_list('SJD_PAYMENT', '*')
    db.close()
    return jsonify(query_result)


###################### -- EMPLOYEE  INSERT -- ######################
'''
    WOW employee add a new vehicle class record
    This is insert into SJD_VEH_CLASS value(...)
    Fetch c_id, over_m_f, rental_r, c_name from front-end
    Front-end use POST method send data to back-end api
'''
@app.route('/Api/InsertVehicleClass', methods=['POST'])
def vehicle_class_insert():
    new_data = request.get_json()
    db = SQLManager()
    db.connection()
    new_id = 'NULL'
    new_omf = new_data['over_mileage_fee']
    new_rental = new_data['rental_rate']
    new_name = new_data['class_name']
    try:
        sql = "insert into SJD_VEH_CLASS values (%s,%s,%s)"
        db.cursor.execute(sql, (new_omf, new_rental, new_name))
        db.commit()
        db.close()
        message = {"Status": "200", "message": "Successfully Inserted"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Insertion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
    WOW employee add a new vehicle record
    This is insert into SJD_VEHICLES value(...)
'''
@app.route('/Api/InsertVehicle', methods=['POST'])
def vehicle_insert():
    new_data = request.get_json()
    db = SQLManager()
    db.connection()
    new_make = new_data['make']
    new_model = new_data['model']
    new_year = new_data['year']
    new_vin = new_data['vin']
    new_plt = new_data['lic_plt_num']
    new_cid = new_data['class_id']
    new_office = new_data['office_id']
    try:
        # Acquire a lock
        sql = "select * from sjd_vehicles for update;"
        db.get_sql_res(sql)
        # Insert new record
        sql = "insert into sjd_vehicles values(%s,%s,%s,%s,%s,%s,%s)"
        db.cursor.execute(sql, (new_make, new_model, new_year,
                                new_vin, new_plt, new_cid, new_office))
        db.commit()
        db.close()
        message = {"Status": "200", "message": "Successfully Inserted"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Insertion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
    WOW employee add a new office record
    This is insert into SJD_OFFICE value(...)
'''
@app.route('/Api/InsertOffice', methods=['POST'])
def office_insert():
    new_data = request.get_json()
    db = SQLManager()
    db.connection()
    new_id = 'NULL'
    new_cou = new_data['add_country']
    new_st = new_data['add_state']
    new_str = new_data['add_street']
    new_unit = new_data['add_unit']
    new_zip = new_data['add_zipcode']
    new_ph = new_data['phone_number']
    new_ci = new_data['add_city']
    try:
        sql = "insert into SJD_OFFICE values(%s,%s,%s,%s,%s,%s,%s)"
        db.cursor.execute(sql, (new_cou, new_st, new_str,
                                new_unit, new_zip, new_ph, new_ci))
        db.commit()
        db.close()
        message = {"Status": "200", "message": "Successfully Inserted"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Insertion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
    WOW employee add a new coupon record
    This is insert into SJD_COUPON value(...)
'''
@app.route('/Api/InsertCoupon', methods=['POST'])
def coupon_insert():
    # Also need to insert SJD_IND_COUPON or SJD_CORP_COUPON in this function
    new_data = request.get_json()
    db = SQLManager()
    db.connection()
    new_id = 'NULL'
    new_am = new_data['discount_amount']
    new_type = new_data['coupon_type']
    try:
        sql = "insert into SJD_COUPON values (%s,%s)"
        db.cursor.execute(sql, (new_am, new_type))
        new_id = db.cursor.lastrowid
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Insertion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp

    if new_type == "'I'":
        # Individual
        new_exp = new_data['expiration_date']
        new_start = new_data['start_date']
        try:
            sql = "insert into SJD_IND_COUPON values (%s,%s,%s)"
            db.cursor.execute(sql, (new_id, new_exp, new_start))
        except Exception as ex:
            print(ex)
            db.conn.rollback()
            db.close()
            message = {"Status": "400", "message": "Bad Data Insertion"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp

    if new_type == "'C'":
        # Corprate
        new_company = new_data['company_name']
        try:
            sql = "insert into SJD_CORP_COUPON values (%s,%s)"
            db.cursor.execute(sql, (new_id, new_company))
            db.commit()
            db.close()
            message = {"Status": "200", "message": "Successfully Inserted"}
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        except Exception as ex:
            print(ex)
            db.conn.rollback()
            db.close()
            message = {"Status": "400", "message": "Bad Data Insertion"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp


###################### -- EMPLOYEE  DELETE -- ######################
'''
    WOW employee delete a vehicle class
    This is delete SJD_VEH_CLASS <where(...)---optional>
    Fetch con_id, con_omf,con_rental,con_name from front-end
'''
@app.route('/Api/DeleteVehicleClass', methods=['POST'])
def vehicle_class_delete():
    condition_json = request.get_json()
    db = SQLManager()
    db.connection()
    # Acquire a lock
    sql = "select * from sjd_veh_class for update;"
    db.get_sql_res(sql)
    table_name = "SJD_VEH_CLASS"
    con_id = condition_json['class_id']
    con_omf = condition_json['over_mileage_fee']
    con_rental = condition_json['rental_rate']
    con_name = "'" + condition_json['class_name'] + "'"
    condition = []
    if len(con_id) != 0:
        condition.append("class_id = " + con_id)
    if len(con_omf) != 0:
        condition.append("over_mileage_fee = " + con_omf)
    if len(con_rental) != 0:
        condition.append("rental_rate = " + con_rental)
    if len(con_name) != 0:
        condition.append("class_name = " + con_name)
    where = ' and '.join(condition)
    try:
        db.delete_row(table_name, where)
        db.commit()
        db.close()
        message = {"Status": "200", "message": "Successfully Deleted"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Deletion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
    WOW employee delete a vehicle
    This is delete SJD_VEHICLE <where(...)---optional>
'''
@app.route('/Api/DeleteVehicle', methods=['POST'])
def vehicle_delete():
    condition_json = request.get_json()
    db = SQLManager()
    db.connection()
    # Acquire a lock
    sql = "select * from sjd_vehicles for update;"
    db.get_sql_res(sql)

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
        db.delete_row(table_name, where)
        db.commit()
        db.close()
        message = {"Status": "200", "message": "Successfully Deleted"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Deletion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
    WOW employee delete an office
    This is delete SJD_OFFICE <where(...)---optional>
'''
@app.route('/Api/DeleteOffice', methods=['POST'])
def office_delete():
    condition_json = request.get_json()
    db = SQLManager()
    db.connection()
    # Acquire a lock
    sql = "select * from sjd_office for update;"
    db.get_sql_res(sql)

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
        db.delete_row(table_name, where)
        db.commit()
        db.close()
        message = {"Status": "200", "message": "Successfully Deleted"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Deletion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
    WOW employee delete a customer
    This is delete SJD_CUSTOMER <where(...)---optional>
    Customer deletion is only based on customer_id column
'''
@app.route('/Api/DeleteCustomer', methods=['POST'])
def customer_delete():
    # According to the delete rule, need to delete corresponding record in IND_CUSTOMER or CORP_CUSTOMER first
    # Then delete it in CUSTOMER table
    condition_json = request.get_json()
    db = SQLManager()
    db.connection()
    table_name = "SJD_CUSTOMER"
    # Check customer type
    con_id = condition_json['cust_customer_id']
    select_col = "cust_cust_type"
    where = "cust_customer_id = " + con_id
    query_result = db.get_one(table_name, select_col, where)
    # Delete IND_CUSTOMER
    if query_result != None and query_result['cust_cust_type'] == 'I':
        try:
            # Acquire a lock
            sql = "select * from sjd_ind_customer for update;"
            db.get_sql_res(sql)
            sql = "select * from sjd_customer for update;"
            db.get_sql_res(sql)
            db.delete_row("SJD_IND_CUSTOMER", where)
        except Exception as ex:
            print(ex)
            db.conn.rollback()
            db.close()
            message = {"Status": "400", "message": "Bad Data Deletion"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
    # Delete CORP_CUSTOMER
    if query_result != None and query_result['cust_cust_type'] == 'C':
        try:
            # Acquire a lock
            sql = "select * from sjd_corp_customer for update;"
            db.get_sql_res(sql)
            sql = "select * from sjd_customer for update;"
            db.get_sql_res(sql)
            db.delete_row("SJD_CORP_CUSTOMER", where)
        except Exception as ex:
            print(ex)
            db.conn.rollback()
            db.close()
            message = {"Status": "400", "message": "Bad Data Deletion"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
    # Delete CUSTOMER
    try:
        db.delete_row(table_name, where)
        db.commit()
        db.close()
        message = {"Status": "200", "message": "Successfully Deleted"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp

    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Deletion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


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
    db = SQLManager()
    db.connection()
    table_name = "SJD_COUPON"
    # Check customer type
    con_id = condition_json['coupon_id']
    select_col = "coupon_type"
    where = "coupon_id = " + con_id
    query_result = db.get_one(table_name, select_col, where)
    # Delete IND_COUPON
    if query_result != None and query_result['coupon_type'] == 'I':
        try:
            # Acquire a lock
            sql = "select * from sjd_ind_coupon for update;"
            db.get_sql_res(sql)
            sql = "select * from sjd_coupon for update;"
            db.get_sql_res(sql)
            db.delete_row("SJD_IND_COUPON", where)
        except Exception as ex:
            print(ex)
            db.conn.rollback()
            db.close()
            message = {"Status": "400", "message": "Bad Data Deletion"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
    # Delete CORP_COUPON
    if query_result != None and query_result['coupon_type'] == 'C':
        try:
            # Acquire a lock
            sql = "select * from sjd_corp_coupon for update;"
            db.get_sql_res(sql)
            sql = "select * from sjd_coupon for update;"
            db.get_sql_res(sql)
            db.delete_row("SJD_CORP_COUPON", where)
        except Exception as ex:
            print(ex)
            db.conn.rollback()
            db.close()
            message = {"Status": "400", "message": "Bad Data Deletion"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
    # Delete COUPON
    try:
        db.delete_row(table_name, where)
        db.commit()
        db.close()
        message = {"Status": "200", "message": "Successfully Deleted"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Deletion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


###################### -- EMPLOYEE  UPDATE -- ######################
'''
    WOW employee update vehicle class information
    This is update SJD_VEH_CLASS set ... <where ... -optional>
    But not support update class_id value(PK)
    Update only based on class_id
'''
@app.route('/Api/UpdateVehicleClass', methods=['POST'])
def vehicle_class_update():
    update_json = request.get_json()
    db = SQLManager()
    db.connection()
    table_name = "SJD_VEH_CLASS"
    new_omf = update_json['over_mileage_fee']
    new_rental = update_json['rental_rate']
    new_name = update_json['class_name']
    set = ""
    if len(new_omf) != 0:
        set = "over_mileage_fee=" + new_omf
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
            # Acquire a lock
            sql = "select * from sjd_veh_class where class_id = {} for update;".format(
                con_id)
            db.get_sql_res(sql)
            db.update_row(table_name, set, where)
            db.commit()
            db.close()
            message = {"Status": "200", "message": "Successfully Updated"}
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        else:
            db.commit()
            db.close()
            message = {"Status": "400",
                       "message": "No data need to be updated"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Update"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
    WOW employee update vehicle information
    This is update SJD_VEHICLE set ... <where ... -optional>
    But not support update primary key column
    Update only based on vin
'''
@app.route('/Api/UpdateVehicle', methods=['POST'])
def vehicle_update():
    update_json = request.get_json()
    db = SQLManager()
    db.connection()
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
            # Acquire a lock
            sql = "select * from sjd_vehicles where vin = {} for update;".format(
                con_vin)
            db.get_sql_res(sql)
            db.update_row(table_name, set, where)
            db.commit()
            db.close()
            message = {"Status": "200", "message": "Successfully Updated"}
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        else:
            db.commit()
            db.close()
            message = {"Status": "400",
                       "message": "No data need to be updated"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Update"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
    WOW employee update office information
    This is update SJD_OFFICE set ... <where ... -optional>
    But not support update primary key column
    Update only based on office_id
'''
@app.route('/Api/UpdateOffice', methods=['POST'])
def office_update():
    update_json = request.get_json()
    db = SQLManager()
    db.connection()
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
            # Acquire a lock
            sql = "select * from sjd_office where office_id = {} for update;".format(
                con_id)
            db.get_sql_res(sql)
            db.update_row(table_name, set, where)
            db.commit()
            db.close()
            message = {"Status": "200", "message": "Successfully Updated"}
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        else:
            db.commit()
            db.close()
            message = {"Status": "400",
                       "message": "No data need to be updated"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Update"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
    WOW employee update coupon information
    This is update SJD_COUPON set ... <where ... -optional>
    But not support update primary key column
    Update only based on coupon_id
'''
@app.route('/Api/UpdateCoupon', methods=['POST'])
def coupon_update():
    update_json = request.get_json()
    db = SQLManager()
    db.connection()
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
            # Acquire a lock
            sql = "select * from sjd_coupon where coupon_id = {} for update;".format(
                con_id)
            db.get_sql_res(sql)
            db.update_row(table_name, set, where)
            db.commit()
            db.close()
            message = {"Status": "200", "message": "Successfully Updated"}
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        else:
            db.commit()
            db.close()
            message = {"Status": "400",
                       "message": "No data need to be updated"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Update"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
    WOW employee update individual coupon information
    This is update SJD_IND_COUPON set ... <where ... -optional>
    But not support update primary key column
    Update only based on coupon_id
'''
@app.route('/Api/UpdateIndCoupon', methods=['POST'])
def ind_coupon_update():
    update_json = request.get_json()
    db = SQLManager()
    db.connection()
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
            # Acquire a lock
            sql = "select * from sjd_ind_coupon where coupon_id = {} for update;".format(
                con_id)
            db.get_sql_res(sql)
            db.update_row(table_name, set, where)
            db.commit()
            db.close()
            message = {"Status": "200", "message": "Successfully Updated"}
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        else:
            db.commit()
            db.close()
            message = {"Status": "400",
                       "message": "No data need to be updated"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Update"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
    WOW employee update corporate coupon information
    This is update SJD_CORP_COUPON set ... <where ... -optional>
    But not support update primary key column
    Update only based on coupon_id
'''
@app.route('/Api/UpdateCorpCoupon', methods=['POST'])
def corp_coupon_update():
    update_json = request.get_json()
    db = SQLManager()
    db.connection()
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
            # Acquire a lock
            sql = "select * from sjd_corp_coupon where coupon_id = {} for update;".format(
                con_id)
            db.get_sql_res(sql)
            db.update_row(table_name, set, where)
            db.commit()
            db.close()
            message = {"Status": "200", "message": "Successfully Updated"}
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        else:
            db.commit()
            db.close()
            message = {"Status": "400",
                       "message": "No data need to be updated"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Update"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


'''
 <WOW Back-end Version 2.0,  Add interaction with front-end>
 <04/13/2022> customer.py
    API in customer.py is only available to customer
'''

###################### -- CUSTOMER RENT RETURN and PAY -- ######################

'''
    WOW customers search available cars
'''
@app.route('/search-cars', methods=['POST'])
def searchCar():
    from decimal import Decimal

    class DecimalEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return str(obj)
            return json.JSONEncoder.default(self, obj)
    data = request.get_json()
    # Acquire a conn from pool
    db = SQLManager()
    db.connection()
    className = data["class_name"]
    location = data["State"]
    sql = "SELECT over_mileage_fee,rental_rate,make,model,year from sjd_veh_class join sjd_vehicles using (class_id) join sjd_office using (office_id) where class_name =%s and add_state=%s and available='Y'"
    db.cursor.execute(sql, (className, location))
    result = db.cursor.fetchall()
    db.conn.commit()
    db.close()
    return json.dumps(result, cls=DecimalEncoder)


'''
    WOW customers rent a car
    Inter a vehicle's vin
'''
@app.route('/review', methods=['POST'])
@jwt_required()
def pickup():
    data = request.get_json()
    # Acquire a conn from pool
    db = SQLManager()
    db.connection()
    # Acquire a vehicle vin and customer id
    vin_val = data['vin']
    cust_id = get_jwt_identity()

    # Acquire a X lock and Check available status
    sql = "select available, office_id from sjd_vehicles where vin=%s for update"
    db.cursor.execute(sql, (vin_val,))
    query_result = db.cursor.fetchone()
    if query_result != None and query_result['available'] == 'Y':
        # This car is available now and update it to be unavailable
        sql = "Update sjd_vehicles set available = 'N' where vin=%s"
        try:
            db.cursor.execute(sql, (vin_val,))
        except Exception as ex:
            print(ex)
            db.conn.rollback()
            db.close()
            message = {"Status": "400", "message": "Bad Data Updating"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
        # Default start_odometer is 0, daily_odometer_limit is 500
        start_odometer = 0
        daily_odometer_limit = 500
        pickup_office = query_result['office_id']
        pickup_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payment_method = data['payment_method']
        card_numer = data['card_number']
        coupon_id = data['coupon_id']

        sql = "Insert INTO sjd_not_finished_order (cust_customer_id,\
            pickup_office_id,\
            pickup_date,\
            vin,\
            start_odometer,\
            daily_odometer_limit,\
            payment_method,\
            card_number,\
            coupon_id)\
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            db.cursor.execute(sql, (cust_id, str(pickup_office), str(
                pickup_date), vin_val, str(start_odometer), daily_odometer_limit, payment_method, card_numer, coupon_id))
        except Exception as ex:
            print(ex)
            db.conn.rollback()
            db.close()
            message = {"Status": "400", "message": "Bad Data Insertion"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
        db.conn.commit()
        db.close()
        message = {"Status": "200", "message": "Successfully Booked"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    else:
        message = {"Status": "400",
                   "message": "Car doesn't exist or already booked"}
        resp = jsonify(message)
        resp.status_code = 400
        db.conn.rollback()
        db.close()
        return resp


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
@app.route('/Api/Dropoff', methods=['POST'])
@jwt_required()
def dropoff():
    # Acquire a conn from pool
    db = SQLManager()
    db.connection()

    data = request.get_json()
    cust_id = get_jwt_identity()
    sql = "Select vin from SJD_NOT_FINISHED_ORDER where cust_customer_id=%s"
    try:
        db.cursor.execute(sql, (cust_id,))
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Cannot fetch the data"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp

    vin_val_res = db.cursor.fetchone()
    vin_val = vin_val_res['vin']
    cur_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Acquire a lock
    sql = "select * from sjd_vehicles where vin = {} for update".format(
        vin_val)
    db.get_sql_res(sql)

    # Update vehicle to be available
    sql = "Update SJD_VEHICLES set available='Y' where vin=%s"
    try:
        db.cursor.execute(sql, (vin_val,))
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Updating"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp
    # Modify vehicle's office id to be current dropoff location
    dropoff_office = data['dropoff_office_id']
    sql = "Update SJD_VEHICLES set dropoff_office=%s where vin=%s"
    try:
        db.cursor.execute(sql, (vin_val, vin_val))
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Updating"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp

    # Acquire information from "not_finished_order" table
    sql = "Select * from SJD_NOT_FINISHED_ORDER where cust_customer_id = %s and vin = %s"
    db.cursor.execute(sql, (cust_id, vin_val))
    order_res = db.cursor.fetchone()

    # If this is a corporate type customer, then cannot use individual coupon, True: I, False: C
    # Corporate user will use company coupon automatically
    use_corp_coupon = "NULL"
    check_cust_type = True
    sql = "Select cust_cust_type from SJD_CUSTOMER where cust_customer_id=%s"
    db.cursor.execute(sql, (cust_id,))
    res = db.cursor.fetchone()
    if res['cust_cust_type'] == 'C':
        check_cust_type = False
        sql = "Select coupon_id from SJD_CORP_CUSTOMER where cust_customer_id=%s"
        db.cursor.execute(sql, (cust_id,))
        res = db.cursor.fetchone()
        use_corp_coupon = res['coupon_id']
    use_coupon = order_res['coupon_id']
    if len(use_coupon) != 0 and check_cust_type == True:
        # Individual customer choose to use a coupon
        sql = "Select coupon_type from SJD_COUPON where coupon_id=%s"
        db.cursor.execute(sql, (use_coupon,))
        ctype = db.cursor.fetchone()
        if ctype['coupon_type'] == 'I':
            # This is an individual coupon
            sql = "Select expiration_date,start_date from SJD_IND_COUPON where coupon_id=%s for update"
            db.cursor.execute(sql, (use_coupon,))
            res = db.cursor.fetchone()
            check_date = compare_time(str(cur_date), str(
                res['start_date']), str(res['expiration_date']))
            if check_date == True:
                sql = "Update SJD_IND_COUPON set expiration_date = '1995-09-01'"
                db.cursor.execute(sql, None)
            if check_date == False:
                use_coupon = "NULL"
    else:
        # Individual customer choose not to use a coupon
        use_coupon = "NULL"

    end_odometer = data['end_odometer']
    order_id = 'NULL'

    sql = "Insert INTO sjd_order (pickup_date,\
            pickup_office_id,\
            pickup_date,\
            start_odometer,\
            end_odometer,\
            daily_odometer_limit),\
            vin,\
            dropoff_office_id,\
            corp_coupon_id,\
            ind_coupon_id,\
            cust_customer_id)\
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        db.cursor.execute(sql, (str(order_res['pickup_date']), str(order_res['pickup_office_id']),
                                str(cur_date), str(order_res['start_odometer']), end_odometer, str(
                                    order_res['daily_odometer_limit']), vin_val,
                                dropoff_office, str(use_corp_coupon), use_coupon, cust_id))
        new_order_id = db.cursor.lastrowid
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Insertion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp

    pay_method = order_res['payment_method']
    card_no = order_res['card_number']
    sql = "Select invoice_id from SJD_INVOICE where order_id = %s"
    db.cursor.execute(sql, (new_order_id,))
    res = db.cursor.fetchone()
    sql = "Insert INTO sjd_payment (payment_date,\
            payment_method,\
            card_number,\
            invoice_id,\
            VALUES (%s,%s,%s,%s)"
    try:
        db.cursor.execute(sql, (str(cur_date), pay_method,
                                card_no, str(res['invoice_id'])))
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400", "message": "Bad Data Insertion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp
    sql = "Delete from SJD_NOT_FINISHED_ORDER where cust_customer_id = %s and vin = %s"
    try:
        db.cursor.execute(sql, (cust_id, vin_val))
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        db.close()
        message = {"Status": "400",
                   "message": "Bad NOT FINISHED ORDER Deletion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp
    db.conn.commit()
    db.close()
    message = {"Status": "200", "message": "Successfully Returned"}
    resp = jsonify(message)
    resp.status_code = 200
    return resp


###################### -- CUSTOMER SELECT THEIR PERSONAL INFORMATION -- ######################
'''
    Fetch customer's personal information, return value to front-end and display to user
    <where customer_id = ... --mandatory>
'''
@app.route("/user-profile")
@jwt_required()
def fetch_customer():
    # Acquire a conn from pool
    db = SQLManager()
    db.connection()
    cust_id = get_jwt_identity()
    sql = "Select cust_cust_type from sjd_customer where cust_customer_id=%s"
    db.cursor.execute(sql, (cust_id,))
    res = db.cursor.fetchone()
    query_result = None
    if res['cust_cust_type'] == 'I':
        sql = "select * from sjd_customer join sjd_ind_customer using (cust_customer_id) where cust_customer_id=%s"
        db.cursor.execute(sql, (cust_id,))
        query_result = db.cursor.fetchall()
    if res['cust_cust_type'] == 'C':
        sql = "select * from sjd_customer join sjd_corp_customer using (cust_customer_id) where cust_customer_id=%s"
        db.cursor.execute(sql, (cust_id,))
        query_result = db.cursor.fetchall()
    db.conn.commit()
    db.close()
    return jsonify(query_result)


'''
    Fetch customer's coupons
    <where customer_id = ... --mandatory>
    If fetch error then return None
'''
@app.route('/Api/FetchCoupon')
@jwt_required()
def fetch_coupon():
    # Check if this customer is a corporate customer
    # If no then cannot fetch coupon information
    db = SQLManager()
    db.connection()
    cust_id = get_jwt_identity()
    sql = "select cust_cust_type from SJD_CUSTOMER where cust_customer_id = %s"
    db.cursor.execute(sql, (cust_id,))
    res = db.cursor.fetchone()

    if res['cust_cust_type'] == 'C':
        sql = "select coupon_id from SJD_CORP_CUSTOMER where cust_customer_id = %s"
        db.cursor.execute(sql, (cust_id,))
        res = db.cursor.fetchone()
        sql = "select * from SJD_CORP_COUPON join SJD_COUPON using (coupon_id) where coupon_id = %s"
        db.cursor.execute(sql, (str(res['coupon_id']),))
        query_result = db.cursor.fetchall()
        db.conn.commit()
        db.close()
        return jsonify(query_result)
    else:
        db.conn.commit()
        db.close()
        return None


'''
    Fetch all invoices of customer
    <where invoice_id = ... --mandatory>
'''
@app.route('/Api/FetchInvoice')
@jwt_required()
def fetch_invoice():
    db = SQLManager()
    db.connection()
    cust_id = get_jwt_identity()

    sql = "select order_id from SJD_ORDER where cust_customer_id = %s"
    db.cursor.execute(sql, (cust_id,))
    orders = db.cursor.fetchall()
    invoices = []
    for i, row in enumerate(orders):
        cur_order_id = row['order_id']
        sql = "select * from SJD_INVOICE where order_id = %s"
        db.cursor.execute(sql, (cur_order_id,))
        invoice = db.cursor.fetchone()
        invoices.append(invoice)
    if len(invoices) == 0:
        db.commit()
        db.close()
        return None
    db.commit()
    db.close()
    return jsonify(invoices)


'''
    Fetch all payment history of customer
    <where payment_id = ... --mandatory>
'''
@app.route('/Api/FetchPayment')
@jwt_required()
def fetch_payment():
    db = SQLManager()
    db.connection()

    cust_id = get_jwt_identity()
    sql = "select order_id from SJD_ORDER where cust_customer_id = %s"
    db.cursor.execute(sql, (cust_id,))
    orders = db.cursor.fetchall()

    payments = []
    for i, row in enumerate(orders):
        cur_order_id = row['order_id']
        sql = "select * from SJD_INVOICE where order_id = %s"
        db.cursor.execute(sql, (str(cur_order_id),))
        invoice = db.cursor.fetchone()
        sql = "select * from SJD_PAYMENT where invoice_id = %s"
        db.cursor.execute(sql, (str(invoice['invoice_id']),))
        cur_payments = db.cursor.fetchall()
        for p in cur_payments:
            payments.append(p)
    if len(payments) == 0:
        db.commit()
        db.close()
        return None
    db.commit()
    db.close()
    return jsonify(payments)


'''
    Fetch customer's order history
    <where customer_id = ... --mandatory>
'''
@app.route('/Api/FetchOrder')
@jwt_required()
def fetch_order():
    db = SQLManager()
    db.connection()
    cust_id = get_jwt_identity()
    sql = "select * from SJD_ORDER where cust_customer_id = %s"
    db.cursor.execute(sql, (cust_id,))
    orders = db.cursor.fetchall()
    db.close()
    return jsonify(orders)


###################### -- CUSTOMER UPDATE THEIR PERSONAL INFORMATION -- ######################
'''
    Update customer's personal information
    This is update customer/ind_customer/corp_customer set ... <where customer_id = ... --mandatory>
'''
@app.route('/Api/UpdateCustomer', methods=['POST'])
@jwt_required()
def personal_cust_update():
    update_json = request.get_json()
    db = SQLManager()
    db.connection()

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

    con_id = get_jwt_identity()
    if len(con_id) == 0:
        # Fail, because this customer doesn't input customer_id
        db.commit()
        db.close()
        message = {"Status": "400",
                   "message": "Please provide your customer ID"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp
    where = "cust_customer_id = " + con_id

    # This means that a customer want to update an attribute in SJD_CUSTOMER
    if len(set) != 0:
        try:
            db.update_row("SJD_CUSTOMER", set, where)
        except Exception as ex:
            print(ex)
            db.conn.rollback()
            db.close()
            message = {"Status": "400", "message": "Bad Data Update"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp

        db.commit()
        db.close()
        message = {"Status": "200", "message": "Successfully Updated"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp

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
            try:
                db.update_row("SJD_IND_CUSTOMER", set, where)
            except Exception as ex:
                print(ex)
                db.conn.rollback()
                db.close()
                message = {"Status": "400", "message": "Bad Data Update"}
                resp = jsonify(message)
                resp.status_code = 400
                return resp
            db.commit()
            db.close()
            message = {"Status": "200", "message": "Successfully Updated"}
            resp = jsonify(message)
            resp.status_code = 200
            return resp

    elif res['cust_cust_type'] == 'C':
        new_corp_name = update_json['corp_name']
        new_regi = update_json['regi_num']
        new_emp_id = update_json['emp_id']
        if len(new_corp_name) != 0:
            new_corp_name = "'" + new_corp_name + "'"
            res = db.get_one("SJD_CORP_COUPON", "*",
                             "company_name = "+new_corp_name)
            if res != None:
                new_coupon = res['coupon_id']
                try:
                    db.update_row("SJD_CORP_CUSTOMER",
                                  "coupon_id = "+str(new_coupon), where)
                except Exception as ex:
                    print(ex)
                    db.conn.rollback()
                    db.close()
                    message = {"Status": "400", "message": "Bad Data Update"}
                    resp = jsonify(message)
                    resp.status_code = 400
                    return resp
                set = "corp_name=" + new_corp_name
            else:
                # Updated corporate name doesn't exist in database
                db.commit()
                db.close()
                message = {"Status": "400",
                           "message": "Corporate name doesn't exist"}
                resp = jsonify(message)
                resp.status_code = 400
                return resp
        elif len(new_regi) != 0:
            new_regi = "'" + new_regi + "'"
            set = "regi_num=" + new_regi
        elif len(new_emp_id) != 0:
            new_emp_id = "'" + new_emp_id + "'"
            set = "emp_id=" + new_emp_id
        # This means that a corporate customer want to update an attribute in SJD_CORP_CUSTOMER
        if len(set) != 0:
            try:
                db.update_row("SJD_CORP_CUSTOMER", set, where)
            except Exception as ex:
                print(ex)
                db.conn.rollback()
                db.close()
                message = {"Status": "400", "message": "Bad Data Update"}
                resp = jsonify(message)
                resp.status_code = 400
                return resp
            db.commit()
            db.close()
            message = {"Status": "200", "message": "Successfully Updated"}
            resp = jsonify(message)
            resp.status_code = 200
            return resp
    # This means that a corporate customer want to update an attribute in SJD_IND_CUSTOMER or an individual customer want to update an attribute in SJD_CORP_CUSTOMER
    db.commit()
    db.close()
    message = {"Status": "400",
               "message": "Updated Error: Incorrect customer type"}
    resp = jsonify(message)
    resp.status_code = 400
    return resp
