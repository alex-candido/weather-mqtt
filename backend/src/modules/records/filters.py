import django_filters
from .models import Records

class RecordsFilter(django_filters.FilterSet):
    class Meta:
        model = Records
        fields = {
            'uuid': ['exact'],
            'timestamp': ['exact', 'gte', 'lte'], # Filtrar por data e hora
            'station__uuid': ['exact'], # Filtrar por UUID da estação
            'station__name': ['exact', 'icontains'], # Filtrar por nome da estação
        }
