from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import FlatViewSet, ResidentListViewSet, PaymentAPIView, BillMatchAPI, InvoiceAPIView

router = SimpleRouter()
router.register('residents', ResidentListViewSet, basename='residents')
router.register('flats', FlatViewSet, basename='flats')
urlpatterns = [
    path('invoices/', InvoiceAPIView.as_view()),
    path('payments/', PaymentAPIView.as_view()),
    path('match-bills/', BillMatchAPI.as_view()),
] + router.urls

