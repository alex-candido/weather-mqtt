import json
import paho.mqtt.client as mqtt
import time
from django.core.management.base import BaseCommand
from django.utils import timezone

from modules.stations.models import Station
from modules.records.models import Records # Alterado de SensorData

class Command(BaseCommand):
    help = 'Starts an MQTT listener to receive sensor data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting MQTT listener...'))

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = self._on_connect
        client.on_message = self._on_message

        try:
            client.connect("broker.hivemq.com", 1883, 60)
        except ConnectionRefusedError:
            self.stderr.write(self.style.ERROR("Erro: Conexão com o broker MQTT recusada. Verifique se o broker está em execução."))
            return

        client.loop_start()

        try:
            while True:
                time.sleep(1) # Pequeno atraso para evitar uso excessivo da CPU
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Listener interrompido pelo usuário."))
        finally:
            client.loop_stop()
            client.disconnect()
            self.stdout.write(self.style.SUCCESS("Listener MQTT finalizado."))

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.stdout.write(self.style.SUCCESS("Conectado ao Broker MQTT!"))
            client.subscribe("station/sensors")
            self.stdout.write(self.style.SUCCESS("Assinado ao tópico 'station/sensors'"))
        else:
            self.stderr.write(self.style.ERROR(f"Falha na conexão com o Broker MQTT. Código: {rc}"))

    def _on_message(self, client, userdata, msg):
        self.stdout.write(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
        try:
            payload = json.loads(msg.payload.decode())

            station_uuid = payload.get('station_id') # Alterado para station_uuid
            timestamp_str = payload.get('timestamp')
            sensors_data = payload.get('sensors', {})

            if not all([station_uuid, timestamp_str, sensors_data]):
                self.stderr.write(self.style.ERROR(f"Dados incompletos na mensagem: {payload}"))
                return

            timestamp = timezone.datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

            try:
                station = Station.objects.get(uuid=station_uuid) # Busca pela UUID
            except Station.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Estação com UUID {station_uuid} não encontrada. Ignorando mensagem."))
                return

            # Converte o dicionário de sensores para uma lista de dicionários
            formatted_sensors = []
            for sensor_name, data in sensors_data.items():
                sensor_type = data.get('type')
                value = data.get('value')
                unit = data.get('unit')

                if all([sensor_type, value is not None, unit]):
                    formatted_sensors.append({
                        "name": sensor_name,
                        "type": sensor_type,
                        "value": value,
                        "unit": unit
                    })
                else:
                    self.stderr.write(self.style.WARNING(f"  -> Aviso: Dados incompletos para o sensor {sensor_name}: {data}"))

            if formatted_sensors:
                Records.objects.create( # Criação do Records
                    station=station,
                    timestamp=timestamp,
                    sensors=formatted_sensors
                )
                self.stdout.write(self.style.SUCCESS(f"Registro criado para a estação {station.name} ({station.uuid}) com {len(formatted_sensors)} sensores."))
            else:
                self.stdout.write(self.style.WARNING(f"Nenhum dado de sensor válido para criar um registro para a estação {station.uuid}."))

        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR(f"Erro ao decodificar JSON: {msg.payload.decode()}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erro ao processar mensagem MQTT: {e}"))
