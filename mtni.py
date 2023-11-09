import json
from paho.mqtt import client as mqtt_client
import time
#import RPi.GPIO as GPIO

# parametros da conxao TCP
host = 'localhost'
port = 1883

# parametros da comunicação MQTT
topic_commands = 'Liberato/Sensores/Comandos'
topic_reading = 'Liberato/Sensores/Leituras'

# set gpio parameters
#GPIO.setmode(GPIO.BOARD) # set numbers of pins as the numbers of boards
# GPIO.setup(pin, GPIO.(IN/OUT))

# dicionario com estrutura do arquivo JSON
transmit_file = {
    'temperatura':24,
    'unidade': "C",
    'hora': "15:16",
}

# verifica se os arquivos enviados estao no formato JSON
def is_json(mensagi):
    try:
        json.loads(mensagi)
    except ValueError as e:
        return False
    return True

# conexao com o broker e criação do cliente
def mqtt_connect():
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Cria o objeto do cliente
    client = mqtt_client.Client()

    # atribuindo a função de callback criada ao objeto
    client.on_connect = on_connect

    # faz a conexão com o broker
    client.connect(host, port)

    return client

# leitura dos valores por GPIO
def GPIO_Readings():
    #gpio read
    transmit_file['hora'] = str(time.localtime)
    return json.dumps(transmit_file)

# transmissao de dados por MQTT em tempo constante
def mqtt_publish(client: mqtt_client):
    client.publish(topic_reading, "arquivo JSON com leituras dos valores dos sensores")
    time.sleep(5)

# leitura de dados por MQTT
def subscribe(client: mqtt_client):
    
    def on_message(client, userdata, msg):
        if(is_json(msg.payload.decode())):
            msg_dic = json.loads(msg.payload.decode())
            print(msg_dic)
            # aqui coloca a função de tratamento de dados
    
    client.subscribe(topic_commands)
    client.on_message = on_message

# interpretação de dados e controle por GPIO
def control_action():
    print("algo acontece aqui")
    # aqui usa caso queira enviar alguma ação para o controlador, tipo ligar um led ou buzzer

def run():
    client = mqtt_connect()
    client.loop_start()
    subscribe(client)

    while 1:
        mqtt_publish()


if __name__ == "__main__":
    run()