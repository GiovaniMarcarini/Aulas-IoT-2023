
#importa as bibliotecas
import time as delay
from urllib.request import urlopen
import RPi.GPIO as gpio
import requests

gpio.setmode(gpio.BOARD)

#variáveis de controle GPIO
ledVermelho, ledVerde = 11, 12

gpio.setup(ledVerde, gpio.OUT)
gpio.setup(ledVermelho, gpio.OUT)

def conexao():
    try:
        urlopen('https://www.materdei.edu.br/pt', timeout=1)
        return True
    except:
        return False
    
if conexao() == True:
    while True:
        consulta_t = requests.get(
    'https://api.thingspeak.com/channels/2309190/fields/1/last?key=K5TJHMHAD8WT2UB1')
        consulta_u = requests.get(
    'https://api.thingspeak.com/channels/2309190/fields/2/last?key=K5TJHMHAD8WT2UB1')
        
        print(float(consulta_t.text))
        delay.sleep(20)

else:
    print('Deu ruim...')
