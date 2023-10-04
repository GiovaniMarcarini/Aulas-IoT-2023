
#importação das bibliotecas
import RPi.GPIO as gpio
import time as delay

#setar modo de sequência da placa
gpio.setmode(gpio.BOARD)

#variáveis de controle
ledVermelho = 11
ledVerde = 12
botao = 18

#configurar portas
gpio.setup(ledVermelho, gpio.OUT)
gpio.setup(ledVerde, gpio.OUT)
gpio.setup(botao, gpio.IN)

#forçar a desligar portas dos leds
gpio.output(ledVermelho, False)
gpio.output(ledVerde, False)

#variáviel de controle do botão
contador = 0

#loop
while True:
    #verifica se houve o clique no botão
    if gpio.input(botao) == True:
        contador = contador + 1
        delay.sleep(0.5)
        
        #controle do pisca led
        i = 0

        # loop para piscar conforme a quantidade de clique
        while i < contador:
            gpio.output(ledVermelho, True)
            gpio.output(ledVerde, True)
            delay.sleep(0.5)
            gpio.output(ledVermelho, False)
            gpio.output(ledVerde, False)
            delay.sleep(0.5)
            i = i + 1

gpio.setwarnings(False)
