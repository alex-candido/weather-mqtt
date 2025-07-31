import django_filters
from .models import Place

class PlaceFilter(django_filters.FilterSet):
    class Meta:
        model = Place
        fields = {
            'name': ['exact', 'icontains'],
            'uuid': ['exact'],
            'status': ['exact'],
            'city': ['exact', 'icontains'],
            'state': ['exact', 'icontains'],
            'country': ['exact', 'icontains'],
        }
