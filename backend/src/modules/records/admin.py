from django.contrib import admin
from .models import Records

@admin.register(Records)
class RecordsAdmin(admin.ModelAdmin):
    list_display = ('station', 'timestamp', 'status', 'sensors', 'created_at', 'updated_at')
    list_filter = ('station', 'status', 'timestamp')
    search_fields = ('station__uuid', 'station__name') # Assuming Station has uuid and name
    raw_id_fields = ('station',) # Useful for ForeignKey fields

    list_per_page = 25
