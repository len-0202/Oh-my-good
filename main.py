import time
import gpiozero
import cv2
import os
import pygame

SW_PIN0 = 17
#SW_PIN1 = 18

sw0 = gpiozero.DigitalInputDevice(SW_PIN0) 
#sw1 = gpiozero.DigitalInputDevice(SW_PIN1) #緑

while True:
    if sw0.value == 1:
        Camera_judge += CAMERA() #カメラの画像認識
        Sleepy_judge += Sleepy(Camera_judge) #居眠りの判定
    
        if Sleepy_judge >= 1: #居眠り中か判断
            print("居眠り中\n")
            print("アームに信号を送信")

            #アームに信号を送信
            time.sleep(10) #10秒待機

            music() # 音楽再生

         