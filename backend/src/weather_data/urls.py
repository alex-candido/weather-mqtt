from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationViewSet, SensorDataViewSet

router = DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'sensor_data', SensorDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
