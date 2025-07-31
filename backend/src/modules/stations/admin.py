from django.contrib import admin
from .models import Station, StationStatus
from modules.places.models import Place 

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid', 'place', 'status', 'model', 'firmware', 'installed_at', 'created_at', 'updated_at')
    list_filter = ('status', 'place', 'installed_at', 'created_at')
    search_fields = ('name', 'uuid', 'model', 'firmware')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    raw_id_fields = ('place',)

    list_per_page = 25
