from rest_framework.routers import DefaultRouter
from .api import RecordsViewSet

router = DefaultRouter()
router.register(r'', RecordsViewSet, basename='records')

urlpatterns = router.urls
