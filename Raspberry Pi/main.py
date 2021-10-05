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

# Multicast
from multicast_server import MulticastServer


#################################################### Deteccoes dos animais

# Valores que serao utilizados pelo Raspberry PI
animal = "dog" # Tipo do animal
mode = "Aproximação" # Modo de despejamento
quantity = 50 # Quantidade de racao
schedules = ['18:50', '19:00'] # Horarios de alimentacao

consumedQuantity = 0
initialDate = None

dogUrl = 'https://www.youtube.com/watch?v=TZn7oWMHD90' # Video de cao
catUrl = 'https://www.youtube.com/watch?v=7Nn7NZI_LN4' # Video de gato

class Detector:

    def __init__(self, url):
        self.url = url
    
    def run(self):
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
        except Exception as e:
            print(e)


#################################################### Servidor

app = Flask(__name__)

hostname = socket.gethostname()
localIp = socket.gethostbyname(hostname)

@app.route("/")
def hello_world():
    return {'message': "API is running!"}

@app.route("/animal", methods=['GET', 'POST'])
def animalRoot():
    global animal 

    if request.method == 'POST':
        data = request.get_json()
        animal = data['animal']

        return {'animal': animal}
    
    elif request.method == 'GET':
        return {'animal': animal}

@app.route("/mode", methods=['GET', 'POST'])
def modeRoot():
    global mode

    if request.method == 'POST':
        data = request.get_json()
        mode = data['mode']

        return {'mode': mode}
    
    elif request.method == 'GET':
        return {'mode': mode}

@app.route("/quantity", methods=['GET', 'POST'])
def quantityRoot():
    global quantity

    if request.method == 'POST':
        data = request.get_json()
        quantity = data['quantity']

        return {'quantity': quantity}

    elif request.method == 'GET':
        return {'quantity': quantity}

def run ():
    app.run(host=localIp, port=5000)


#################################################### Threads

detector = Detector(url=dogUrl)
multicastServer = MulticastServer()

_thread.start_new_thread(multicastServer.run, ())
_thread.start_new_thread(run, ())
detector.run()
