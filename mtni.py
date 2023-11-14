import json
from paho.mqtt import client as mqtt_client
import time
#import RPi.GPIO as GPIO

# parametros da conxao TCP
host = 'mqtt.tago.io'
port = 1883
username = "Default"
password = "9132886f-3a1c-4f3f-9cd3-aae3f1725f45"
client_ID = "ENZO4411"

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
    'climatizador': False,
    'hora': "15:16",
}

# para enviar ao tago como variavel precisa estar neste formato {'variable': <variavel>, 'value':<valor>}
var_file = {
    'variable':"temperatura",
    'value': 15,
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

    # Cria o objeto do cliente e faz a conexão com o broker
    client = mqtt_client.Client(client_ID)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(host, port)

    return client

# leitura dos valores por GPIO
def GPIO_Readings():
    #gpio read
    #transmit_file['hora'] = str(time.localtime())
    return json.dumps(var_file)

# transmissao de dados por MQTT em tempo constante
def mqtt_publish(client: mqtt_client):
    client.publish(topic_reading, GPIO_Readings())
    print("arquivo enviado")
    time.sleep(10)

# leitura de dados por MQTT
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if(is_json(msg.payload.decode())):
            msg_dic = json.loads(msg.payload.decode())
            if msg_dic['valor'] == 'true':
                transmit_file["climatizador"] = True
                print("Climatizador acionado")
            else: 
                transmit_file["climatizador"] = False
                print("Climatizador desacionado")
            # aqui coloca a função de tratamento de dados
    
    client.subscribe(topic_commands)
    #client.subscribe(topic_reading)
    client.on_message = on_message

# interpretação de dados e controle por GPIO
def control_action():
    print("algo acontece aqui")
    # aqui usa caso queira enviar alguma ação para o controlador, tipo ligar um led ou buzzer

def run():    
    client = mqtt_connect() #conecta
    client.loop_start() # cria uma thread pra conexão (non-blocking)

    # ESPERA PELA CONEXÃO COM O BROKER
    while not client.is_connected():
        time.sleep(1)

    #SUBSCRIBE
    subscribe(client) # comandos vindos do broker

    while 1:
        #publica as leituras do sensor
        mqtt_publish(client)

if __name__ == "__main__":
    run()