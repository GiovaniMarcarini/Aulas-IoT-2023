
#import das bibliotecas
import RPi.GPIO as gpio
import time as delay

gpio.setmode(gpio.BOARD)

pin_t = 15
pin_e = 16
lixeira_v = 20

gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)

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

    
while True:
    valorRecebido = distancia()
    print("Distancia = %.1f CM" % valorRecebido)
    espaco_d = (valorRecebido/lixeira_v)*100
    print("Espaço disponível na lixeira = %.1f" % espaco_d, '%')
    espaco_o = 100 - espaco_d
    print("Espaço ocupado na lixeira = %.1f" % espaco_o, '%')
    delay.sleep(5)
