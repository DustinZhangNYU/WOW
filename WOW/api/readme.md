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
  "firstName": "Dustin",
  "lastName": "Zhang",
  "mobile_phone": 6125320597,
  "driver_license_number": "NB12550",
  "street": "Gold St",
  "apt": "608",
  "city": "Brooklyn",
  "state": "NY",
  "country": "USA",
  "middleName": null,
  "ins_company_name": "AAA",
  "ins_pol_num": 12345,
  "zipcode": 11201,
  "cust_type": "C",
  "corp_name": "Google",
  "regi_num": "G1K56324",
  "emp_id": "G112233"
}
```

## Search-car Test

POST http://127.0.0.1:5000/search-cars

```json
{ "class_name": "SUV", "State": "FL" }
```
