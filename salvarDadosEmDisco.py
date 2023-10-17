
#import das bibliotecas
import RPi.GPIO as gpio
import time as delay
import Adafruit_DHT as dht
import os

#mode de leitura dos pinos da placa
gpio.setmode(gpio.BOARD)

#pino do sensor dht11
pin_sensor = 4 #lembrar que a biblioteca é modo BCM
dht_sensor = dht.DHT11

f = open('/root/Aula-IoT/log.txt', 'a+')
f.write('Data       Hora         Temperatura         Umidade\n')
f.close()

while True:
    #leitura dos valores 
    umid, temp = dht.read(dht_sensor, pin_sensor)

    #validação se obteve valor
    if umid is not None and temp is not None:
        f = open('/root/Aula-IoT/log.txt', 'a+')
        f.write("{0}         {1}         {2:0.1f}*C         {3:0.1f}%\n"
                .format(delay.strftime('%m/%d/%y'), delay.strftime('%H:%M'),
                        temp, umid))
        f.close()
        print("Temperatura = {0:0.1f}*C | Umidade = {1:0.1f}%".format(temp, umid))

    else:
        f = open('/root/Aula-IoT/log.txt', 'a+')
        f.write("{0}         {1}       Não foi possível obter os valores\n"
                .format(delay.strftime('%m/%d/%y'), delay.strftime('%H:%M')))
        f.close()
        print("Não foi possível obter valores")
      
    delay.sleep(5)
