from apscheduler.schedulers.background import BackgroundScheduler
from .models import Flat, PaymentHistory, Bill
from datetime import datetime, timedelta
from django.db import connection


def db_table_exists(table):
    return True if table in connection.introspection.table_names() else False


def create_blank_records():
    today = datetime.today()
    yesterday = today - timedelta(days=3)
    print("#", PaymentHistory.objects.first())
    if yesterday.month < today.month:
        flats = Flat.objects.all()
        for flat in flats:
            PaymentHistory.objects.get_or_create(flat=flat, due_date=today.date())
            Bill.objects.get_or_create(flat=flat, tr_type="bill", amount=(-flat.maintenance_charge)
                                       , applied=0, balance=(-flat.maintenance_charge))



def test():
    print("#testing")


def start():
    scheduler = BackgroundScheduler()
    print("#1")

    if db_table_exists('Flat') and Flat.objects.first() is not None:
        print("#in it!")
        scheduler.add_job(create_blank_records, 'interval', days=1)
        scheduler.start()
