from rest_framework.routers import DefaultRouter
from .api import StationViewSet

router = DefaultRouter()
router.register(r'', StationViewSet, basename='stations')

urlpatterns = router.urls
