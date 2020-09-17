from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import FlatViewSet, ResidentListViewSet, MonthlyCollectionListCreateView

router = SimpleRouter()
router.register('collections', MonthlyCollectionListCreateView, basename='collections')
router.register('residents', ResidentListViewSet, basename='residents')
router.register('flats', FlatViewSet, basename='flats')
urlpatterns = [
    # path('flats/', FlatListViewSet.as_view()),
] + router.urls

