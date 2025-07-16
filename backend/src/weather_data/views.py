from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Max, OuterRef, Subquery, Avg

from .models import Station, SensorData
from .serializers import StationSerializer, SensorDataSerializer

class StationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    lookup_field = 'station_id' # Permite buscar por station_id na URL

class SensorDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

    def get_queryset(self):
        # Permite filtrar por station_id na URL, ex: /api/sensor_data/?station_id=STATION_FORTALEZA_001
        queryset = super().get_queryset()
        station_id = self.request.query_params.get('station_id', None)
        if station_id is not None:
            queryset = queryset.filter(station__station_id=station_id)
        return queryset

    @action(detail=False, methods=['get'])
    def latest(self, request):
        station_id = request.query_params.get('station_id', None)
        if not station_id:
            return Response({'detail': 'Parâmetro station_id é obrigatório.'}, status=400)

        # Obtém os IDs dos registros mais recentes para cada sensor_name
        latest_ids = SensorData.objects.filter(
            station__station_id=station_id
        ).values('sensor_name').annotate(max_timestamp=Max('timestamp'))

        # Filtra os dados do sensor para incluir apenas os com os timestamps mais recentes
        # Isso é um pouco mais complexo com distinct, então vamos iterar para garantir
        latest_sensor_data = []
        for item in latest_ids:
            latest_record = SensorData.objects.filter(
                station__station_id=station_id,
                sensor_name=item['sensor_name'],
                timestamp=item['max_timestamp']
            ).first()
            if latest_record:
                latest_sensor_data.append(latest_record)

        serializer = self.get_serializer(latest_sensor_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def record_count(self, request):
        station_id = request.query_params.get('station_id', None)
        if not station_id:
            return Response({'detail': 'Parâmetro station_id é obrigatório.'}, status=400)

        try:
            station = Station.objects.get(station_id=station_id)
            count = SensorData.objects.filter(station=station).count()
            return Response({'station_id': station_id, 'record_count': count})
        except Station.DoesNotExist:
            return Response({'detail': 'Estação não encontrada.'}, status=404)

    @action(detail=False, methods=['get'])
    def temperature_prediction(self, request):
        station_id = request.query_params.get('station_id', None)
        if not station_id:
            return Response({'detail': 'Parâmetro station_id é obrigatório.'}, status=400)

        try:
            station = Station.objects.get(station_id=station_id)
            # Pega as últimas 10 leituras de temperatura para a estação
            recent_temperatures = SensorData.objects.filter(
                station=station,
                sensor_type='temperature'
            ).order_by('-timestamp')[:10]

            if not recent_temperatures:
                return Response({'station_id': station_id, 'prediction': None, 'message': 'Dados de temperatura insuficientes para previsão.'})

            # Calcula a média
            avg_temp = sum([t.value for t in recent_temperatures]) / len(recent_temperatures)
            return Response({'station_id': station_id, 'prediction': round(avg_temp, 2), 'unit': '°C'})

        except Station.DoesNotExist:
            return Response({'detail': 'Estação não encontrada.'}, status=404)