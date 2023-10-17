
#importa as bibliotecas
import time as delay
from urllib.request import urlopen
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)

ledVermelho, ledVerde = 11, 12
botao = 18
pinDHT = 4
pinT = 15
pinE = 16

urlBase = 'https://api.thingspeak.com/update?api_key='
apiKeyWrite = 'M785BEOAQJ89A3E7'
fieldTemmp = 'field1='
fieldUmid = 'field2='
fieldLixeira = 'field3='
fieldDistancia = 'field4='

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

else:
    #se não tiver internet pisca 3 vezes o led vermelho
    i = 0
    while i <= 3:
        gpio.output(ledVermelho, True)
        delay.sleep(1)
        gpio.output(ledVermelho, False)
        delay.sleep(1)
        i = i + 1
