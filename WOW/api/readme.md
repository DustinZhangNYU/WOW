## To Install Packages:
```bash
cd api
pip install -r pip install -r requirements.txt
```
## To run the demo:
```bash
export FLASK_APP=config.py
export FLASK_DEBUG=1
flask run
```
## Test json:
# Login Test
POST http://127.0.0.1:5000/login
```json
{"email":"dustinzhangzzz@gmail.com","password":"zxxzjs2012!"}
```
# Register Test
POST http://127.0.0.1:5000/register
```json
{
    "Email": "dustinzhangzzz@gmail.com",
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
    "Zipcode": 11201
}```
