#importação das bibliotecas 
import RPi.GPIO as gpio
import time as delay
import Adafruit_DHT as dht
import paho.mqtt.client as mqtt

#definição de pinagem seguindo a ordem da placa
gpio.setmode(gpio.BOARD)
 
#variáveis de interação com os GPIOs
ledvermelho = 11
ledverde = 12
ldr = 13
botao = 18
pin_dht = 4
pin_t = 15 
pin_e = 16

#definição do modelo de sensor
dht_sensor = dht.DHT11

#variável de distancia limite para considerar intrusão e gerar alerta
distanciaSegura = 5 #CM

#variável de controle para alerta
alerta = False

#canais para publicação no mqtt
canalUmidade = 'prova/humidade'
canalTemperatura = 'prova/temperatura'
canalBotao = 'prova/botao'
canalAlerta = 'prova/alerta'
canalLedVermelho = 'prova/ledVermelho'
canalLedVerde = 'prova/ledVerde'

#configuração do modo de operação do GPIO para cada pino
gpio.setup(ledvermelho, gpio.OUT)
gpio.setup(ledverde, gpio.OUT)
gpio.setup(botao, gpio.IN)
gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)
gpio.setup(ldr, gpio.IN)

#forçar os leds a iniciarem desligados
gpio.output(ledvermelho, False)
gpio.output(ledverde, False)

#definição para obter a distância lida pelo sensor HC-SR04
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

#definição para obter dos valores lidos pelo sensor DHT11
def temperatura():
    umid, temp = dht.read(dht_sensor, pin_dht)

    #validação, caso não retorna valor popula as variáveis com zero
    if umid is None:
        umid = 0.0
    if temp is None:
        temp = 0.0
    return umid, temp    

#conexão com o broker mqtt
client = mqtt.Client('Prof-Publish')
client.connect('10.10.10.80',1888,60)

#definição para controlar o clique do botão
def botaopressionado():
    client.publish(canalBotao, 'Botão pressionado')
    print('Botão pressionado')

#definição para controlar os alertas
def msgAlerta(msg, tipo):
    #publica no calna alerta a msg recebida
    client.publish(canalAlerta, msg)

    #verifica o tipo de alerta, se é pra ligar o alerta ou desligar
    if tipo == True:
        gpio.output(ledverde, False)
        gpio.output(ledvermelho, True)
        client.publish(canalLedVerde, 'Led verde desligado')
        client.publish(canalLedVermelho, 'Led de alerta ligado')
    else:
        gpio.output(ledvermelho, False)
        gpio.output(ledverde, True)
        client.publish(canalLedVermelho, 'Led de alerta desligado')
        client.publish(canalLedVerde, 'Led verde ligado')


while True:

    #verifica se houve o clique no botão
    if gpio.input(botao) == True:
        delay.sleep(0.5)
        botaopressionado()
        msgAlerta('Sistema iniciado', False)

        #inicialização das váriáveis de horário para controle das leituras
        horaLeituraDistancia = delay.time()
        horaLeituraDHT = delay.time()

        #se clicou a primeira vez inicia o sistema e trava o processamento dentro de outro loop para ignorar o primeiro clique do botão
        #lembrando que agora ele só vai desligar os alertas se for pressionado denovo
        while True:

            if gpio.input(botao) == True:
                delay.sleep(0.5)
                botaopressionado()

                #verifica se existe alerta, desliga o alerta
                if alerta:
                    msgAlerta('Alerta sendo desligado', False)

                    #atualiza a variável de controle de alerta
                    alerta = False
            
            #verifica o horário atual do sistema para fazer os controles de tempo das leituras dos sensores
            horaAtual = delay.time()

            #essa comparação faz com que o código não trave no delay e execute a leitura da distância a cada 5 segundos se o alerta estiver desligado
            #em caso de alerta ligado não preciso verificar
            if (horaAtual - horaLeituraDistancia) >= 5 and alerta == False:
                valor_lido = distancia()
                print(valor_lido)
                if valor_lido <= distanciaSegura:
                    msgAlerta('Alerta de movimento', True)

                    #atualiza a variável de controle do alerta
                    alerta = True
                    
                #atualiza a variável de controle com a ultuima hora da leitura
                horaLeituraDistancia = delay.time()
            
            #essa comparação faz com que o código não trave no delay e execute a leitura do sensor DHT a cada 15 segundos
            if (horaAtual - horaLeituraDHT) >= 15:
                client.publish(canalUmidade, str(temperatura()[0]))
                client.publish(canalTemperatura, str(temperatura()[0]))
                #atualiza o horário da ultima leitura
                horaLeituraDHT = delay.time()
