from flask import Flask, jsonify, request
import socket
import json
from threading import Thread

app = Flask(__name__)

## Obtencao de IP
hostname = socket.gethostname()
localIp = socket.gethostbyname(hostname)

# Valores que serao utilizados pelo Raspberry PI
animal = "Cão" # Tipo do animal
mode = "Horário"
quantity = 50 # Quantidade de racao
schedules = [] # Horarios de alimentacao

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

def keepAlive():
    t = Thread(target=run)
    t.start()