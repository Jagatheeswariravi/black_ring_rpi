import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import Image
import io
import os
from datetime import datetime
from ultralytics import YOLO
import math
from time import sleep
#import RPi.GPIO as GPIO

class_name =""

## Setting up code of raspberrypi GPIO input 
# GPIO.setmode(GPIO.BOARD)
# button1=16
# GPIO.setup(button1,GPIO.IN)
##Setting up code for gui window
sg.theme('black')


def start_button_click():
    main()

column_1 = [
            [sg.Image("ring1.png",key='-COLOR-', pad=(0, 25),expand_y=True,expand_x=True)]]
show_ok=True
show_not_ok=True
column_2 = [[sg.Button('Start', size=(8, 2), font=('Times New Roman', 16), pad=(0, 5), button_color="blue",
               key='-START-'),
     sg.Button('OK', size=(10, 2), font=('Times New Roman', 16), pad=(0, 5),button_color="green",visible=False),
     sg.Button('Not OK', size=(10, 2), font=('Times New Roman', 16), pad=(0, 5),button_color="red",visible=False)
]]

layout = [

    [
     sg.Column(column_1), sg.Column(column_2, pad=(10, 40))
     ]
]

window = sg.Window('   WIPER LINK SEAL PRESENCE CHECKING   ', layout, size=(1200, 650), 
                   margins=(1, 1),titlebar_font=('Times New Roman',28),titlebar_background_color="white",
                   titlebar_text_color="green",titlebar_icon="logo.png",use_custom_titlebar=True,auto_size_buttons=True,background_color="black")



while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    
    show_ok = True
    show_not_ok = False

    def capture_frames():
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            sg.popup_error('Failed to access the camera!')
            return

        ret, frame = cap.read()

        if ret:
            return frame
        

    def yolo_detection(img):
        model = YOLO("C:\\Users\\PMTC-ELE\\Downloads\\weights.pt")
        results = model.predict(img)
        global class_name

        classNames = {0:"ok",1:"not_ok"}

        for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    #cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    class_name = classNames[cls]

                    if class_name == "ok":
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                        label = f"{class_name} - {conf}"
                        t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=1)[0]
                        c2 = x1 + t_size[0], y1 - t_size[1] - 3
                        cv2.rectangle(img, (x1, y1), c2, [255, 255, 255], -1, cv2.LINE_AA)
                        cv2.putText(img, label, (x1, y1 - 2), 0, 1, [0, 255, 0], thickness=2, lineType=cv2.LINE_AA)
                    if class_name == "not_ok":
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        label = f"{class_name} - {conf}"
                        t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=1)[0]
                        c2 = x1 + t_size[0], y1 - t_size[1] - 3
                        cv2.rectangle(img, (x1, y1), c2, [255, 255, 255], -1, cv2.LINE_AA)
                        cv2.putText(img, label, (x1, y1 - 2), 0, 1, [0, 0, 255], thickness=2, lineType=cv2.LINE_AA)
        return img,class_name

    def main():
        img = capture_frames()
        #img=cv2.imread("C:\\Users\\PMTC-ELE\\Documents\\black_ring\\ok\\frame_0020.jpg") 
        image,name = yolo_detection(img)
        cv2.imwrite("ring1.png",image)
        window["-COLOR-"].update("ring1.png")
        if name == "ok":
            window['OK'].update(visible=True)
            

        else:
            
            window['Not OK'].update(visible=True)
    if event == '-START-':  
        main()

    ##triggering code    

    # if GPIO.input(button1) == 0:
    #     main() 
    #     sleep(.5)
    

   

window.close()
