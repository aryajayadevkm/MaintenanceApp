from apscheduler.schedulers.background import BackgroundScheduler
from .models import Flat, PaymentHistory
from datetime import datetime, timedelta


def create_blank_records():
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    print("#", PaymentHistory.objects.first())
    if yesterday.month < today.month:
        flats = Flat.objects.all()
        for flat in flats:
            PaymentHistory.objects.get_or_create(flat=flat, paid_for=today.date())
    elif PaymentHistory.objects.first() is None:
        flats = Flat.objects.all()
        for flat in flats:
            PaymentHistory.objects.create(flat=flat, paid_for=today.date())


def test():
    print("#testing")


def start():
    scheduler = BackgroundScheduler()
    scheduler.configure({'apscheduler.daemonic': False})
    print("#1")
    if Flat.objects.first() is not None:
        print("#in it!")
        scheduler.add_job(create_blank_records, 'interval', days=1)
        scheduler.start()