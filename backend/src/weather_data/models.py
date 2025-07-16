from django.db import models

class Station(models.Model):
    station_id = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} ({self.station_id})"

    class Meta:
        verbose_name = "Estação"
        verbose_name_plural = "Estações"

class SensorData(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='sensor_readings')
    sensor_name = models.CharField(max_length=100) # Ex: thermometer_230
    sensor_type = models.CharField(max_length=50)  # Ex: temperature, humidity
    value = models.FloatField()
    unit = models.CharField(max_length=10)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.station.station_id} - {self.sensor_name}: {self.value}{self.unit} at {self.timestamp}"

    class Meta:
        verbose_name = "Dado de Sensor"
        verbose_name_plural = "Dados de Sensores"
        ordering = ['timestamp']
