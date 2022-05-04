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
        self.conn.commit()
        last_id = self.cursor.lastrowid
        return last_id

    # Delete record from table and auto commit, also fetch the primary key value of current last row
    def delete_row(self, table_name, where=None, args=None):
        if where != None and len(where) != 0:
            sql = "Delete from " + table_name + " where " + where + ";"
        else:
            sql = "Delete from " + table_name + ";"
        self.cursor.execute(sql, args)
        self.conn.commit()
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
                      mobile_phone, "I", city, hashpassword)
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
        message = {"Status": "200", "message": "Successfully Registered"}
        resp = jsonify(message)
        resp.status_code = 200
        return resp


def generateSaltPassword(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


@app.route('/Pickup', methods=['POST'])
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

        daily_odometer_limit = data['daily_odometer_limit']

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
    jti = get_jwt()["jti"]
    now = datetime.datetime.now(datetime.timezone.utc)
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO sjd_jwt_revoked_token (token_val,\
        token_date) \
        VALUES (%s,%s)"
    try:
        db.cursor.execute(sql, (jti, formatted_date))
    except Exception as ex:
        print(ex)
        message = {"Status": "400", "message": "Bad Data Insertion"}
        resp = jsonify(message)
        resp.status_code = 400
        return resp
    db.conn.commit()
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
