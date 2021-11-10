import requests

url = 'http://127.0.1.1:5000/feeds/148'
myObj = {"animal": "dog", "mode": "Horário", "quantity": 50, "schedules": ["09:55"]}
x = requests.put(url, json = myObj)

print(x.text)