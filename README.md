# MaintenanceApp
Maintenance App backend.
This is flat-admin-only use. No permissions set.

<br />
## APIs:
1. api/users/ - register flat admin
1. api/flats/ - add and retrive flats
2. api/residents/ - add and retrieve residents
3. api/invoices/ - Fetches list of flats, their maintenance charge and amount paid for that month (creates empty records for every new month)
4. api/payments/ - Get flat-wise dues Post payment
5. api/match-bills/ - Match bills

<br />
## Instructions:
1. pip install -r requirement.txt
2. python manage.py createsuperuser
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py createsuperuser
6. Go to django-admin interface and add a building
<br />

1. Try the dummy data to register at **api/users/** end point on postman:
<br />
```
{
    "user":{
        "username":"yourname",
        "email":"yourname@gmail.com", 
        "password": "yourname1234"
    }
}
```
<br />
2. To login at **api/users/login/** end point on postman:
<br />
{
    "user":{
        "email":"yourname@gmail.com", 
        "password": "yourname1234"
    }
}

<br />
3. To add residents with POST request at **api/residents/** end point on postman:
<br />
```
{
   "name":"resident",
   "mobile_no": "9876543210",
   "email": "resident@gmail.com"
}
```
<br />
GET request at the same endpoint gives list of all residents, and PATCH request at api/residents/1/ lets you update details of resident whose id is 1.
<br />
<br />
4. To add flats at **api/flats/** end point on postman:
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

### Check out some features
This app lets you schedule bill generation and keeps record of all bills and payments,
<br />
1. Generate bills automatically/manually
2. Show overdues
3. Record monthly/advance payment 
4. Match bills and payments
5. Manage fine

To try these, add some flats (maintenance charge should not be left blank). Now go to **api/collections/** end point and make a get request. You'll find the dues and the months overdue. (Note: Flat upon registration sets maintenance charge due for that month and payment records get appended automatically every month.
<br />
make a PATCH request at **api/collections/1/** with dummy data (here 1 is flat id):
<br />
{
    "amount_paid": "1500",
    "months": [
        "2020-09-17"
    ]
}
If there's any extra amount it can be applied to bills any time. If amount paid is insufficient, bills are partially filled and dues get updated accordingly. 








