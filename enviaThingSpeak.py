#importa as bibliotecas
import time as delay
from urllib.request import urlopen
import RPi.GPIO as gpio
import Adafruit_DHT as dht
import requests

gpio.setmode(gpio.BOARD)

#variáveis de controle GPIO
ledVermelho, ledVerde = 11, 12
botao = 18
pinDHT = 4
pin_t = 15
pin_e = 16

#variáveis de configuração API ThingSpeak
urlBase = 'https://api.thingspeak.com/update?api_key='
apiKeyWrite = 'M785BEOAQJ89A3E7'
fieldTemmp = '&field1='
fieldUmid = '&field2='
fieldLixeira = '&field3='
fieldDistancia = '&field4='

#configurações 
dht_sensor = dht.DHT11

gpio.setup(ledVermelho, gpio.OUT)
gpio.setup(ledVerde, gpio.OUT)

gpio.output(ledVermelho, False)
gpio.output(ledVerde, False)

#definição para testar a conexão com a internet
def conexao():
    try:
        urlopen('https://www.materdei.edu.br/pt', timeout=1)
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

def sensorDHT():
    umid, temp = dht.read(dht_sensor, pinDHT)
    if umid is not None and temp is not None:
        return temp, umid
    else:
        temp = 0.0
        umid = 0.0
        return temp, umid
        
#verifica se existe conexão ou não
if conexao() == True:
    #se tiver internet pisca 3 vezes o led verde
    i = 0
    while i <= 3:
        gpio.output(ledVerde, True)
        delay.sleep(1)
        gpio.output(ledVerde, False)
        delay.sleep(1)
        i = i + 1

    #loop de execução principal
    while True:
        
        #criação da variável com os dados
        dados = (urlBase + apiKeyWrite + fieldTemmp + str(sensorDHT()[0]) +
                fieldUmid + str(sensorDHT()[1]))
        
        #envia os dados para a API
        requests.post(dados)
        print('dados enviados')
        delay.sleep(30)

else:
    #se não tiver internet pisca 3 vezes o led vermelho
    i = 0
    while i <= 3:
        gpio.output(ledVermelho, True)
        delay.sleep(1)
        gpio.output(ledVermelho, False)
        delay.sleep(1)
        i = i + 1
