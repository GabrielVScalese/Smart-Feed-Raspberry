#################################################### Bibliotecas

# API
from flask import Flask, request
import socket
import json
import _thread

# Deteccoes
import cv2
import time
import pafy
from time_controller import TimeController
import datetime
import pytz
tz = pytz.timezone('America/Sao_Paulo')

# Multicast
from multicast_server import MulticastServer


#################################################### Deteccoes dos animais

initialDate = datetime.datetime.now(tz)

# Valores que serao utilizados pelo Raspberry PI
animal = None # Tipo do animal
mode = None # Modo de despejamento
quantity = None # Quantidade de racao
schedules = None # Horarios de alimentacao

dogUrl = 'https://www.youtube.com/watch?v=TZn7oWMHD90' # Video de cao
catUrl = 'https://www.youtube.com/watch?v=7Nn7NZI_LN4' # Video de gato

state = False # Indicar se a maquina esta vinculado a um pet
petId = None # Para fazer requisicoes

class Detector:

    def __init__(self, url):
        self.url = url
    
    def run(self):
        global state

        try:
            videoPafy = pafy.new(self.url)
            best = videoPafy.getbest(preftype='mp4')
            cap = cv2.VideoCapture('./video.mp4')
    
            COLORS = [(0,255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
            tempo0 = 0

            class_names = []
            with open('./detections/coco.names', 'r') as f:
                class_names = [cname.strip() for cname in f.readlines()]

            net = cv2.dnn.readNet('./detections/yolov4-tiny.weights', './detections/yolov4-tiny.cfg')
            model = cv2.dnn_DetectionModel(net)
            model.setInputParams(size=(416, 416), scale=1/255)

            while True:
                if state == True:
                # if (time.perf_counter() - tempo0 >= 1800 or tempo0 == 0):
                    _, frame = cap.read()

                    classes, scores, boxes = model.detect(frame, 0.1, 0.2)
                    for (classId, score, box) in zip(classes, scores, boxes):
                        color = COLORS[int(classId) % len(COLORS)]

                        label = f"{class_names[classId[0]].capitalize()} : {score}"

                        if class_names[classId[0]] == animal:
                            if score >= 0.65:
                                largura = box[2] # length x
                                comprimento = box[3] # length y
                                # if (largura >= 220 or comprimento >= 220):
                                if mode == 'Horário':
                                    if TimeController.nowIsValid(schedules):
                                        cv2.rectangle(frame, box, color, 2)
                                        cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                                        print('Máquina ativada')
                                        # tempo0 = time.perf_counter()
                                    else:
                                        print('Fora de horário')
                                else:
                                    cv2.rectangle(frame, box, color, 2)
                                    cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                                # else:
                                #     print('Muito distante')
                    # else:
                    #     print(str(1800 - (time.perf_counter() - tempo0)) + ' segundos até a utilização')

                    cv2.imshow('Detections', frame)
                    if cv2.waitKey(1) == 27:
                        break
                else:
                    print('Dados necessarios nao foram vinculados')
        except Exception as e:
            print(e)


#################################################### Servidor

app = Flask(__name__)

hostname = socket.gethostname()
localIp = socket.gethostbyname(hostname)

@app.route("/")
def root():
    return {'message': "API is running!"}

@app.route('/feeds', methods=['POST', 'GET'])
def feedRoot():
    global petId
    global animal
    global mode
    global quantity
    global schedules
    global state

    if request.method == 'POST':
        data = request.get_json()
        petId = data['petId']
        animal = data['animal']
        mode = data['mode']
        quantity = data['quantity']
        schedules = data['schedules']
        state = True

        return {'petId': petId, 'animal': animal, 'mode': mode, 'quantity': quantity, 'schedules': schedules}

    if request.method == 'GET':
        return {petId, animal, mode, quantity, schedules}

def run ():
    app.run(host=localIp, port=5000)


#################################################### Threads

detector = Detector(url=dogUrl)
multicastServer = MulticastServer()

_thread.start_new_thread(multicastServer.run, ())
_thread.start_new_thread(run, ())
detector.run()
