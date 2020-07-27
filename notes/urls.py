from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import FlatViewSet

router = SimpleRouter()
router.register('notes', FlatViewSet)
urlpatterns = router.urls
