import django_filters
from .models import Sensor

class SensorFilter(django_filters.FilterSet):
    class Meta:
        model = Sensor
        fields = {
            'name': ['exact', 'icontains'],
            'uuid': ['exact'],
            'status': ['exact'],
            'type': ['exact'],
            'unit': ['exact'],
            'min_value': ['exact', 'gte', 'lte'],
            'max_value': ['exact', 'gte', 'lte'],
        }
