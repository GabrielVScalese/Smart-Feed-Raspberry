#################################################### Bibliotecas

# API
from flask import Flask, request
import socket
import json
import _thread
import consumptions_repository as cr
import pets_repository as pr

# Deteccoes
#import cv2
import time
#import pafy
import datetime
import pytz
from time_controller import TimeController

# Multicast
from multicast_server import MulticastServer

#Motor
# import RPi.GPIO as GPIO

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
initialDate = None
jaRodou = False
jaReportou = False

#Motor
# GPIO.setmode(GPIO.BOARD)
# control_pins = [7,11,13,15]
# for pin in control_pins:
#     GPIO.setup(pin, GPIO.OUT)
#     GPIO.output(pin, 0)

# halfstep_seq = [
#     [1,0,0,0],
#     [1,1,0,0],
#     [0,1,0,0],
#     [0,1,1,0],
#     [0,0,1,0],
#     [0,0,1,1],
#     [0,0,0,1],
#     [1,0,0,1]
#     ]

class Detector:

    def __init__(self):
        pass

    def run(self):
        try:
            global jaReportou
            global jaRodou
            global quantityTotal

            while True:
                if state == True:
                    if mode == 'Horário':
                        if TimeController.nowIsValid(schedules) and jaRodou == False:
                            print('Máquina ativada')
                            # for i in range(100):
                            #     for halfstep in range(8):
                            #         for pin in range(4):
                            #             GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                            #         time.sleep(0.001)
                            # for i in range(100):
                            #     for halfstep in reversed(range(8)):
                            #         for pin in range(4):
                            #             GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                            #         time.sleep(0.001)
                                    
                            jaRodou = True
                        else:
                            if TimeController.nowIsValid(schedules) == False:
                                print('Fora de horário')
                                jaRodou = False
                            else:
                                print('Já rodou')
                else:
                    print('Dados necessarios nao foram vinculados')

                pets = pr.PetsRepository.getFeeds(1).json()
                print(pets)

                nowDate = datetime.datetime.now()
                if (nowDate.hour == 23 and nowDate.minute == 59 and nowDate.second == 59 and jaReportou == False):
                    stringNowDate = nowDate.strftime("%Y-%m-%d %H:%M:%SZ")
                    response = cr.ConsumptionsRepository.createConsumption({'pet_id': petId , 'date': stringNowDate, 'quantity': quantityTotal })
                    quantityTotal = 0
                    jaReportou = True
                    print('resposta: ' + str(response))
                
                if (jaReportou and nowDate.second != 59):
                    jaReportou = False

        except Exception as e:
            print(e)
        except KeyboardInterrupt as k:
            print("Keyboard Interrupted")
        finally:
            # GPIO.cleanup()
            print('GPIO limpo')


#################################################### Threads

detector = Detector()
multicastServer = MulticastServer()

_thread.start_new_thread(multicastServer.run, ())
detector.run()