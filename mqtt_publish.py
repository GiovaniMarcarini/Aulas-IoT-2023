
import RPi.GPIO as gpio
import time as delay
import Adafruit_DHT as dht
import paho.mqtt.client as mqtt
from urllib.request import urlopen

gpio.setmode(gpio.BOARD)

ledVermelho = 11
ledVerde = 12
botao = 18
pin_dht = 4
pin_t = 15
pin_e = 16

dht_sensor = dht.DHT11

lixeira_v = 20

gpio.setup(ledVermelho, gpio.OUT)
gpio.setup(ledVerde, gpio.OUT)
gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)
gpio.setup(botao, gpio.IN)

gpio.output(ledVermelho, False)
gpio.output(ledVerde, False)

def conexao():
    try:
        urlopen('https://materdei.edu.br/pt', timeout=1)
        return True
    except:
        return False
    
def distancia():
    gpio.output(pin_t, True)
    delay.sleep(0.000001)
    gpio.output(pin_t, False)
    tempo_i = delay.time()
    tempo_f = delay.time()

    while gpio.input(pin_e) == False:
        tempo_i = delay.time()
    while gpio.input(pin_e) == True:
        tempo_f = delay.time()

    tempo_d = tempo_f - tempo_i

    distancia = (tempo_d*34300)/2
    return distancia

def dht():
    umd, temp = dht.read(dht_sensor, pin_dht)
    return umd, temp
    
if conexao():
    client = mqtt.Client('Prof-Publish')
    client.connect('10.10.10.80', 1888, 60)
    while True:
        valor_lido = distancia()
        ocupacao_l = (valor_lido/lixeira_v)*100

        if ocupacao_l > 100:
            ocupacao_l = 100

        ocupacao_d = 100 - ocupacao_l

        try:
            client.publish('aula/1411/umidade', str(dht()[0]) )
            delay.sleep(1)
            client.publish('aula/14-11/temperatura/prof', str(dht()[1]) )
            delay.sleep(1)
            client.publish('aula/14-11/distancia/prof', str(distancia()) )
            delay.sleep(1)
            client.publish('aula/14-11/ocupacao/prof', str(ocupacao_l) )
            delay.sleep(1)

        except Exception as e:
            print(e)
            client.loop_stop()
            client.disconnect()
        
        print('dados publicados')
        delay.sleep(10)

else:
    print('Sem conexão')
