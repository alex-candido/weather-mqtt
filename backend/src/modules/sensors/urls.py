from rest_framework.routers import DefaultRouter
from .api import SensorViewSet

router = DefaultRouter()
router.register(r'', SensorViewSet, basename='sensors')

urlpatterns = router.urls
