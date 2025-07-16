#include <WiFi.h>
#include <HTTPClient.h>
#include <PubSubClient.h>
#include <ArduinoJson.h> // Certifique-se de ter esta biblioteca instalada

// --- Credenciais WiFi ---
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// --- Broker MQTT ---
const char* mqtt_broker = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "estacao/sensores";
const char* mqtt_client_id = "esp32_weather_simulator"; // ID único para o cliente MQTT

WiFiClient espClient;
PubSubClient client(espClient);

// --- Configurações da Estação Meteorológica ---
const char* station_id = "STATION_FORTALEZA_001";
const char* city_name = "Fortaleza";
const float latitude = -3.73; // Latitude de Fortaleza
const float longitude = -38.52; // Longitude de Fortaleza

// URL Base da API Open-Meteo
const char* api_url_base = "https://api.open-meteo.com/v1/forecast";

// Definição dos Sensores (mapeamento de chaves da API para o nosso formato)
struct SensorDef {
    const char* name;     // Nome/ID do sensor (ex: thermometer_230)
    const char* type;     // Tipo de medição (ex: temperature)
    const char* api_key;  // Chave correspondente na resposta da API Open-Meteo
    const char* unit;     // Unidade de medida
};

SensorDef sensorDefinitions[] = {
    {"thermometer_230", "temperature", "temperature_2m", "°C"},
    {"hygrometer_597", "humidity", "relative_humidity_2m", "%"},
    {"anemometer_588", "wind_speed", "wind_speed_10m", "m/s"},
    {"pluviometer_318", "rain", "precipitation", "mm"}
};
const int numSensors = sizeof(sensorDefinitions) / sizeof(sensorDefinitions[0]);

// Intervalo de envio de dados (em milissegundos)
unsigned long lastSendTime = 0;
const long sendInterval = 15000; // 15 segundos

// --- Funções de Conexão ---
void setup_wifi() {
    delay(10);
    Serial.print("Conectando a ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nWiFi conectado");
    Serial.print("Endereço IP: ");
    Serial.println(WiFi.localIP());
}

void reconnect_mqtt() {
    // Loop até estarmos conectados
    while (!client.connected()) {
        Serial.print("Tentando conexão MQTT...");
        // Tenta conectar
        if (client.connect(mqtt_client_id)) {
            Serial.println("conectado");
            // Uma vez conectado, você pode se inscrever em tópicos aqui, se necessário
            // client.subscribe("meu/topico");
        } else {
            Serial.print("falhou, rc=");
            Serial.print(client.state());
            Serial.println(" tentando novamente em 5 segundos");
            // Espera 5 segundos antes de tentar novamente
            delay(5000);
        }
    }
}

// --- Função para Buscar Dados da API ---
String get_weather_data() {
    HTTPClient http;
    String url = String(api_url_base) + "?latitude=" + String(latitude, 6) + "&longitude=" + String(longitude, 6) + "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&wind_speed_unit=ms";
    Serial.print("[HTTP] GET... ");
    Serial.println(url);

    http.begin(url); // Inicia a conexão HTTP
    int httpCode = http.GET(); // Faz a requisição GET

    if (httpCode > 0) { // Se o código de retorno for maior que 0 (sucesso ou erro do servidor)
        Serial.printf("[HTTP] GET... código: %d\n", httpCode);
        if (httpCode == HTTP_CODE_OK) { // Se a requisição foi bem-sucedida (código 200)
            String payload = http.getString(); // Obtém o payload da resposta
            // Serial.println(payload); // Descomente para ver o JSON completo da API
            http.end();
            return payload;
        }
    } else { // Erro na conexão HTTP
        Serial.printf("[HTTP] GET... falhou, erro: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end(); // Fecha a conexão
    return ""; // Retorna string vazia em caso de erro
}

// --- Função para Publicar Dados MQTT ---
void publish_sensor_data(String weatherJson) {
    // Tamanho do documento JSON para deserialização e serialização
    // Ajuste este valor conforme a complexidade do seu JSON
    const size_t CAPACITY = 1024; 
    DynamicJsonDocument doc(CAPACITY);

    // Deserializa o JSON recebido da API
    DeserializationError error = deserializeJson(doc, weatherJson);

    if (error) {
        Serial.print(F("deserializeJson() falhou: "));
        Serial.println(error.f_str());
        return;
    }

    JsonObject current = doc["current"];

    // Constrói o novo payload JSON para o MQTT
    DynamicJsonDocument outputDoc(CAPACITY);
    outputDoc["station_id"] = station_id;

    JsonObject location = outputDoc.createNestedObject("location");
    location["city"] = city_name;
    location["latitude"] = latitude;
    location["longitude"] = longitude;

    // Obtém o timestamp atual (para ESP32, idealmente via NTP)
    // Para este exemplo, usaremos um placeholder ou um timestamp simples.
    // Em um projeto real, você usaria uma biblioteca NTP para obter a hora exata.
    char timestamp_buf[30];
    // Exemplo de como obter um timestamp real com NTP (requer configuração prévia do NTPClient)
    // time_t now; time(&now); struct tm timeinfo; localtime_r(&now, &timeinfo);
    // strftime(timestamp_buf, sizeof(timestamp_buf), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);
    
    // Placeholder para simulação:
    sprintf(timestamp_buf, "2025-07-15T%02d:%02d:%02dZ", hour(), minute(), second());
    outputDoc["timestamp"] = timestamp_buf;

    JsonObject sensors = outputDoc.createNestedObject("sensors");

    for (int i = 0; i < numSensors; i++) {
        SensorDef s = sensorDefinitions[i];
        if (current.containsKey(s.api_key)) {
            JsonObject sensorObj = sensors.createNestedObject(s.name);
            sensorObj["type"] = s.type;
            sensorObj["value"] = current[s.api_key].as<float>();
            sensorObj["unit"] = s.unit;
        }
    }

    String output;
    serializeJson(outputDoc, output);
    Serial.print("Publicando MQTT: ");
    Serial.println(output);

    if (client.publish(mqtt_topic, output.c_str())) {
        Serial.println("Mensagem publicada com sucesso");
    } else {
        Serial.println("Falha ao publicar mensagem");
    }
}

// --- Setup e Loop do Arduino ---
void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_broker, mqtt_port);
    // client.setCallback(callback); // Não é necessário para um cliente que apenas publica
}

void loop() {
    if (!client.connected()) {
        reconnect_mqtt();
    }
    client.loop(); // Mantém a conexão MQTT ativa e processa mensagens pendentes

    unsigned long currentMillis = millis();
    if (currentMillis - lastSendTime >= sendInterval) {
        lastSendTime = currentMillis;
        String weatherData = get_weather_data();
        if (weatherData.length() > 0) {
            publish_sensor_data(weatherData);
        }
    }
}