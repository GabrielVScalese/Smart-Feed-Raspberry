#################################################### Bibliotecas

# API
from flask import Flask, request
import socket
import json
import _thread

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
import RPi.GPIO as GPIO

#################################################### Deteccoes dos animais

def getNowDate():
    tz = pytz.timezone('America/Sao_Paulo')
    nowDate = datetime.datetime.now()

    return nowDate

# Valores que serao utilizados pelo Raspberry PI
petId = None # Para fazer requisicoes
animal = None # Tipo do animal
mode = None # Modo de despejamento
quantity = None # Quantidade de racao
schedules = None # Horarios de alimentacao
state = False # Indicar se a maquina esta vinculado a um pet
initialDate = None
jaRodou = False

#Motor
GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15]
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

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
            '''cap = cv2.VideoCapture('Raspberry Pi\\video.mp4')
            #cap = cv2.VideoCapture(0)
    
            COLORS = [(0,255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
            tempo0 = 0

            classNames = []
            with open('Raspberry Pi\detections\coco.names', 'r') as f:
                classNames = [cname.strip() for cname in f.readlines()]

            net = cv2.dnn.readNet('Raspberry Pi\detections\yolov4-tiny.weights', 'Raspberry Pi\detections\yolov4-tiny.cfg')
            model = cv2.dnn_DetectionModel(net)
            model.setInputParams(size=(416, 416), scale=1/255)'''

            while True:
                if state == True:
                    '''if (time.perf_counter() - tempo0 >= 1800 or tempo0 == 0):
                    _, frame = cap.read()

                    classes, scores, boxes = model.detect(frame, 0.1, 0.2)
                    for (classId, score, box) in zip(classes, scores, boxes):
                    color = COLORS[int(classId) % len(COLORS)]

                    label = f"{classNames[classId[0]].capitalize()} : {score}"

                    if classNames[classId[0]] == animal:
                    if score >= 0.65:
                    largura = box[2]
                    comprimento = box[3]
                    if (largura >= 220 or comprimento >= 220):
                    tempo0 = time.perf_counter()'''
                    if mode == 'Horário':
                        if TimeController.nowIsValid(schedules) and jaRodou == False:
                            '''cv2.rectangle(frame, box, color, 2)
                            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)'''
                            print('Máquina ativada')
                            for i in range(100):
                                for halfstep in range(8):
                                    for pin in range(4):
                                        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                                    time.sleep(0.001)
                            for i in range(100):
                                for halfstep in reversed(range(8)):
                                    for pin in range(4):
                                        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                                    time.sleep(0.001)
                                    
                            jaRodou = True
                            #guardar no banco a consumption dps q passar um dia
                        else:
                            if TimeController.nowIsValid(schedules) == False:
                                print('Fora de horário')
                                jaRodou = False
                            else:
                                print('Já rodou')
                            '''else:
                            cv2.rectangle(frame, box, color, 2)
                            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            else:
                            print('Muito distante')
                    else:
                    print(str(1800 - (time.perf_counter() - tempo0)) + ' segundos até a utilização')

                    cv2.imshow('Detections', frame)
                    if cv2.waitKey(1) == 27:
                    break'''
                else:
                    print('Dados necessarios nao foram vinculados')
        except Exception as e:
            print(e)
        except KeyboardInterrupt as k:
            print("Keyboard Interrupted")
        finally:
            GPIO.cleanup()

#################################################### API

app = Flask(__name__)

hostname = socket.gethostname()
localIp = socket.gethostbyname(hostname)
print(localIp)

@app.route("/")
def root():
    return {'message': "API is running!"}

@app.route("/activate", methods=['POST'])
def activateMotor ():
    print('Motor girando')

    return {'message': 'Ok'}

@app.route('/feeds/<int:pet>', methods=['PUT'])
def feedRoot(pet):
    global petId
    global animal
    global mode
    global quantity
    global schedules
    global state
    global initialDate
    
    data = request.get_json()
    petId = pet
    animal = data['animal'].lower()
    mode = data['mode']
    quantity = data['quantity']
    schedules = data['schedules']

    if state == False:
        initialDate = getNowDate()
    
    state = True

    return {'petId': petId, 'animal': animal, 'mode': mode, 'quantity': quantity, 'schedules': schedules}

def run ():
    app.run(host=localIp, port=5000)

#################################################### Threads

detector = Detector()
multicastServer = MulticastServer()

_thread.start_new_thread(multicastServer.run, ())
#run()
_thread.start_new_thread(run, ())
detector.run()