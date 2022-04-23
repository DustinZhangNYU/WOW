'''
 <WOW Back-end Version 2.0,  Add interaction with front-end, No concurrent and attack injection>
 <04/21/2022> api.py
    WOW system APIs in app.py
'''

# Basic logic to using the website
# Customer: register -> log in -> search for cars -> look up information on certain car
# -> continue on submitting the order with payment info etc, then submit order
# -> order completed, congratulations page
# - Siya Guo, 04/22

# separated the api documentation

from config import *

'''
    WOW employee or customer fetch all vehicle class information
    This is select * from SJD_VEH_CLASS
'''

@app.route('search-cars')
# when searching for cars, asking the customer to input what kind of vehicles he/she is looking for - Siya Guo, 04/22
# @app.route('/Api/GetVehicleClassList')
def vehicle_class_fetchall():
    query_result = db.get_list('SJD_VEH_CLASS', '*')
    return jsonify(query_result)


'''
    WOW employee or customer fetch all vehicle information
    This is select * from SJD_VEHICLES
'''
@app.route('search-cars')
# when searching for cars, asking the customer to input what kind of vehicles he/she is looking for - Siya Guo, 04/22
# @app.route('/Api/GetVehiclesList')
def vehicle_fetchall():
    query_result = db.get_list('SJD_VEHICLES', '*')
    return jsonify(query_result)


'''
    WOW employee or customer fetch all office information
    This is select * from SJD_OFFICE
'''

@app.route('search-cars')
# choose pickup and drop-off office locations on the search page - Siya Guo, 04/22
# @app.route('/Api/GetOfficeList')
def office_fetchall():
    query_result = db.get_list('SJD_OFFICE', '*')
    return jsonify(query_result)

