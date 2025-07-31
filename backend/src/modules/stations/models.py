# src/modules/stations/models.py

import uuid

from django.db import models
from modules.places.models import Place

class StationStatus(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    INACTIVE = 0, 'Inactive'

class Station(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    status = models.IntegerField(choices=StationStatus.choices, default=StationStatus.ACTIVE)

    model = models.CharField(max_length=255)
    firmware = models.CharField(max_length=255, blank=True, null=True)
    installed_at = models.DateTimeField(null=True, blank=True)

    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='stations'
    )

    sensors = models.ManyToManyField(
        'sensors.Sensor',
        related_name='stations',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
