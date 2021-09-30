# API
from flask import Flask, jsonify, request
import socket
import json

# Detections
import cv2
import time
import pafy
import _thread

## Deteccoes dos animais

# Valores que serao utilizados pelo Raspberry PI
animal = "dog" # Tipo do animal
mode = "Horário"
quantity = 50 # Quantidade de racao
schedules = [] # Horarios de alimentacao

dogUrl = 'https://www.youtube.com/watch?v=TZn7oWMHD90' # Video de cao
catUrl = 'https://www.youtube.com/watch?v=7Nn7NZI_LN4' # Video de gato

class Detector:

    def __init__(self, url):
        self.url = url
    
    def run(self):
        videoPafy = pafy.new(self.url)
        best = videoPafy.getbest(preftype='mp4')
        cap = cv2.VideoCapture(best.url)
    
        # Define cores para fazer as marcacoes de objeto
        COLORS = [(0,255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
        tempo0 = 0

        # Recuperacao dos objetos treinados
        class_names = []
        with open('api\coco.names', 'r') as f:
            class_names = [cname.strip() for cname in f.readlines()]

        net = cv2.dnn.readNet('api\yolov4-tiny.weights', 'api\yolov4-tiny.cfg')
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(416, 416), scale=1/255)

        while True:
            # if (time.perf_counter() - tempo0 >= 1800 or tempo0 == 0):
            _, frame = cap.read()

            classes, scores, boxes = model.detect(frame, 0.1, 0.2) # Valores para melhorar rede neural
            for (classId, score, box) in zip(classes, scores, boxes):
                color = COLORS[int(classId) % len(COLORS)]

                label = f"{class_names[classId[0]].capitalize()} : {score}"

                if class_names[classId[0]] == animal:
                    if score >= 0.6:
                        cv2.rectangle(frame, box, color, 2)
                        cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        largura = box[2] #length x
                        comprimento = box[3] #length y
                        if (largura >= 220 or comprimento >= 220):
                            tempo0 = time.perf_counter()
                        else:
                                print('Muito distante')
            # else:
            #     print(str(1800 - (time.perf_counter() - tempo0)) + ' segundos até a utilização')

            cv2.imshow('Detections', frame)
            if cv2.waitKey(1) == 27:
                break

## Servidor

app = Flask(__name__)

## Obtencao de IP
hostname = socket.gethostname()
localIp = socket.gethostbyname(hostname)

@app.route("/")
def hello_world():
    return jsonify({'message': "API is running!"})

@app.route("/animal", methods=['GET', 'POST'])
def animalRoot():
    global animal 

    if request.method == 'POST':
        data = request.get_json()
        animal = data['animal']

        return jsonify({'animal': animal})
    
    elif request.method == 'GET':
        return jsonify({'animal': animal})

@app.route("/mode", methods=['GET', 'POST'])
def modeRoot():
    global mode

    if request.method == 'POST':
        data = request.get_json()
        mode = data['mode']

        return jsonify({'mode': mode})
    
    elif request.method == 'GET':
        return jsonify({'mode': mode})

@app.route("/quantity", methods=['GET', 'POST'])
def quantityRoot():
    global quantity

    if request.method == 'POST':
        data = request.get_json()
        quantity = data['quantity']

        return jsonify({'quantity': quantity})

    elif request.method == 'GET':
        return jsonify({'quantity': quantity})

def run ():
    app.run(host=localIp, port=5000)


detector = Detector(url=dogUrl)
_thread.start_new_thread(run, ())
detector.run()