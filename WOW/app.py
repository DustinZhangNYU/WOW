'''
 <WOW Back-end Version 1.0,  No interaction with front-end now, only database operation>
 <04/13/2022> app.py
    APIs in app.py is available to both customer and employee
'''
from config import *
from classes import *
#from flask import *
#app = Flask(__name__)
#app.config.from_object(__name__)

db = SQLManager()
db.connection()

'''
    WOW employee or customer fetch all vehicle class information
    This is select * from SJD_VEH_CLASS
'''
def vehicle_class_fetchall():
    vehicle_c = Vehicle_Classes()
    query_result = db.get_list('SJD_VEH_CLASS','*')
    for i,row, in enumerate(query_result):
        vehicle_c.class_id.append(row['class_id'])
        vehicle_c.over_milage_fee.append(row['over_milage_fee'])
        vehicle_c.rental_rate.append(row['rental_rate'])
        vehicle_c.class_name.append(row['class_name'])
    return vehicle_c

'''
    WOW employee or customer fetch all vehicle information
    This is select * from SJD_VEHICLES
'''
def vehicle_fetchall():
    vehicle = Vehicles()
    query_result = db.get_list('SJD_VEHICLES','*')
    for i,row, in enumerate(query_result):
        vehicle.make.append(row['make'])
        vehicle.model.append(row['model'])
        vehicle.year.append(row['year'])
        vehicle.vin.append(row['vin'])
        vehicle.lic_plt_num.append(row['lic_plt_num'])
        vehicle.class_id.append(row['class_id'])
        vehicle.office_id.append(row['office_id'])
    return vehicle

'''
    WOW employee or customer fetch all office information
    This is select * from SJD_OFFICE
'''
def office_fetchall():
    office = Office()
    query_result = db.get_list('SJD_OFFICE','*')
    for i,row, in enumerate(query_result):
        office.id.append(row['office_id'])
        office.country.append(row['add_country'])
        office.state.append(row['add_state'])
        office.street.append(row['add_street'])
        office.unit.append(row['add_unit'])
        office.zipcode.append(row['add_zipcode'])
        office.phone_number.append(row['phone_number'])
        office.city.append(row['add_city'])
    return office

