from rest_framework import serializers
from .models import Station, StationStatus
from modules.places.serializers import PlaceSerializer
from modules.records.serializers import RecordsSerializer # Importar RecordsSerializer
from modules.sensors.serializers import SensorSerializer # Importar SensorSerializer

class StationInfoSerializer(serializers.Serializer):
    model = serializers.CharField(max_length=255)
    firmware = serializers.CharField(max_length=255, allow_null=True)
    installed_at = serializers.DateTimeField(allow_null=True)

class StationSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)
    info = StationInfoSerializer(source='*', read_only=True) # Mapeia campos do modelo para o serializer aninhado
    
    # Adicionar campos para sensors e records
    sensors = serializers.SerializerMethodField()
    records = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = (
            'id',
            'uuid',
            'name',
            'description',
            'status',
            'info',
            'place',
            'sensors',
            'records',
            'created_at',
            'updated_at',
        )

    def get_sensors(self, obj):
        # Retorna os sensores relacionados à estação
        return SensorSerializer(obj.sensors.all(), many=True).data

    def get_records(self, obj):
        # Retorna os 5 registros mais recentes relacionados à estação
        return RecordsSerializer(obj.records.order_by('-timestamp')[:5], many=True).data