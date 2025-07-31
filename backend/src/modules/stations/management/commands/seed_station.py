import uuid
from django.core.management.base import BaseCommand
from modules.places.models import Place
from modules.stations.models import Station, StationStatus
from modules.sensors.models import Sensor, SensorType, UnitType # Importar Sensor e enums

# Use the STATION_ID from the simulator for consistency
SIMULATOR_STATION_UUID = "d17b5b3e-5c67-4231-9a84-4b18d72f0e56"

class Command(BaseCommand):
    help = 'Seeds the database with a sample Place, Station, and Sensors for testing.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding for Place, Station, and Sensors...'))

        # 1. Create or get a Place
        place_name = "Fortaleza - CE"
        place_defaults = {
            "description": "Sample location for weather station.",
            "latitude": -3.73,
            "longitude": -38.52,
        }
        place, created = Place.objects.get_or_create(
            name=place_name,
            defaults=place_defaults
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created Place: {place.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Place "{place.name}" already exists. Using existing one.'))
            # Update defaults if place already exists
            for key, value in place_defaults.items():
                setattr(place, key, value)
            place.save()
            self.stdout.write(self.style.SUCCESS(f'Updated existing Place: {place.name}'))


        # 2. Create or get a Station
        station_name = "ESP32 Simulator Station"
        station_defaults = {
            "name": station_name,
            "description": "Weather station simulated by ESP32.",
            "status": StationStatus.ACTIVE,
            "model": "ESP32-WROOM-32",
            "firmware": "1.0.0",
            "place": place,
        }
        
        # Try to get by UUID first, if not found, create
        try:
            station = Station.objects.get(uuid=SIMULATOR_STATION_UUID)
            created_station = False
            self.stdout.write(self.style.WARNING(f'Station with UUID {SIMULATOR_STATION_UUID} already exists. Using existing one.'))
            # Update defaults if station already exists
            for key, value in station_defaults.items():
                setattr(station, key, value)
            station.save()
            self.stdout.write(self.style.SUCCESS(f'Updated existing Station: {station.name}'))

        except Station.DoesNotExist:
            station = Station.objects.create(
                uuid=SIMULATOR_STATION_UUID,
                **station_defaults
            )
            created_station = True
            self.stdout.write(self.style.SUCCESS(f'Successfully created Station: {station.name} (UUID: {station.uuid})'))

        # 3. Create or get Sensors and associate them with the Station
        self.stdout.write(self.style.SUCCESS('Creating and associating sample Sensors...'))

        sensor_definitions = [
            {
                "name": "thermometer_230",
                "type": SensorType.THERMOMETER,
                "unit": UnitType.CELSIUS,
                "min_value": -50.0,
                "max_value": 50.0
            },
            {
                "name": "hygrometer_597",
                "type": SensorType.HYGROMETER,
                "unit": UnitType.PERCENT,
                "min_value": 0.0,
                "max_value": 100.0
            },
            {
                "name": "anemometer_588",
                "type": SensorType.ANEMOMETER,
                "unit": UnitType.METERS_PER_SECOND,
                "min_value": 0.0,
                "max_value": 60.0
            },
            {
                "name": "pluviometer_318",
                "type": SensorType.PLUVIOMETER,
                "unit": UnitType.MILLIMETERS,
                "min_value": 0.0,
                "max_value": 500.0
            },
            {
                "name": "solarimeter_999",
                "type": SensorType.SOLARIMETER,
                "unit": UnitType.WATTS_PER_METER_SQUARED,
                "min_value": 0.0,
                "max_value": 1500.0
            }
        ]

        for sensor_data in sensor_definitions:
            sensor, created = Sensor.objects.get_or_create(
                name=sensor_data["name"],
                type=sensor_data["type"].value, # Use .value for IntegerChoices
                defaults={
                    "description": f"Sensor {sensor_data["name"]} ({sensor_data["type"].label})",
                    "unit": sensor_data["unit"].value, # Use .value for IntegerChoices
                    "min_value": sensor_data["min_value"],
                    "max_value": sensor_data["max_value"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  -> Created Sensor: {sensor.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'  -> Sensor "{sensor.name}" already exists. Using existing one.'))
                # Update defaults if sensor already exists
                for key, value in sensor_data.items():
                    if key in ["min_value", "max_value", "unit", "type"]:
                        setattr(sensor, key, value.value if isinstance(value, (SensorType, UnitType)) else value)
                sensor.save()
                self.stdout.write(self.style.SUCCESS(f'Updated existing Sensor: {sensor.name}'))

            station.sensors.add(sensor)
            self.stdout.write(self.style.SUCCESS(f'  -> Associated Sensor {sensor.name} with Station {station.name}'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed.'))