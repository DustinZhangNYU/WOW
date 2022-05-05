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
  "Email": "zxxcccc@yahoo.com",
  "Password": "zxxzjs2012!",
  "FirstName": "Dustin",
  "LastName": "Zhang",
  "Mobile Phone": 6125320597,
  "Driver License Number": "NB12550",
  "Street": "Gold St",
  "Apt/Unit": "608",
  "City": "Brooklyn",
  "State": "NY",
  "Country": "USA",
  "MiddleName": null,
  "Ins_company_name": "AAA",
  "Ins_pol_num": 12345,
  "Zipcode": 11201,
  "Cust_type": "C",
  "Corp_name": "Google",
  "Regi_num": "G1K56324",
  "Emp_id": "G112233"
}
```

## Search-car Test

POST http://127.0.0.1:5000/search-cars

```json
{ "class_name": "SUV", "State": "FL" }
```
