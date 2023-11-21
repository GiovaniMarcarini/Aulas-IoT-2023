import paho.mqtt.client as mqtt
import time as delay
import RPi._GPIO as gpio

gpio.setmode(gpio.BOARD)

mqtt_umidade = ''
mqtt_temperatura = ''
mqtt_ocupacaoLixeira = ''
mqtt_distancia = ''

def on_connect(client, userdata, flags, rc):
    print('Conectado com o código: '+ str(rc))
    client.subscribe('aula/umidade/prof')
    client.subscribe('aula/1411/temperatura/prof')
    client.subscribe('aula/1411/distancia/prof')
    client.subscribe('aula/1411/ocupacao/prof')

def on_message(client, userdata, msg):
    global mqtt_umidade
    global mqtt_temperatura
    global mqtt_distancia
    global mqtt_ocupacaoLixeira

    if msg.topic == 'aula/umidade/prof':
        mqtt_umidade = str(msg.payload.decode('utf-8'))
        print(msg.topic + " " + mqtt_umidade)
        
client = mqtt.Client('Subscribe-Prof')
client.connect('10.10.10.80', 1888, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
client.disconnect()

