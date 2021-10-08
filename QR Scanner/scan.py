import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import requests
import pygame
import json
import RPi.GPIO as GPIO
import time
relay_pin = 20
def setup():
    GPIO.setmode(GPIO.BCM)
    SERVO = 20
    GPIO.setup(SERVO, GPIO.OUT)

   

pygame.init()
config = json.loads(open("scanner.json", "r").read())
print(config)
def playsound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (0,400)
fontScale              = 1
fontColor              = (0,255,0)
lineType               = 2
def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)

    for obj in barcode:
    
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        print(barcodeData)
        url = f"https://ansimhwajangsil.compilingcoder.repl.co/api/scan/{barcodeData}/{config['ID']}".replace(" ", "%20")
        print(url)
        response = requests.get(url=url)
        print(response)
        json_data = response.json()
        string = "Scanning..."
        print(json_data)
        
        cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
        
       
        if json_data["result"] == "success":
            playsound("music.wav")
            time.sleep(1)
            playsound("success.mp3")
            
            try:
                

                setup()
                print("OPEN")
                GPIO.output(relay_pin, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.cleanup()
                time.sleep(5)
                setup()
                print("close")
                GPIO.output(relay_pin, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.cleanup()
                
            except KeyboardInterrupt:
                break
            return True
        else:
           playsound("music2.wav")
           playsound("fail.mp3")
           return False
        time.sleep(2)
        
        

cap = cv2.VideoCapture(0)
while True:
    set_time_delay = 0
    while True:
        if set_time_delay == 1:
            i = 0
            while i < 120:
                ret, frame = cap.read()
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                
                cv2.imshow('Scanner', frame)
                code = cv2.waitKey(10)
                if code == ord('q'):
                    break
                i+=1
                print(f"IDLE QUEUE ({i}/120) ")
                
                if i == 120:
                    print("QUEUE FINISHED.")
                    set_time_delay = 0
        ret, frame = cap.read()
        if decoder(frame) != None:
            set_time_delay = 1
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow('Scanner', frame)
        
        code = cv2.waitKey(10)
        if code == ord('q'):
            break
    time.sleep(5)
GPIO.cleanup()