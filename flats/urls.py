from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import FlatListViewSet, ResidentListViewSet, MonthlyCollectionViewSet


urlpatterns = [
    path('flats/', FlatListViewSet.as_view()),
    path('residents/', ResidentListViewSet.as_view()),
    path('collections/', MonthlyCollectionViewSet.as_view())
]