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

value = input("値を入力してください: ")

if switch == 1:
    camera_status = face_detect.get_camera_status() #カメラの画像認識
    
    if camera_status == 1: #居眠り中か判断
        print("居眠り中\n")
        print("アームに信号を送信")

        #アームに信号を送信
        time.sleep(10) #10秒待機

        #music() # 音楽再生

    else: #Sleepy_judge == 0
        print("居眠りしていません\n")
else:
    print("値が違います")
         
