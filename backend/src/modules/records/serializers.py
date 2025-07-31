from rest_framework import serializers
from .models import Records

class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = (
            'id',
            'uuid',
            'sensors',
            'created_at',
            'updated_at',
        )