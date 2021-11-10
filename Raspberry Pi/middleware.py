import cv2
import pafy
import requests

url = 'https://www.youtube.com/watch?v=TZn7oWMHD90'
animal = 'dog'

class Detector:
    
    def __init__(self, url):
        self.url = url
    
    def run(self):
        global state

        try:
            videoPafy = pafy.new(self.url)
            best = videoPafy.getbest(preftype='mp4')
            cap = cv2.VideoCapture(best.url)
    
            COLORS = [(0,255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
            # tempo0 = 0

            class_names = []
            with open('./detections/coco.names', 'r') as f:
                class_names = [cname.strip() for cname in f.readlines()]

            net = cv2.dnn.readNet('./detections/yolov4-tiny.weights', './detections/yolov4-tiny.cfg')
            model = cv2.dnn_DetectionModel(net)
            model.setInputParams(size=(416, 416), scale=1/255)

            while True:
                # if state == True:
                # if (time.perf_counter() - tempo0 >= 1800 or tempo0 == 0):
                _, frame = cap.read()

                classes, scores, boxes = model.detect(frame, 0.1, 0.2)
                for (classId, score, box) in zip(classes, scores, boxes):
                    color = COLORS[int(classId) % len(COLORS)]

                    label = f"{class_names[classId[0]].capitalize()} : {score}"

                    if class_names[classId[0]] == animal:
                        if score >= 0.65:
                            # largura = box[2] # length x
                            # comprimento = box[3] # length y
                            # if (largura >= 220 or comprimento >= 220):
                            # if mode == 'Horário':
                            #     if TimeController.nowIsValid(schedules):
                            #         cv2.rectangle(frame, box, color, 2)
                            #         cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            #         print('Máquina ativada')
                            #         # tempo0 = time.perf_counter()
                            #     else:
                            #         print('Fora de horário')
                            # else:

                            # --> Por aproximacao
                            cv2.rectangle(frame, box, color, 2)
                            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                            requests.post('http://192.168.0.13:5000/activate')
                            # else:
                            #     print('Muito distante')
                # else:
                #     print(str(1800 - (time.perf_counter() - tempo0)) + ' segundos até a utilização')

                cv2.imshow('Detections', frame)
                if cv2.waitKey(1) == 27:
                    break

        except Exception as e:
            print(e)


detector = Detector(url)
detector.run()