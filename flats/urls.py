from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import FlatListViewSet, ResidentListViewSet, MonthlyCollectionViewSet, MonthlyCollectionListCreateView

router = SimpleRouter()
router.register('monthly-collection', MonthlyCollectionListCreateView, basename='monthly-collection')

urlpatterns = [
    path('flats/', FlatListViewSet.as_view()),
    path('residents/', ResidentListViewSet.as_view()),
    path('collections/', MonthlyCollectionViewSet.as_view()),
] + router.urls

