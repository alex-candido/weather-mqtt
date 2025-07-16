from django.contrib import admin
from .models import Station, SensorData

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('station_id', 'city', 'latitude', 'longitude', 'created_at', 'updated_at')
    search_fields = ('station_id', 'city')
    list_filter = ('city',)

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('station', 'sensor_name', 'sensor_type', 'value', 'unit', 'timestamp')
    list_filter = ('station', 'sensor_type', 'unit')
    search_fields = ('station__station_id', 'sensor_name', 'sensor_type')
    date_hierarchy = 'timestamp'
