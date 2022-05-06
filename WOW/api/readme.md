# To Install Packages:

```bash
cd api
pip install -r requirements.txt
```

# To run the demo:

```bash
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run
```

# Test with postman:

## Login Test

POST http://127.0.0.1:5000/login

```json
{ "email": "dustinzhangzzz@gmail.com", "password": "zxxzjs2012!" }
```

## Register Test

POST http://127.0.0.1:5000/register

```json
{
  "email": "zxxcccc@yahoo.com",
  "password": "zxxzjs2012!",
  "first_name": "Dustin",
  "last_name": "Zhang",
  "phone": 6125320597,
  "dri_lic_num": "NB12550",
  "add_street": "Gold St",
  "add_unit": "608",
  "add_city": "Brooklyn",
  "add_state": "NY",
  "add_country": "USA",
  "middle_name": null,
  "ins_com_name": "AAA",
  "ins_pol_num": 12345,
  "add_zipcode": 11201,
  "cust_type": "C",
  "corp_name": "Google",
  "regi_num": "G1K56324",
  "emp_id": "G112233"
}
```

## Search-car Test

POST http://127.0.0.1:5000/search-cars

```json
{ "class_name": "SUV", "add_state": "FL" }
```

```json
{ "class_name": "Luxury Car", "add_state": "NY" }
```

## Delete Customer Test

DELETE http://127.0.0.1:5000/DeleteCustomer

```json
{ "cust_customer_id": 35 }
```
