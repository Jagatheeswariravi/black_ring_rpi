import cv2
import numpy as np
import PySimpleGUI as sg
from PIL import Image
import io
import os
from datetime import datetime
import math
from time import sleep
from pymodbus.client import ModbusTcpClient
import RPi.GPIO as GPIO

refPt = [(114, 450), (184, 518)]

name =""

############################## Setting up code of raspberrypi GPIO input########################### 
GPIO.setmode(GPIO.BOARD)
button1=16
GPIO.setup(button1,GPIO.IN)
##############################Setting up code for gui window#########################################
##########################################  PLC code###########################################

PLC_IP =" 192.168.0.180"
PLC_PORT = 502
PLC_REGISTER_ADDRESS = 0 
TARGET_PLC_VALUE = 42 

client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
client.connect()

sg.theme('black')

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
        
    def search_for_black_circle(image_path):
        global image, refPt

        # Load the image
        image = cv2.imread(image_path)
        clone = image.copy()
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        detected_circles = process_roi(roi)

        if detected_circles is not None:
            for circle in detected_circles:
                center = (circle[0] + refPt[0][0], circle[1] + refPt[0][1])
                radius = circle[2]
                cv2.circle(image, center, radius, (0, 0, 255), 2)

        # Show the whole image with detected circles (if any)
        cv2.imshow("Image with Detected Circles", image)
        cv2.waitKey(0)

    def process_roi(roi):
        global name
        # Convert ROI to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding to create a binary image
        _, binary_roi = cv2.threshold(gray_roi, 50, 255, cv2.THRESH_BINARY)

        # Use Hough Circle Transform to detect circles
        circles = cv2.HoughCircles(binary_roi, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=50)


        if circles is not None:
            name = "ok"
            circles = np.uint16(np.around(circles))
            return (circles[0,:])


        else:
           return None



    def main():
        img = capture_frames()
        image =search_for_black_circle(img)
        cv2.imwrite("ring1.png",image)
        window["-COLOR-"].update("ring1.png")
        if name == "ok":
            window['OK'].update(visible=True)
            client.write_registers(1000,"Ok",unit=1)

        else:
            window['Not OK'].update(visible=True)
            client.write_registers(1000,"Not ok",unit=1)
    


    ##################################triggering code####################################### 
    latched_input = client.read_holding_registers(PLC_REGISTER_ADDRESS, count=1, unit=0x01)
    if latched_input == 1:
        main()
        sleep(.5)
    client.close()  
    
    ##################################triggering code####################################### 

    if GPIO.input(button1) == 0:
        main() 
        sleep(.5)
    



   