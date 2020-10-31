from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import FlatViewSet, ResidentListViewSet, BillAPIView, PaymentAPIView

router = SimpleRouter()
router.register('residents', ResidentListViewSet, basename='residents')
router.register('flats', FlatViewSet, basename='flats')
urlpatterns = [
    path('bills/', BillAPIView.as_view()),
    path('payments/', PaymentAPIView.as_view()),
] + router.urls

