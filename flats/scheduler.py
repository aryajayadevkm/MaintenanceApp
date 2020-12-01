from apscheduler.schedulers.background import BackgroundScheduler
from .models import Flat, Invoice
from datetime import datetime, timedelta
from django.db import connection


def db_table_exists(table):
    return True if table in connection.introspection.table_names() else False


def create_blank_records():
    today = datetime.today()
    yesterday = today - timedelta(days=3)
    if yesterday.month < today.month:
        flats = Flat.objects.all()
        for flat in flats:
            Invoice.objects.get_or_create(flat=flat, due_date=today, tr_type="bill", amount=(-flat.maintenance_charge)
                                          , applied=0, balance=(-flat.maintenance_charge))


def start():
    scheduler = BackgroundScheduler()
    print("scheduler starting")

    if db_table_exists('Flat') and Flat.objects.first() is not None:
        print("into flats")
        scheduler.add_job(create_blank_records, 'interval', days=1)
        scheduler.start()
