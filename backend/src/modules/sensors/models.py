# src/modules/sensors/models.py

import uuid

from django.db import models

class SensorStatus(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    INACTIVE = 0, 'Inactive'

class SensorType(models.IntegerChoices):
    THERMOMETER = 1, 'Temperature'  
    HYGROMETER = 2, 'Humidity'      
    ANEMOMETER = 3, 'Wind'           
    PLUVIOMETER = 4, 'Rainfall'     
    SOLARIMETER = 5, 'Solar Radiation' 

class UnitType(models.IntegerChoices):
    CELSIUS = 1, 'Degrees Celsius (°C)'
    PERCENT = 3, 'Percentage (%)'
    METERS_PER_SECOND = 4, 'Meters per Second (m/s)'
    MILLIMETERS = 7, 'Millimeters (mm)'
    WATTS_PER_METER_SQUARED = 9, 'Watts per Square Meter (W/m²)'

class Sensor(models.Model): 
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    status = models.IntegerField(choices=SensorStatus.choices, default=SensorStatus.ACTIVE)
    type = models.IntegerField(choices=SensorType.choices)
    unit = models.IntegerField(choices=UnitType.choices)

    min_value = models.FloatField()
    max_value = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
