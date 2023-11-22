import RPi.GPIO as gpio
import time as delay
import Adafruit_DHT as dht
import paho.mqtt.client as mqtt

gpio.setmode(gpio.BOARD)
 
ledvermelho = 11
ledverde = 12
ldr = 13
botao = 18
pin_dht = 4
pin_t = 15 
pin_e = 16
lixeira_v = 20

dht_sensor = dht.DHT11

gpio.setup(ledvermelho, gpio.OUT)
gpio.setup(ledverde, gpio.OUT)
gpio.setup(botao, gpio.IN)
gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)
gpio.setup(ldr, gpio.IN)

gpio.output(ledvermelho, False)
gpio.output(ledverde, False)

def testeconexao():
    try:
        urlopen('http://colegiomaterdei.com.br', timeout=1)
        return True
    except:
        return False

if testeconexao() == True:
    gpio.output(ledverde, True)
    delay.sleep(2)
    gpio.output(ledverde, False)
else:
    gpio.output(ledvermelho, True)
    delay.sleep(2) 
    gpio.output(ledvermelho, False)
    
def distancia():
    gpio.output(pin_t, True)
    delay.sleep(0.000001)
    gpio.output(pin_t, False)
    tempo_i = delay.time()
    tempo_f = delay.time()
    
    while gpio.input(pin_e) == False:
        tempo_i = delay.time()
    while gpio.input(pin_e)  == True:
        tempo_f = delay.time()
     
    tempo_d = tempo_f - tempo_i
    
    distancia = (tempo_d*34300)/2
    return distancia

def temperatura():
    umid, temp = dht.read(dht_sensor, pin_dht)
    return umid, temp    
        
def luz():
    luminosidade = (gpio.input(ldr))
    
    if luminosidade == 1:
        luz = 'noite'
    else:
        luz = 'dia'
    return luz

client = mqtt.Client('Prof-Publish')
client.connect('10.10.10.80',1888,60)

while True:
    valor_lido = distancia()
    ocupacao_l = (valor_lido/lixeira_v)*100
    ocupacao_f = 100 - ocupacao_l
           
       
    try:        
        client.publish('aula/umidade/prof', str(temperatura()[0]))
        delay.sleep(1)  
        client.publish('aula/temperatura/prof', str(temperatura()[1]))
        delay.sleep(1) 
        client.publish('aula/distancia/prof', str(valor_lido))
        delay.sleep(1)
        client.publish('aula/ocupacao/prof', str(ocupacao_f) )
        print('Dados publicados > ', delay.strftime('%d/%m/%y'), 'às ', delay.strftime('%H:%M'))

        
    except Exception as e:
        client.loop_stop()
        client.disconnect()
        print(e)  
        
    delay.sleep(20)    
    
