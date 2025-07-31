import django_filters
from .models import Station

class StationFilter(django_filters.FilterSet):
    class Meta:
        model = Station
        fields = {
            'name': ['exact', 'icontains'],
            'uuid': ['exact'],
            'status': ['exact'],
            'model': ['exact', 'icontains'],
            'firmware': ['exact', 'icontains'],
            'place__name': ['exact', 'icontains'], # Filtrar por nome do local
        }
