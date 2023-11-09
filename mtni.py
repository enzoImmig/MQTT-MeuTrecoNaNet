import json
from paho.mqtt import client as mqtt_client
import time
import RPi.GPIO as GPIO

# parametros da conxao TCP
host = 'localhost'
port = 1883

# set gpio parameters
GPIO.setmode(GPIO.BOARD) # set numbers of pins as the numbers of boards
# GPIO.setup(pin, GPIO.(IN/OUT))

# dicionario com estrutura do arquivo JSON
transmit_file = {
    'Temperatura':24,
    'Unidade': "C",
    'Hora': "15:16",
}

# conexao com o broker e criação do cliente

# leitura dos valores por GPIO

#transmissao de dados por MQTT em tempo constante

# leitura de dados por MQTT

# interpretação de dados e controle por GPIO

def run():
    mqtt_connect()


if __name__ == "__main__":
    run()