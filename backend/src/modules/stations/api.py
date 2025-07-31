from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend # Importar DjangoFilterBackend
from .models import Station
from .serializers import StationSerializer
from django_app.pagination import CustomPagination
from .filters import StationFilter # Importar StationFilter

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend] # Adicionar backend de filtro
    filterset_class = StationFilter # Adicionar classe de filtro