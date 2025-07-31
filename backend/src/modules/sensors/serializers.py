from rest_framework import serializers
from .models import Sensor, SensorStatus, SensorType, UnitType

class SensorInfoSerializer(serializers.Serializer):
    min_value = serializers.FloatField()
    max_value = serializers.FloatField()

class SensorSerializer(serializers.ModelSerializer):
    info = SensorInfoSerializer(source='*', read_only=True) # Mapeia campos do modelo para o serializer aninhado

    class Meta:
        model = Sensor
        fields = (
            'id',
            'uuid',
            'name',
            'description',
            'status',
            'info',
            'type',
            'unit',
            'created_at',
            'updated_at',
        )