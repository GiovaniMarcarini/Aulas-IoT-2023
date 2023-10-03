# importação das bibliotecas
import RPi.GPIO as gpio
import time as delay

#Configuração de pinagem da placa
gpio.setmode(gpio.BOARD)

#Criação das variáveis de controle
ledVermelho = 11
ledVerde = 12

#Configuração da porta da raspberry
gpio.setup(ledVermelho, gpio.OUT)
gpio.setup(ledVerde, gpio.OUT)

#Forçar desligar leds
gpio.output(ledVermelho, False)
gpio.output(ledVerde, False)

#Loop de execução 
while True:
    #Liga o Led
    gpio.output(ledVermelho, True)
    print('Led Vermelho aceso')
    #aguarda 1 segundo
    delay.sleep(1)
    #desliga o led
    gpio.output(ledVermelho, False)
    print('Led Vermelho desligado')
    delay.sleep(1)


#Desabilitar Warning
gpio.setwarnings(False)
