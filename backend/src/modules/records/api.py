from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Records
from .serializers import RecordsSerializer
from django_app.pagination import CustomPagination
from .filters import RecordsFilter

class RecordsViewSet(viewsets.ModelViewSet):
    queryset = Records.objects.all()
    serializer_class = RecordsSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecordsFilter

    @action(detail=False, methods=['get'])
    def latest(self, request):
        station_uuid = request.query_params.get('station_uuid')
        queryset = self.get_queryset()

        if station_uuid:
            queryset = queryset.filter(station__uuid=station_uuid)

        latest_record = queryset.order_by('-created_at').first()
        if latest_record:
            serializer = self.get_serializer(latest_record)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
