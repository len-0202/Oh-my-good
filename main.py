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

threading.Thread(
    target=face_detect.CAMERA,
    daemon=True
).start()

while True:

    switch = int(input("1を入力: "))

    if switch == 1:

        if face_detect.get_camera_status() == 1:
            print("居眠り中")
            print("アームに信号を送信")

            #アームに信号を送信
            time.sleep(10) #10秒待機

            #music() # 音楽再生

        else:#Sleepy_judge == 0
            print("居眠りしていません")
