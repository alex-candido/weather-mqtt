import uuid

from django.db import models

from modules.stations.models import Station

class RecordsStatus(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    INACTIVE = 0, 'Inactive'

# o campo sensors é = [{
#   type: SensorType;
#   value: number | string;
#   unit: UnitType;
# }]

class Records(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    timestamp = models.DateTimeField()
    status = models.IntegerField(choices=RecordsStatus.choices, default=RecordsStatus.ACTIVE)

    sensors = models.JSONField(
        default=list, 
        blank=True,   
        null=True,  
    )
    
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='records'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"
