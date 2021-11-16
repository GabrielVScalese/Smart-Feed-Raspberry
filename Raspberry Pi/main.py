#################################################### Bibliotecas

# API
import _thread
import consumptions_repository as cr
import pets_repository as pr

# Deteccoes
import datetime
import pytz
from time_controller import TimeController

# Multicast
from multicast_server import MulticastServer

#Motor e Balanca
import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
#control_pins = [7,11,13,15]
control_pins = [4,17,27,22]
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

referenceUnit = 1
from hx711 import HX711

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

#################################################### Deteccoes dos animais

def getNowDate():
    tz = pytz.timezone('America/Sao_Paulo')
    nowDate = datetime.datetime.now()

    return nowDate

# Valores que serao utilizados pelo Raspberry PI
petId = None # Para fazer requisicoes
animal = None # Tipo do animal
mode = None # Modo de despejamento
quantityTotal = 0 # Quantidade de racao total no dia
quantity = 0 # Quantidade de racao
schedules = None # Horarios de alimentacao
state = False # Indicar se a maquina esta vinculado a um pet
jaRodou = False # Já rodou o motor?
jaReportou = False # Já reportou o consumo?
qtdBalanca = 0 # Quantidade de alimento na balança
pesoPrevioBalanca = 0 # Peso que ja estava na balança, a ser desconsiderado
pesoPote = 0 # Peso do pote de racao

#Motor

halfstep_seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
    ]

class Detector:

    def __init__(self):
        pass

    def run(self):
        try:
            #variaveis globais
            global petId
            global animal
            global mode
            global quantityTotal
            global quantity
            global schedules
            global state
            global jaRodou
            global jaReportou
            global pesoPrevioBalanca
            global qtdBalanca
            global pesoPote

            pesoPote = hx.get_weight(5) #recebe leitura do peso do pote (obs: reiniciar maquina ao trocar pote)
            hx.power_down()
            hx.power_up()
            time.sleep(0.1)

            while True:
                #recuperacao de dados
                pets = pr.PetsRepository.getFeeds(1).json()
                petId = pets[0]['id']
                mode = pets[0]['feed']['mode']
                quantity = pets[0]['feed']['quantity']
                schedules = pets[0]['feed']['schedules']
                
                xRot = int(quantity / 50) #calcula o numero de rotacoes com base na quantidade de racao
                
                if mode == 'Horário':
                    #se estiver no horario e ainda nao girou nesse horario
                    if TimeController.nowIsValid(schedules) and jaRodou == False or True:
                        print('Máquina ativada')
                        
                        quantityTotal += quantity #adiciona o depositado no horario ao total
                        
                        #gira o motor
                        for i in range(xRot):
                            for i in range(100):
                                for halfstep in range(8):
                                    for pin in range(4):
                                        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                                    time.sleep(0.001)
                            time.sleep(0.3)
                            for i in range(100):
                                for halfstep in reversed(range(8)):
                                    for pin in range(4):
                                        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                                    time.sleep(0.001)
                                
                        jaRodou = True
                    else:
                        if TimeController.nowIsValid(schedules) == False:
                            print('Fora de horário')
                            jaRodou = False
                        else:
                            print('Já rodou')
                
                #ao fim do dia, registra o consumo
                nowDate = datetime.datetime.now()
                if (nowDate.hour == 23 and nowDate.minute == 59 and jaReportou == False):
                    stringNowDate = nowDate.strftime("%Y-%m-%d %H:%M:%SZ")
                    pesoPrevioBalanca = hx.get_weight(5) - pesoPote #recebe leitura de sobras - peso do pote
                    hx.power_down()
                    hx.power_up()
                    time.sleep(0.1)
                    qtdBalanca = quantityTotal - pesoPrevioBalanca #recebe a quantidade - sobras
                    response = cr.ConsumptionsRepository.createConsumption({'pet_id': petId , 'date': stringNowDate, 'quantity': qtdBalanca })
                    quantityTotal = 0
                    jaReportou = True
                    print('resposta: ' + str(response.json()))
                
                if (jaReportou and nowDate.minute != 59):
                    jaReportou = False

        except Exception as e:
            print(e)
        except KeyboardInterrupt as k:
            print("Keyboard Interrupted")
        finally:
            GPIO.cleanup()
            print('GPIO limpo')


#################################################### Threads

detector = Detector()
multicastServer = MulticastServer()

_thread.start_new_thread(multicastServer.run, ())
detector.run()
