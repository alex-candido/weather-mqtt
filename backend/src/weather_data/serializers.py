from rest_framework import serializers
from .models import Station, SensorData

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['station_id', 'city', 'latitude', 'longitude', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['sensor_name', 'sensor_type', 'value', 'unit', 'timestamp']
        read_only_fields = ['timestamp']
