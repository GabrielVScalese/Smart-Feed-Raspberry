#################################################### Bibliotecas

# API
from flask import Flask, request
import socket
import json
import _thread

# Deteccoes
import cv2
import time
#import pafy
import datetime
import pytz
from time_controller import TimeController

# Multicast
from multicast_server import MulticastServer

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

class Detector:

    def __init__(self):
        pass

    def run(self):
        try:
            cap = cv2.VideoCapture('video.mp4')
    
            COLORS = [(0,255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
            tempo0 = 0

            classNames = []
            with open('Raspberry Pi\detections\coco.names', 'r') as f:
                classNames = [cname.strip() for cname in f.readlines()]

            net = cv2.dnn.readNet('Raspberry Pi\detections\yolov4-tiny.weights', 'Raspberry Pi\detections\yolov4-tiny.cfg')
            model = cv2.dnn_DetectionModel(net)
            model.setInputParams(size=(416, 416), scale=1/255)

            while True:
                if state == True:
                    if (time.perf_counter() - tempo0 >= 1800 or tempo0 == 0):
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
                                        tempo0 = time.perf_counter()
                                        if mode == 'Horário':
                                            if TimeController.nowIsValid(schedules):
                                                cv2.rectangle(frame, box, color, 2)
                                                cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                                                print('Máquina ativada')
                                            else:
                                                print('Fora de horário')
                                        else:
                                            cv2.rectangle(frame, box, color, 2)
                                            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                                    else:
                                        print('Muito distante')
                    else:
                        print(str(1800 - (time.perf_counter() - tempo0)) + ' segundos até a utilização')

                    cv2.imshow('Detections', frame)
                    if cv2.waitKey(1) == 27:
                        break
                else:
                    print('Dados necessarios nao foram vinculados')
        except Exception as e:
            print(e)

#################################################### API

app = Flask(__name__)

hostname = socket.gethostname()
localIp = socket.gethostbyname(hostname)

@app.route("/")
def root():
    return {'message': "API is running!"}

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
_thread.start_new_thread(run, ())
detector.run()