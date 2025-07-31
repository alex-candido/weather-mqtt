import requests
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime, timezone

# --- Configurações ---

# MQTT Broker
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "station/sensors"

# Estação Meteorológica
# TODO: Make STATION_ID dynamic (e.g., from env var or command line arg)
STATION_ID = "d17b5b3e-5c67-4231-9a84-4b18d72f0e56"
CITY_NAME = "Fortaleza" # Keep for now, but it's not used in the final payload location
LATITUDE = -3.73
LONGITUDE = -38.52

# API de Meteorologia (Open-Meteo)
API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m", "shortwave_radiation"],
    "wind_speed_unit": "ms"
}

# Definição dos Sensores
# Mapeia nomes descritivos dos sensores para os dados da API e seus tipos.
SENSOR_DEFINITIONS = [
    {
        "name": "thermometer_230",
        "type": "thermometer", # Changed from "temperature"
        "api_key": "temperature_2m",
        "unit": "°C"
    },
    {
        "name": "hygrometer_597",
        "type": "hygrometer", # Changed from "humidity"
        "api_key": "relative_humidity_2m",
        "unit": "%"
    },
    {
        "name": "anemometer_588",
        "type": "anemometer", # Changed from "wind_speed"
        "api_key": "wind_speed_10m",
        "unit": "m/s"
    },
    {
        "name": "pluviometer_318",
        "type": "pluviometer", # Changed from "rain"
        "api_key": "precipitation",
        "unit": "mm"
    },
    {
        "name": "solarimeter_999",
        "type": "solarimeter",
        "api_key": "shortwave_radiation",
        "unit": "W/m²"
    }
]

# Intervalo entre os envios (em segundos)
SEND_INTERVAL = 5

# --- Funções ---

def get_weather_data():
    """Busca os dados meteorológicos mais recentes da API."""
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()
        data = response.json()
        print(f"Dados meteorológicos de {CITY_NAME} recebidos da API com sucesso.")
        return data.get("current")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados da API: {e}")
        return None

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback executado quando o cliente se conecta ao broker."""
    if rc == 0:
        print(f"Conectado ao Broker MQTT em {MQTT_BROKER}:{MQTT_PORT}")
    else:
        print(f"Falha na conexão com o Broker MQTT. Código de retorno: {rc}")

def on_disconnect(client, userdata, rc, properties=None):
    """Callback executado quando o cliente se desconecta."""
    print("Desconectado do Broker MQTT.")

def main():
    """Função principal que executa o simulador."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except ConnectionRefusedError:
        print(f"Erro: Conexão com o broker em {MQTT_BROKER}:{MQTT_PORT} foi recusada.")
        print("Verifique se o broker MQTT está em execução (ex: 'systemctl start mosquitto' ou 'mosquitto -d').")
        exit(1)

    client.loop_start()

    try:
        while True:
            current_weather = get_weather_data()

            if current_weather:
                sensors_payload = {}
                for sensor in SENSOR_DEFINITIONS:
                    value = current_weather.get(sensor["api_key"])
                    if value is not None:
                        sensors_payload[sensor["name"]] = {
                            "type": sensor["type"],
                            "value": float(value),
                            "unit": sensor["unit"]
                        }

                if sensors_payload:
                    full_payload = {
                        "station_id": STATION_ID,
                        "location": {
                            "latitude": LATITUDE,
                            "longitude": LONGITUDE
                        },
                        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                        "sensors": sensors_payload
                    }

                    json_payload = json.dumps(full_payload, indent=2, ensure_ascii=False)

                    result = client.publish(MQTT_TOPIC, json_payload)
                    result.wait_for_publish()

                    if result.is_published():
                        print(f"Publicado em {MQTT_TOPIC}:\n{json_payload}\n")
                    else:
                        print("Falha ao publicar dados da estação.")

            else:
                print("Não foi possível obter dados meteorológicos. Tentando novamente em 60 segundos.")
                time.sleep(45) # Aguarda 45s + 15s do final do loop

            time.sleep(SEND_INTERVAL)

    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo usuário.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Simulador finalizado.")

if __name__ == "__main__":
    main()
