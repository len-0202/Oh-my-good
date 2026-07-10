import time
from gpiozero import Button
import cv2
import os
import pygame
import threading
import face_detect

#SW_PIN0 = 17
#SW_PIN1 = 18

#sw0 = gpiozero.DigitalInputDevice(SW_PIN0) 
#sw1 = gpiozero.DigitalInputDevice(SW_PIN1) #緑

button = Button(18, pull_up=False, bounce_time=0.05)

mode = False

threading.Thread(
    target=face_detect.CAMERA,
    daemon=True
).start()

while True:

    # ボタンが押された瞬間
    if button.is_pressed:
        mode = not mode

        if mode:
            print("監視開始")
        else:
            print("監視終了")

        while button.is_pressed:
            time.sleep(0.01)

    if mode:
        if face_detect.get_camera_status() == 1:

            print("居眠り中")
            print("アームに信号を送信")

            # アーム制御
            time.sleep(10)
            #music() # 音楽再生
            time.sleep(10)

            print("起きるまで待機...")

            # 起きるまで待機
            while face_detect.get_camera_status() == 1:
                time.sleep(0.5)

            print("監視再開")

    time.sleep(0.1)