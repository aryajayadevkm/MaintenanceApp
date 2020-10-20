from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import FlatViewSet, ResidentListViewSet, CollectionAPIView, BillsAPIView

router = SimpleRouter()
router.register('residents', ResidentListViewSet, basename='residents')
router.register('flats', FlatViewSet, basename='flats')
urlpatterns = [
    path('collections/', CollectionAPIView.as_view()),
    path('bills/', BillsAPIView.as_view()),
] + router.urls

