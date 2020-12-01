from .models import Invoice
from django.db.models import F


def match(payments, bills):
    i, j = 0, 0
    np, nb = len(payments), len(bills)
    while i < np and j < nb:
        balance = payments[i].balance + bills[j].balance
        (payments[i].balance, bills[j].balance) = (balance, 0) if balance >= 0 else (0, balance)
        bills[j].applied = bills[j].balance - bills[j].amount
        payments[i].applied = payments[i].balance - payments[i].amount
        bills[j].save(), payments[i].save()
        if balance >= 0:
            j += 1
        else:
            i += 1
    return [payments, bills]


def match_bulk(flat):
    payments = Invoice.objects.filter(flat=flat, tr_type="payment", balance__gt=0)
    bills = Invoice.objects.filter(flat=flat, tr_type="bill", balance__lt=0)
    match(payments, bills)


def unmatch_bulk(flat):
    Invoice.objects.filter(flat=flat).update(balance=F('amount'), applied=0)