# MaintenanceApp
Restarted Maintenance App(only backend at present).
This is flat-admin-only use. No permissions set.
<br />
## Api end-points:
1. api/users/ - register flat admin
1. api/flats/ - add and retrive flats
2. api/residents/ - add and retrieve residents
3. api/collections/ - Fetches list of flats, their maintenance charge and amount paid for that month (creates empty records for every new month)

## Instructions:
1. pip install -r requirement.txt
2. python manage.py createsuperuser
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py createsuperuser
6. Go to django-admin interface and add a building

Try the dummy data to register at api/users/ end point on postman:
<br />
{
    "user":{
        "username":"yourname",
        "email":"yourname@gmail.com", 
        "password": "yourname1234"
    }
}

To login at api/users/login/ end point on postman:
<br />
{
    "user":{
        "email":"yourname@gmail.com", 
        "password": "yourname1234"
    }
}

To add residents with POST request at api/residents/ end point on postman:
<br />
{
   "name":"resident",
   "mobile_no": "9876543210",
   "email": "resident@gmail.com"
}
<br />
GET request at the same endpoint gives list of all residents, and PATCH request at api/residents/1/ lets you update details of resident whose id is 1.

To add flats at api/flats/ end point on postman:
<br />
{
    "building":"1",
   "flat_no": "G3",
   "owner": "1",
   "maintenance_charge":"2500"
}
<br />
GET request at the same endpoint gives list of all flats, and PATCH request at api/flats/1/ lets you update details of flat whose id is 1.
<br />

### Testing maintenance collection
The real feature of the app is collection of maintenance charge and record keeping. This means
<br />
1. It calculates due amount
2. months which are overdue
3. Allows payment in advance
4. Stock up extra payment
5. Use the stocked up amount to pay off the dues.









