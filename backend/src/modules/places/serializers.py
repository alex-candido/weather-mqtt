from rest_framework import serializers
from .models import Place, PlaceStatus

class PlaceInfoSerializer(serializers.Serializer):
    address = serializers.CharField(allow_null=True, allow_blank=True)
    city = serializers.CharField(allow_null=True, allow_blank=True)
    state = serializers.CharField(allow_null=True, allow_blank=True)
    country = serializers.CharField(allow_null=True, allow_blank=True)

class GeoPointSerializer(serializers.Serializer):
    type = serializers.CharField(default="Point", read_only=True)
    coordinates = serializers.SerializerMethodField()

    def get_coordinates(self, obj):
        return [obj.longitude, obj.latitude]

class PlaceSerializer(serializers.ModelSerializer):
    info = PlaceInfoSerializer(source='*', read_only=True) # Mapeia campos do modelo para o serializer aninhado
    geometry = GeoPointSerializer(source='*', read_only=True) # Mapeia campos do modelo para o serializer aninhado

    class Meta:
        model = Place
        fields = (
            'id',
            'uuid',
            'name',
            'description',
            'info',
            'geometry',
            'status',
            'latitude',
            'longitude',
            'created_at',
            'updated_at',
        )