from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sensor
from .serializers import SensorSerializer
from django_app.pagination import CustomPagination
from .filters import SensorFilter

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = SensorFilter
