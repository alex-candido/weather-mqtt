# Simulador de Estação Meteorológica para ESP32

Este projeto simula uma estação meteorológica que busca dados climáticos reais de uma API e os publica em um broker MQTT, imitando o comportamento de um dispositivo ESP32.

## Pré-requisitos

1.  **Python 3.10+** e **pip**
2.  **PDM**: Um gerenciador de pacotes e dependências Python. Se não o tiver, instale com:
    ```bash
    pip install --user pdm
    ```
3.  **Broker MQTT**: Um broker MQTT, como o [Mosquitto](https://mosquitto.org/), deve estar instalado e em execução.

## Configuração

1.  **Instale o Mosquitto (Exemplo para Debian/Ubuntu):**
    ```bash
    sudo apt-get update
    sudo apt-get install -y mosquitto mosquitto-clients
    ```

2.  **Instale as dependências do projeto:**
    Navegue até o diretório `esp32_simulator` e execute:
    ```bash
    pdm install
    ```
    Isso criará um ambiente virtual e instalará as bibliotecas `requests` e `paho-mqtt`.

## Execução

1.  **Inicie o Broker MQTT:**
    Abra um novo terminal e inicie o Mosquitto em modo daemon (segundo plano):
    ```bash
    mosquitto -d
    ```
    Você pode verificar se ele está rodando na porta padrão (1883) com `sudo netstat -tulpn | grep 1883`.

2.  **Inicie o Simulador:**
    No diretório `esp32_simulator`, execute o script de inicialização:
    ```bash
    pdm run start
    ```

3.  **(Opcional) Monitore as mensagens MQTT:**
    Para confirmar que os dados estão sendo publicados, você pode usar um cliente MQTT para se inscrever no tópico. Em um novo terminal, execute:
    ```bash
    mosquitto_sub -h localhost -t "estacao/sensores" -v
    ```
    O parâmetro `-v` exibe o tópico junto com a mensagem. Você verá os dados dos sensores sendo impressos a cada 5 segundos.
