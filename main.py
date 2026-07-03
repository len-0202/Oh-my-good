import time
import gpiozero
import cv2
import os
import pygame
import threading
import face_detect

#SW_PIN0 = 17
#SW_PIN1 = 18

#sw0 = gpiozero.DigitalInputDevice(SW_PIN0) 
#sw1 = gpiozero.DigitalInputDevice(SW_PIN1) #緑

camera_thread = threading.Thread(
    target=face_detect.CAMERA,
    daemon=True
)

camera_thread.start()
print("値を入力→")
switch = input()
print(f"value: {switch}")

while True:
    if switch == 1:
        Sleepy_judge += CAMERA() #カメラの画像認識
    
        if Sleepy_judge == 1: #居眠り中か判断
            print("居眠り中\n")
            print("アームに信号を送信")

            #アームに信号を送信
            time.sleep(10) #10秒待機

            #music() # 音楽再生

        else: #Sleepy_judge == 0
            print("居眠りしていません\n")
    else:
        print("値が違います")
         
