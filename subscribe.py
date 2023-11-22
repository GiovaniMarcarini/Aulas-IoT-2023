import paho.mqtt.client as mqtt
import time as delay
import RPi._GPIO as gpio

gpio.setmode(gpio.BOARD)

ledVermelho = 11

mqtt_umidade = ''
mqtt_temperatura = ''
mqtt_ocupacaoLixeira = ''
mqtt_distancia = ''

gpio.setup(ledVermelho, gpio.OUT)

def on_connect(client, userdata, flags, rc):
    print('Conectado com o código: '+ str(rc))
    client.subscribe('aula/umidade/prof')
    client.subscribe('aula/temperatura/prof')
    client.subscribe('aula/distancia/prof')
    client.subscribe('aula/ocupacao/prof')

def on_message(client, userdata, msg):
    global mqtt_umidade
    global mqtt_temperatura
    global mqtt_distancia
    global mqtt_ocupacaoLixeira

    if msg.topic == 'aula/umidade/prof':
        mqtt_umidade = str(msg.payload.decode('utf-8'))
        print(msg.topic + " " + mqtt_umidade)

    if msg.topic == 'aula/temperatura/prof':
        mqtt_temperatura = str(msg.payload.decode('utf-8'))
        print(msg.topic + " " + mqtt_temperatura)

    if msg.topic == 'aula/distancia/prof':
        mqtt_distancia = str(msg.payload.decode('utf-8'))
        print(msg.topic + " " + mqtt_distancia)
    
    if msg.topic == 'aula/ocupacao/prof':
        mqtt_ocupacaoLixeira = str(msg.payload.decode('utf-8'))
        print(msg.topic + " " + mqtt_ocupacaoLixeira)
        if (float(mqtt_ocupacaoLixeira) >= 80):
            gpio.output(ledVermelho, True)
        else:
            gpio.output(ledVermelho, False)

client = mqtt.Client('proff-s')
client.connect('10.10.10.80', 1888, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
client.disconnect()

