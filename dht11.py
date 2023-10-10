
#import das bibliotecas
import RPi.GPIO as gpio
import time as delay
import Adafruit_DHT as dht

#mode de leitura dos pinos da placa
gpio.setmode(gpio.BOARD)

#pino do sensor dht11
pin_sensor = 4 #lembrar que a biblioteca é modo BCM
dht_sensor = dht.DHT11

while True:
    #leitura dos valores 
    umid, temp = dht.read(dht_sensor, pin_sensor)

    #validação se obteve valor
    if umid is not None and temp is not None:
        print("Temperatura = {0:0.1f}*C | Umidade = {1:0.1f}%".format(temp, umid))
    else:
      print("Não foi possível obter valores")
      
    delay.sleep(5)
