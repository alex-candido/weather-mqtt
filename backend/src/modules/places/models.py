# src/modules/places/models.py

import uuid

from django.db import models

class PlaceStatus(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    INACTIVE = 0, 'Inactive'

class Place(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=PlaceStatus.choices, default=PlaceStatus.ACTIVE)

    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    