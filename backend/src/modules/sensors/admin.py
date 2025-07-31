from django.contrib import admin
from .models import Sensor, SensorStatus, SensorType, UnitType

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'unit', 'status', 'min_value', 'max_value', 'created_at', 'updated_at')
    list_filter = ('type', 'unit', 'status', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('uuid', 'created_at', 'updated_at')

    list_per_page = 25

