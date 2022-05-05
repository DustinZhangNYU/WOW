'''
 <WOW Database configuration Version 2.0>
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
        # self.conn = pymysql.connect(host = DB_CONFIG['host'],port = DB_CONFIG['port'],user = DB_CONFIG['user'],db = DB_CONFIG['db'],charset = DB_CONFIG['charset'])
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
        self.conn.commit()

    # Insert record into table and auto commit, also fetch the primary key value of current last row
    # Cursor.insert_id() can fetch current inserted row's id value
    def insert_row(self, table_name, col_value, args=None):
        sql = "Insert into " + table_name + " values (" + col_value + ");"
        self.cursor.execute(sql, args)
        last_id = self.cursor.lastrowid
        return last_id

    # Delete record from table and auto commit, also fetch the primary key value of current last row
    def delete_row(self, table_name, where=None, args=None):
        if where != None and len(where) != 0:
            sql = "Delete from " + table_name + " where " + where + ";"
        else:
            sql = "Delete from " + table_name + ";"
        self.cursor.execute(sql, args)
        last_id = self.cursor.lastrowid
        return last_id

    # Execute any kind of sql line such as JOIN ...
    def get_sql_res(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    # Close MySQL connection
    def close(self):
        if self.cursor != None:
            self.cursor.close()
        if self.conn != None:
            pool.release(self.conn)


app = Flask(__name__)
db = SQLManager()
db.connection()
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
# Tables last id (used in concurrent)

# Add a connection pool (used in concurrent)


@app.route('/login', methods=["POST"])
def login():
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
        return resp
    cust_id = query_result["cust_customer_id"]
    if verifyPassword(query_result["cust_hash_password"], password) == False:
        message = {"Status": "400", "message": "Password is incorrect"}
        resp = jsonify(message)
        resp.status_code = 400
        print("Password is incorrect")
        return resp
    else:
        access_token = create_access_token(identity=cust_id, fresh=True)
        message = {"Status": "200", "message": "Successfully Login!",
                   "access_token": access_token}
        resp = jsonify(message)
        resp.status_code = 200
        print("Successfully Login!")
        return resp


def verifyPassword(hashedPassword, password):
    return bcrypt.checkpw(password.encode(), hashedPassword.encode())


@app.route('/register', methods=["POST"])
def register():
    request_data = request.get_json()
    email = request_data['Email']
    first_name = request_data['FirstName']
    last_name = request_data["LastName"]
    password = request_data["Password"]
    mobile_phone = request_data["Mobile Phone"]
    dln = request_data["Driver License Number"]  # Driver license number
    street = request_data["Street"]
    unit = request_data["Apt/Unit"]
    city = request_data["City"]
    state = request_data["State"]
    country = request_data["Country"]
    zipcode = request_data["Zipcode"]
    ins_company_name = request_data["Ins_company_name"]
    ins_pol_num = request_data["Ins_pol_num"]
    middle_name = request_data["MiddleName"]
    cust_type = request_data["Cust_type"]
    sql = 'select cust_hash_password from sjd_customer where cust_email_address = %s'
    hashpassword = generateSaltPassword(password)
    query = db.cursor.execute(sql, (email,))
    query_result = db.cursor.fetchone()
    if query_result != None:
        message = {"Status": "400", "message": "Email is Used"}
        resp = jsonify(message)
        resp.status_code = 400
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
            return resp
        db.conn.commit()
        sql = "select cust_customer_id from sjd_customer where cust_email_address=%s"
        query = db.cursor.execute(sql, (email,))
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
                return resp
            db.conn.commit()
        elif (cust_type == "C"):
            corp_name = request_data["Corp_name"]
            regi_num = request_data["Regi_num"]
            emp_id = request_data["Emp_id"]
            sql = "Insert INTO sjd_corp_customer (cust_customer_id,\
                corp_name,\
                regi_num,\
                emp_id)\
                VALUES(%s,%s,%s,%s)"
            parameters = (cust_id, corp_name, regi_num, emp_id)
            try:
                db.cursor.execute(sql, parameters)
            except Exception as ex:
                print(ex)
                message = {"Status": "400", "message": "Bad Data Insertion"}
                resp = jsonify(message)
                resp.status_code = 400
                return resp
            db.conn.commit()
        message = {"Status": "200", "message": "Successfully Registered"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp


def generateSaltPassword(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


@app.route('/review', methods=['POST'])
@jwt_required()
def pickup():
    data = request.get_json()
    vin_val = data['vin']
    cust_id = get_jwt_identity()
    select_col = "available, office_id"
    sql = "select available, office_id from sjd_vehicles where vin=%s"
    query = db.cursor.execute(sql, (vin_val,))
    query_result = db.cursor.fetchone()
    if query_result != None and query_result['available'] == 'Y':
        # This car is available now
        sql = "Update sjd_vehicles set available = 'N' where vin=%s"
        try:
            db.cursor.execute(sql, (vin_val,))
        except Exception as ex:
            print(ex)
            db.conn.rollback()
            message = {"Status": "400", "message": "Bad Data Updating"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
        pickup_office = query_result['office_id']
        pickup_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Default start_odometers are zero
        start_odometer = 0

        daily_odometer_limit = 500

        # 用一张另外的 SJD_NOT_FINISHED_ORDER 表先暂时几下谁在哪里什么时候租了哪台车，这台车此时的start_odometers和这个待完成订单的daily_odometer_limit值
        sql = "Insert INTO sjd_not_finished_order (cust_customer_id,\
            pickup_office_id,\
            pickup_date,\
            vin,\
            start_odometer,\
            daily_odometer_limit)\
            VALUES (%s,%s,%s,%s,%s,%s)"
        try:
            print(vin_val)
            db.cursor.execute(sql, (cust_id, str(pickup_office), str(
                pickup_date), vin_val, str(start_odometer), daily_odometer_limit))
        except Exception as ex:
            print(ex)
            db.conn.rollback()
            message = {"Status": "400", "message": "Bad Data Insertion"}
            resp = jsonify(message)
            resp.status_code = 400
            return resp
        db.conn.commit()
        message = {"Status": "200", "message": "Successfully Booked"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    else:
        message = {"Status": "400",
                   "message": "Car doesn't exist or already booked"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp


@app.route("/user-profile")
@jwt_required()
def fetch_customer():
    data = request.get_json()
    cust_id = get_jwt_identity()
    sql = "Select cust_cust_type from sjd_customer where cust_customer_id=%s"
    db.cursor.execute(sql, cust_id)
    res = db.cursor.fetchone()
    query_result = None
    if res['cust_cust_type'] == 'I':
        sql = "select * from sjd_customer join sjd_ind_customer using (cust_customer_id) where cust_customer_id=%s"
        db.cursor.execute(sql, cust_id)
        query_result = db.cursor.fetchall()
    if res['cust_cust_type'] == 'C':
        sql = "select * from sjd_customer join sjd_corp_customer using (cust_customer_id) where cust_customer_id=%s"
        db.cursor.execute(sql, cust_id)
        query_result = db.cursor.fetchall()
    return jsonify(query_result)


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.route('/search-cars', methods=['POST'])
def searchCar():
    from decimal import Decimal

    class DecimalEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return str(obj)
            return json.JSONEncoder.default(self, obj)
    data = request.get_json()
    className = data["class_name"]
    location = data["State"]
    sql = "SELECT over_milage_fee,rental_rate,make,model,year from sjd_veh_class join sjd_vehicles using (class_id) join sjd_office using (office_id) where class_name =%s and add_state=%s and available='Y'"
    db.cursor.execute(sql, (className, location))
    result = db.cursor.fetchall()
    print(result)
    return json.dumps(result, cls=DecimalEncoder)


@app.route('/Api/Dropoff', methods=['POST'])
@jwt_required()
def dropoff():
    data = request.get_json()
    cust_id = get_jwt_identity()
    sql = "Select vin from SJD_NOT_FINISHED_ORDER where cust_customer_id=%s"
    try:
        db.cursor.execute(sql, (cust_id,))
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        message = {"Status": "400", "message": "Cannot fetch the data"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp
    vin_val = db.cursor.fetchone()
    cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
    sql = "Update SJD_VEHICLES set available='Y' where vin=%s"

    try:
        db.cursor.execute(sql, (vin_val,))
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        message = {"Status": "400", "message": "Bad Data Updating"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp
    dropoff_office = data['dropoff_office_id']
    sql = "Update SJD_VEHICLES set dropoff_office=%s where vin=%s"
    try:
        db.cursor.execute(sql, (vin_val, vin_val))
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        message = {"Status": "400", "message": "Bad Data Updating"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp

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
    use_coupon = data['coupon_id']
    if len(use_coupon) != 0 and check_cust_type == True:
        # Individual customer choose to use a coupon
        sql = "Select coupon_type from SJD_COUPON where coupon_id=%s"
        db.cursor.execute(sql, (use_coupon,))
        ctype = db.cursor.fetchone()
        if ctype['coupon_type'] == 'I':
            # This is an individual coupon
            sql = "Select expiration_date,start_date from SJD_IND_COUPON where coupon_id=%s"
            db.cursor.execute(sql, (use_coupon))
            res = db.cursor.fetchone()
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
    sql = "Select * from SJD_NOT_FINISHED_ORDER where cust_customer_id = %s and vin = %s"
    db.cursor.execute(sql, (cust_id, vin_val))
    res = db.cursor.fetchone()
    db.insert_row("SJD_ORDER", col_val)
    sql = "Insert INTO sjd_not_finished_order (pickup_date,\
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
        print(vin_val)
        db.cursor.execute(sql, (str(res['pickup_date']), str(res['pickup_office_id']),
                                str(cur_date), str(res['start_odometer']), end_odometer, str(
                                    res['daily_odometer_limit']), vin_val,
                                dropoff_office, str(use_corp_coupon), use_coupon, cust_id))
    except Exception as ex:
        print(ex)
        db.conn.rollback()
        message = {"Status": "400", "message": "Bad Data Insertion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp
    sql = "select count(*) from SJD_PAYMENT"
    query_result = db.get_sql_res(sql)
    pay_id = query_result[0]['count(*)'] + 1
    pay_method = data['payment_method']
    card_no = data['card_number']
    sql = "Select invoice_id from SJD_NOT_FINISHED_ORDER where cust_customer_id = %s and vin = %s"
    db.cursor.execute(sql, (cust_id, vin_val))
    res = db.cursor.fetchone()
    res = db.get_one("SJD_INVOICE", "invoice_id",
                     "order_id = " + str(order_id))
    col_data = [str(pay_id), "'" + str(cur_date) + "'",
                pay_method, card_no, str(res['invoice_id'])]
    col_val = ','.join(col_data)
    last_id = db.insert_row("SJD_PAYMENT", col_val)
    last_id = db.delete_row("SJD_NOT_FINISHED_ORDER",
                            "cust_customer_id = " + cust_id + " and vin = " + vin_val)
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run()
